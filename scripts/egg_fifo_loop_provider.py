"""One live OpenAI Responses call for the FIFO assertion experiment (Python stdlib)."""
import http.client
import json
import math
import os
from urllib import error, request


ENDPOINT = "https://api.openai.com/v1/responses"
KNOWN_ERRORS = {
    "insufficient_quota", "rate_limit_exceeded", "billing_hard_limit_reached",
    "model_not_found", "invalid_api_key", "invalid_request_error",
}


class ProviderError(RuntimeError):
    """Safe error text plus accounting even when no usable candidate was returned."""

    def __init__(self, message, receipt):
        super().__init__(message)
        self.receipt = receipt


class _NoRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _strict_json(text):
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError("duplicate JSON field")
            obj[key] = value
        return obj

    def reject_constant(value):
        raise ValueError("nonfinite JSON value")

    return json.loads(text, object_pairs_hook=unique, parse_constant=reject_constant)


def _receipt(model):
    return {"requested_model": model, "id": None, "model": None, "status": None, "usage": None,
            "service_tier": None, "dispatch_attempted": False, "http_status": None}


def decode_response(raw, *, requested_model, schema, http_status=200):
    """Validate a real or fixture provider response. Keep raw usage on candidate failures."""
    receipt = {**_receipt(requested_model), "dispatch_attempted": True, "http_status": http_status}
    try:
        response = _strict_json(raw)
    except (ValueError, UnicodeError):
        raise ProviderError("Responses API returned malformed JSON", receipt) from None
    if not isinstance(response, dict):
        raise ProviderError("Responses API returned an unexpected envelope", receipt)
    for k in ("id", "model", "status", "usage", "service_tier"):
        receipt[k] = response.get(k)
    if receipt["status"] != "completed":
        raise ProviderError("Responses API did not complete the candidate", receipt)
    usage = receipt["usage"]
    token_fields = ("input_tokens", "output_tokens", "total_tokens")
    if (not all(isinstance(receipt[k], str) and receipt[k] for k in ("id", "model"))
            or not isinstance(usage, dict)
            or any(type(usage.get(k)) is not int or usage[k] < 0 for k in token_fields)
            or usage["total_tokens"] != usage["input_tokens"] + usage["output_tokens"]):
        raise ProviderError("Responses API returned incomplete or inconsistent accounting", receipt)
    items = response.get("output")
    if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
        raise ProviderError("Responses API did not return output items", receipt)
    messages = [item for item in items if item.get("type") == "message" and item.get("role") == "assistant"]
    if len(messages) != 1 or messages[0].get("status", "completed") != "completed":
        raise ProviderError("Responses API did not return one complete assistant message", receipt)
    content = messages[0].get("content")
    if not isinstance(content, list) or not content or not all(isinstance(part, dict) for part in content):
        raise ProviderError("Responses API returned empty or invalid assistant content", receipt)
    if any(part.get("type") == "refusal" for part in content):
        raise ProviderError("Responses API declined the assertion request", receipt)
    if not all(part.get("type") == "output_text" and isinstance(part.get("text"), str) for part in content):
        raise ProviderError("Responses API did not return structured text", receipt)
    try:
        value = _strict_json("".join(part["text"] for part in content))
    except (ValueError, UnicodeError):
        raise ProviderError("Responses API returned invalid candidate JSON", receipt) from None
    if (not isinstance(value, dict) or not set(schema.get("required", ())).issubset(value)
            or (schema.get("additionalProperties") is False and set(value) - set(schema.get("properties", {})))):
        raise ProviderError("Responses API returned an unexpected candidate object", receipt)
    return {**receipt, "output": value}


def respond(messages, schema, *, model, max_output_tokens=2048, timeout=90.0, reasoning_effort=None):
    """Send one HTTPS request; the caller validates assertion semantics and controls the round budget."""
    if not isinstance(model, str) or not model.strip():
        raise ValueError("an explicit model is required")
    if type(max_output_tokens) is not int or max_output_tokens <= 0:
        raise ValueError("max_output_tokens must be a positive integer")
    if not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or timeout <= 0:
        raise ValueError("timeout must be finite and positive")
    if not isinstance(messages, list) or not messages or not all(isinstance(m, dict) for m in messages):
        raise ValueError("messages must be a nonempty list of input messages")
    if not isinstance(schema, dict) or schema.get("type") != "object":
        raise ValueError("a root object JSON schema is required")
    receipt = _receipt(model)
    token = os.environ.get("OPENAI_API_KEY", "")
    if not token or any(not 33 <= ord(c) <= 126 for c in token):
        raise ProviderError("OPENAI_API_KEY is missing or invalid", receipt)
    body = {"model": model, "input": messages, "max_output_tokens": max_output_tokens, "store": False,
            "text": {"format": {"type": "json_schema", "name": "fifo_assertion_revision", "strict": True, "schema": schema}}}
    if reasoning_effort is not None:
        body["reasoning"] = {"effort": reasoning_effort}
    payload = json.dumps(body, ensure_ascii=False, allow_nan=False).encode("utf-8")
    call = request.Request(ENDPOINT, data=payload, method="POST",
                           headers={"Content-Type": "application/json", "Authorization": "Bearer " + token})
    opener = request.build_opener(_NoRedirect)
    receipt["dispatch_attempted"] = True
    try:
        with opener.open(call, timeout=timeout) as response:
            receipt["http_status"] = response.status
            raw = response.read()
    except error.HTTPError as exc:
        receipt["http_status"] = exc.code
        category = None
        try:
            payload = _strict_json(exc.read(65536))
            detail = payload.get("error", {}) if isinstance(payload, dict) else {}
            if isinstance(detail, dict):
                for field in ("code", "type"):
                    value = detail.get(field)
                    if isinstance(value, str) and value in KNOWN_ERRORS:
                        category = value
                        break
        except (ValueError, UnicodeError, OSError, http.client.HTTPException):
            pass
        finally:
            exc.close()
        receipt["error_code"] = category
        suffix = f": {category}" if category else ""
        raise ProviderError(f"Responses API HTTP failure ({receipt['http_status']}){suffix}", receipt) from None
    except (OSError, http.client.HTTPException):
        raise ProviderError("Responses API transport failure; provider usage unknown", receipt) from None
    return decode_response(raw, requested_model=model, schema=schema, http_status=receipt["http_status"])
