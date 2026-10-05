import json
from pathlib import Path
from tempfile import TemporaryDirectory
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
                if operation == "offline_corpus":
                    self.assertEqual(result["access"], "invalid_request")
                elif operation == "capabilities":
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

    def test_offline_corpus_reads_only_bounded_matches(self):
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "assets-manifest.json").write_text(json.dumps({
                "schema_version": 1,
                "assets": [{"asset_id": "a1", "kind": "thumbnail", "name": "timer.png", "source": "browser:1"},
                            {"asset_id": "a2", "kind": "thumbnail", "name": "other.png", "source": "browser:1"}],
            }))
            (root / "appllama-apps-observed-20260915.json").write_text(json.dumps({
                "source": "https://appllama.io/", "appPaths": ["/apps/1/timer", "/apps/2/other"],
                "complete": False, "observedApps": 2,
            }))
            result = json.loads(app_design_research({
                "operation": "offline_corpus", "task": "find timer", "query": "timer",
                "corpus_path": str(root), "limit": 1,
            }))
        self.assertEqual(result["access"], "offline")
        self.assertEqual(len(result["assets"]), 1)
        self.assertEqual(len(result["apps"]), 1)
        self.assertEqual(result["apps"][0]["analytics"]["revenue"]["status"], "unavailable")
        self.assertEqual(result["coverage"]["app_paths_observed"], 2)

    def test_offline_corpus_prefers_complete_catalog_and_keeps_revenue_observed(self):
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "downloads").mkdir()
            (root / "appllama-apps-observed-20260915.json").write_text(json.dumps({
                "source": "https://appllama.io/", "appPaths": ["/apps/1/old"],
                "complete": False, "observedApps": 1,
            }))
            (root / "downloads" / "appllama-browser-catalog-complete.json").write_text(json.dumps({
                "complete": True,
                "apps": {
                    "/apps/1/transit": {"url": "https://appllama.io/apps/1/transit",
                                        "text": "Transit\n$100K/mo\nest. revenue"},
                    "/apps/2/masked": {"url": "https://appllama.io/apps/2/masked",
                                       "text": "Masked\n$##K/mo\nest. revenue"},
                },
                "media": {},
            }))
            result = json.loads(app_design_research({
                "operation": "offline_corpus", "task": "find apps", "query": "apps", "corpus_path": str(root), "limit": 1,
            }))
        self.assertEqual(result["access"], "offline")
        self.assertEqual(len(result["apps"]), 1)
        self.assertEqual(result["apps"][0]["analytics"]["revenue"]["label"], "$100K/mo")
        self.assertTrue(result["coverage"]["catalog_complete"])
        self.assertFalse(result["coverage"]["details_complete"])
        self.assertEqual(result["provenance"]["files"][0]["path"], "downloads/appllama-browser-catalog-complete.json")

    def test_offline_corpus_rejects_traversal_and_symlinked_files(self):
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "assets-manifest.json").write_text("{}")
            result = json.loads(app_design_research({
                "operation": "offline_corpus", "task": "x", "query": "x",
                "corpus_path": str(root / ".." / root.name),
            }))
        self.assertEqual(result["access"], "invalid_request")

        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            (root / "assets-manifest.json").write_text(json.dumps({"assets": []}))
            (root / "observed.json").write_text(json.dumps({"appPaths": [], "complete": False}))
            (root / "appllama-apps-observed-20260915.json").symlink_to(root / "observed.json")
            result = json.loads(app_design_research({
                "operation": "offline_corpus", "task": "x", "query": "x",
                "corpus_path": str(root),
            }))
        self.assertEqual(result["access"], "invalid_request")

        with TemporaryDirectory() as directory:
            base = Path(directory)
            root, outside = base / "corpus", base / "outside"
            root.mkdir()
            outside.mkdir()
            (outside / "appllama-browser-catalog-complete.json").write_text(json.dumps({"complete": True, "apps": {}}))
            (root / "downloads").symlink_to(outside, target_is_directory=True)
            result = json.loads(app_design_research({
                "operation": "offline_corpus", "task": "x", "query": "x",
                "corpus_path": str(root),
            }))
        self.assertEqual(result["access"], "invalid_request")


if __name__ == "__main__":
    unittest.main()
