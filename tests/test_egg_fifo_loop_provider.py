"""Offline envelope and accounting controls. No test contacts a provider."""
import io
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from egg_fifo_loop_provider import ENDPOINT, ProviderError, decode_response, respond


MODEL = "fixture-model"
SCHEMA = {"type": "object", "properties": {"diagnosis": {"type": "string"}},
          "required": ["diagnosis"], "additionalProperties": False}
MESSAGES = [{"role": "user", "content": "fixture input"}]


def envelope():
    return {"id": "resp_fixture", "model": "model_fixture_snapshot", "status": "completed",
            "service_tier": "default",
            "usage": {"input_tokens": 23, "output_tokens": 17, "total_tokens": 40,
                      "input_tokens_details": {"cached_tokens": 9},
                      "output_tokens_details": {"reasoning_tokens": 4}},
            "output": [{"type": "reasoning", "summary": []},
                       {"type": "message", "role": "assistant", "status": "completed",
                        "content": [{"type": "output_text", "text": '{"diagnosis":"hold valid"}'}]}]}


class ProviderControls(unittest.TestCase):
    def test_strict_single_post_and_complete_receipt(self):
        fake = envelope()
        with (patch.dict(os.environ, {"OPENAI_API_KEY": "unit-test-only"}),
              patch("egg_fifo_loop_provider.request.build_opener") as make):
            opened = make.return_value.open
            res = opened.return_value.__enter__.return_value
            res.status = 200
            res.read.return_value = json.dumps(fake).encode()
            got = respond(MESSAGES, SCHEMA, model=MODEL, max_output_tokens=128, timeout=3)
            req, = opened.call_args.args
            self.assertEqual((opened.call_count, req.full_url, req.get_method()), (1, ENDPOINT, "POST"))
            self.assertEqual(opened.call_args.kwargs, {"timeout": 3})
            body = json.loads(req.data)
            self.assertEqual(body["text"]["format"], {"strict": True, "type": "json_schema",
                                                      "schema": SCHEMA, "name": "fifo_assertion_revision"})
            self.assertEqual(body["max_output_tokens"], 128)
            self.assertNotIn("reasoning", body)
            self.assertFalse(body["store"])
        self.assertEqual((got["requested_model"], got["model"], got["id"]),
                         (MODEL, fake["model"], fake["id"]))
        self.assertEqual(got["output"], {"diagnosis": "hold valid"})
        self.assertEqual(got["usage"], fake["usage"])
        self.assertNotIn("unit-test-only", json.dumps(got))

    def test_incomplete_refusal_and_malformed_candidates_keep_usage(self):
        for scenario in ("incomplete", "refusal", "duplicate_key", "unexpected_field"):
            data = envelope()
            content = data["output"][1]["content"]
            if scenario == "incomplete":
                data["status"] = "incomplete"
            elif scenario == "refusal":
                content[0] = {"type": "refusal", "refusal": "fixture"}
            elif scenario == "duplicate_key":
                content[0]["text"] = '{"diagnosis":"first","diagnosis":"second"}'
            else:
                content[0]["text"] = '{"diagnosis":"abc","extra":true}'
            with self.subTest(scenario=scenario), self.assertRaises(ProviderError) as err:
                decode_response(json.dumps(data), requested_model=MODEL, schema=SCHEMA)
            self.assertEqual(err.exception.receipt["usage"], data["usage"])
            self.assertTrue(err.exception.receipt["dispatch_attempted"])

    def test_missing_key_no_network_and_http_error_no_retry_or_secret(self):
        with (patch.dict(os.environ, {"OPENAI_API_KEY": ""}),
              patch("egg_fifo_loop_provider.request.build_opener") as opener,
              self.assertRaises(ProviderError) as err):
            respond(MESSAGES, SCHEMA, model=MODEL)
        opener.assert_not_called()
        self.assertFalse(err.exception.receipt["dispatch_attempted"])
        with (patch.dict(os.environ, {"OPENAI_API_KEY": "unit-test-only"}),
              patch("egg_fifo_loop_provider.request.build_opener") as opener,
              self.assertRaises(ProviderError) as err):
            opener.return_value.open.side_effect = HTTPError(ENDPOINT, 401, "unit-test-only", {},
                                                              io.BytesIO(b"unit-test-only"))
            respond(MESSAGES, SCHEMA, model=MODEL)
        opener.return_value.open.assert_called_once()
        self.assertEqual(err.exception.receipt["http_status"], 401)
        self.assertIsNone(err.exception.receipt["usage"])
        self.assertNotIn("unit-test-only", str(err.exception) + json.dumps(err.exception.receipt))
