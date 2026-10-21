"""Strict Responses API adapter and deterministic offline/replay adapters."""
import json
import os
import random
import time


SCHEMA = {
    "type": "object", "additionalProperties": False,
    "required": ["actions"],
    "properties": {"actions": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "required": ["reset", "req", "priority_override"],
        "properties": {"reset": {"type": "integer"}, "req": {"type": "integer"},
                       "priority_override": {"type": "integer"}}}}}
}


def validate_actions(value, limit):
    if not isinstance(value, dict) or set(value) != {"actions"} or not isinstance(value["actions"], list):
        raise ValueError("Expected only an actions array")
    actions = value["actions"]
    if not 1 <= len(actions) <= limit:
        raise ValueError(f"Expected 1..{limit} actions")
    for i, item in enumerate(actions):
        if not isinstance(item, dict) or set(item) != {"reset", "req", "priority_override"}:
            raise ValueError(f"Action {i}: required fields are reset, req, priority_override")
        for field, maximum in (("reset", 1), ("req", 255), ("priority_override", 255)):
            if type(item[field]) is not int or not 0 <= item[field] <= maximum:
                raise ValueError(f"Action {i}: {field} must be integer 0..{maximum}")
    return actions


def token_estimate(messages):
    # UTF-8 byte count is a conservative local cap when tokenizer assets are
    # unavailable offline. API-reported usage is the measured token count.
    return sum(len(item["content"].encode("utf-8")) for item in messages) + 16


def usage_record(usage):
    if usage is None:
        return {"input_tokens": None, "output_tokens": None, "total_tokens": None,
                "cached_input_tokens": None, "reasoning_output_tokens": None}
    value = usage.model_dump() if hasattr(usage, "model_dump") else usage
    input_details = value.get("input_tokens_details") or {}
    output_details = value.get("output_tokens_details") or {}
    return {"input_tokens": value.get("input_tokens"),
            "output_tokens": value.get("output_tokens"),
            "total_tokens": value.get("total_tokens"),
            "cached_input_tokens": input_details.get("cached_tokens"),
            "reasoning_output_tokens": output_details.get("reasoning_tokens")}


class OpenAIModel:
    def __init__(self, config, schema=SCHEMA, schema_name="arbiter_actions"):
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is absent from the environment")
        from openai import OpenAI
        self.config = config
        self.schema = schema
        self.schema_name = schema_name
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"],
                             timeout=config["timeout_seconds"], max_retries=0)

    def generate(self, messages, context):
        settings = self.config
        started = time.perf_counter()
        response = self.client.responses.create(
            model=settings["model"], input=messages, store=False,
            max_output_tokens=settings["max_output_tokens"],
            reasoning={"effort": settings["reasoning_effort"]},
            text={"format": {"type": "json_schema", "name": getattr(self, "schema_name", "arbiter_actions"),
                             "strict": True, "schema": getattr(self, "schema", SCHEMA)}})
        latency = time.perf_counter() - started
        returned = response.model
        record = {"requested_model": settings["model"], "returned_model": returned,
                  "response_id": response.id, "latency_seconds": latency,
                  "status": response.status, "incomplete_details": str(response.incomplete_details) if response.incomplete_details else None,
                  "usage": usage_record(response.usage), "output_text": response.output_text}
        if returned != settings["model"]:
            raise ModelResponseError("returned_model_mismatch", record)
        if response.status != "completed":
            raise ModelResponseError("incomplete_response", record)
        try:
            record["parsed"] = json.loads(response.output_text)
        except (ValueError, TypeError):
            raise ModelResponseError("invalid_json", record) from None
        return record


class ModelResponseError(Exception):
    def __init__(self, reason, record):
        super().__init__(reason)
        self.reason, self.record = reason, record


class MockModel:
    """Arm-blind random smoke test; it deliberately ignores coverage feedback."""
    def __init__(self, config):
        self.config = config

    def generate(self, messages, context):
        rng = random.Random(self.config["seed"] + context["repetition"] * 1009 + context["round"])
        actions = []
        for _ in range(self.config["max_new_cycles"]):
            actions.append({"reset": int(rng.randrange(24) == 0),
                            "req": rng.randrange(256),
                            "priority_override": rng.randrange(256) if rng.randrange(3) == 0 else 0})
        return {"requested_model": "mock-random", "returned_model": "mock-random",
                "response_id": f"mock-{context['repetition']}-{context['round']}",
                "latency_seconds": 0.0, "status": "completed", "incomplete_details": None,
                "usage": usage_record(None), "output_text": json.dumps({"actions": actions}),
                "parsed": {"actions": actions}}


class ReplayModel:
    def __init__(self, source):
        self.calls = {}
        self.source_modes = set()
        for line in open(source, encoding="utf-8"):
            item = json.loads(line)
            if item.get("accepted"):
                self.calls[(item["arm"], item["repetition"], item["round"])] = item
                self.source_modes.add(item["mode"])
        if len(self.source_modes) != 1:
            raise ValueError("Replay source must contain one consistent originating mode")
        self.source_mode = self.source_modes.pop()

    def generate(self, messages, context):
        item = self.calls[(context["arm"], context["repetition"], context["round"])]
        return {"requested_model": item["requested_model"], "returned_model": item["returned_model"],
                "response_id": item["response_id"], "latency_seconds": 0.0,
                "status": "completed", "incomplete_details": None, "usage": item["usage"],
                "output_text": json.dumps({"actions": item["actions"]}),
                "parsed": {"actions": item["actions"]}}
