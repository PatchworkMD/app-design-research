import json
import unittest
from research import OPERATIONS, app_design_research


class ExplodingContext:
    def dispatch_tool(self, *args, **kwargs):
        raise AssertionError("network dispatch must stay unreachable")


def request(operation, **extra):
    value = {"operation": operation, "task": "review supplied evidence", "query": "timer"}
    if operation == "inspect_app":
        value["url"] = "https://appllama.io/apps/1/timer"
    elif operation == "inspect_reference":
        value["url"] = "https://appllama.io/screens/1/timer"
    value.update(extra)
    return value


class PublicAdapterTests(unittest.TestCase):
    def test_every_operation_is_disabled_without_dispatch(self):
        ctx = ExplodingContext()
        for operation in OPERATIONS:
            with self.subTest(operation=operation):
                result = json.loads(app_design_research(request(operation), ctx=ctx, task_id="t"))
                if operation == "capabilities":
                    self.assertEqual(result["access"], "disabled")
                else:
                    self.assertEqual(result["access"], "disabled")
                    self.assertIn("written_permission_required", result["limitation_flags"])

    def test_invalid_data_is_bounded(self):
        result = json.loads(app_design_research({"operation": "browse_apps", "task": "", "query": "x"}))
        self.assertEqual(result["access"], "invalid_request")
        self.assertLessEqual(len(result["error"]), 1000)

    def test_no_request_flag_can_enable_network(self):
        result = json.loads(app_design_research(request("browse_apps", allow_network=True,
                            permission_granted=True), ctx=ExplodingContext(), task_id="t"))
        self.assertEqual(result["access"], "disabled")

    def test_credentials_and_oversized_inputs_rejected(self):
        inputs = [request("inspect_app", url="https://user:pass@appllama.io/apps/1/timer"),
                  request("browse_apps", query="x" * 2001), None]
        for value in inputs:
            with self.subTest(value_type=type(value).__name__):
                result = json.loads(app_design_research(value, ctx=ExplodingContext()))
                self.assertEqual(result["access"], "invalid_request")

    def test_capabilities_do_not_claim_research_execution(self):
        result = json.loads(app_design_research(request("capabilities"), ctx=ExplodingContext()))
        self.assertEqual(result["implemented"], [])
        self.assertFalse(result["paid_mcp"])
        self.assertFalse(result["full_parity"])


if __name__ == "__main__":
    unittest.main()
