"""Synthetic checks of structured metadata and relationship provenance."""

import sys
import io
from email.message import Message
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from literature import search


class SciverseExtensionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "requirements").mkdir()
        (self.root / "requirements/privacy.md").write_text(
            search.SCIVERSE_BEGIN + "\nSciverse synthetic queries and identifiers\n" + search.SCIVERSE_MARKER + "\n" + search.SCIVERSE_END, encoding="utf-8")
        self.scope = "Sciverse synthetic queries and identifiers"

    def test_catalog_filters_cursor_and_relation_are_recorded(self):
        catalog = {"fields": [{"name": "year", "filterable": True, "sortable": True, "operators": ["GTE"]}]}
        result = {"results": [{"unique_id": "paper:1", "title": "Paper"}], "next_cursor": "next", "total_count": 2}
        with patch.object(search, "_request", side_effect=[catalog, result, {"items": [{"id": "10/example"}], "total_pages": 2}]) as request:
            sid, _, data = search.metadata_search(self.root, "token", "topic", scope_basis=self.scope, filters=[{"field": "year", "operator": "GTE", "value": 2020}], sort=[{"field": "year", "order": "desc"}], cursor="opaque")
            _, relation = search.add_relations(self.root, "token", sid, "paper:1", "CITATIONS", page=2)
        self.assertEqual(data["routes"][0]["pagination"]["next_cursor"], "next")
        self.assertEqual(request.call_args_list[1].args[2]["cursor"], "opaque")
        self.assertEqual(request.call_args_list[1].args[2]["filters"][0]["operator"], "FILTER_OP_GTE")
        self.assertEqual(request.call_args_list[1].args[2]["sort"][0]["order"], "SORT_ORDER_DESC")
        self.assertEqual(relation["request"]["page"], 2)
        self.assertEqual(relation["inspection"], "relationship-leads")
        with self.assertRaises(search.LiteratureError):
            search.context_request(self.root, sid, "paper:1", 0, 100)
        search.revoke_sciverse(self.root)
        with self.assertRaises(search.LiteratureError):
            search.add_relations(self.root, "token", sid, "paper:1", "CITATIONS")

    def test_catalog_rejects_unavailable_field_and_records_failure(self):
        with patch.object(search, "_request", return_value={"fields": []}) as request:
            _, _, data = search.metadata_search(self.root, "token", "topic", scope_basis=self.scope, filters=[{"field": "year", "value": 2020}])
        self.assertEqual(request.call_count, 1)
        self.assertEqual(data["routes"][0]["status"], "unavailable")

    def test_malformed_response_is_not_reported_as_an_empty_success(self):
        with patch.object(search, "_request", return_value={"code": "UPSTREAM_ERROR"}):
            _, _, data = search.metadata_search(self.root, "token", "topic", scope_basis=self.scope)
        self.assertEqual(data["routes"][0]["status"], "unavailable")

    def test_same_doi_candidates_do_not_merge_versions(self):
        result = {"results": [{"unique_id": "work-1", "doi": "10.1234/Example", "doc_id": "version-a"},
                              {"unique_id": "work-2", "doi": "https://doi.org/10.1234/example", "doc_id": "version-b"}]}
        with patch.object(search, "_request", return_value=result):
            _, _, data = search.metadata_search(self.root, "token", "topic", scope_basis=self.scope)
        self.assertEqual(len(data["routes"][0]["results"]), 2)
        self.assertEqual(len(data["duplicate_candidates"]), 1)
        self.assertEqual(data["duplicate_candidates"][0]["status"], "unverified-same-doi")

    def test_resume_reuses_parameters_after_failure_and_requires_active_scope(self):
        catalog = {"fields": [{"name": "year", "filterable": True, "sortable": True, "operators": ["GTE"]}]}
        first = {"results": [{"unique_id": "paper:1"}], "next_cursor": "next"}
        second = {"results": [{"unique_id": "paper:2"}]}
        filters = [{"field": "year", "operator": "GTE", "value": 2020}]
        sort = [{"field": "year", "order": "desc"}]
        with patch.object(search, "_request", side_effect=[catalog, first, search.LiteratureError("network failed"), second]) as request:
            sid, _, _ = search.metadata_search(self.root, "token", "topic", scope_basis=self.scope, filters=filters, sort=sort, page_size=1)
            _, _, failed = search.resume_metadata_search(self.root, "token", sid)
            self.assertEqual(failed["routes"][-1]["status"], "unavailable")
            _, _, resumed = search.resume_metadata_search(self.root, "token", sid)
        self.assertEqual(len(resumed["routes"]), 3)
        for call in (request.call_args_list[2], request.call_args_list[3]):
            body = call.args[2]
            self.assertEqual((body["query"], body["cursor"], body["page_size"]), ("topic", "next", 1))
            self.assertEqual(body["filters"][0]["value"], 2020)
            self.assertEqual(body["sort"][0]["order"], "SORT_ORDER_DESC")
        self.assertEqual(resumed["routes"][-1]["catalog_source"], "saved-search-snapshot")
        with self.assertRaisesRegex(search.LiteratureError, "no next cursor"):
            search.metadata_resume_request(self.root, sid)
        search.revoke_sciverse(self.root)
        with self.assertRaisesRegex(search.LiteratureError, "No confirmed"):
            search.metadata_resume_request(self.root, sid)

    def test_experimental_materials_require_recorded_source_and_preserve_truncation(self):
        metadata = {"results": [{"unique_id": "paper:1", "doi": "10.1234/example"}]}
        discovery = {"items": [{"schema_id": "schema-1"}]}
        materials = {"items": [{"counts": {"evidence": {"truncated": True}}}]}
        with patch.object(search, "_request", side_effect=[metadata, discovery, materials]) as request:
            sid, _, _ = search.metadata_search(self.root, "token", "topic", scope_basis=self.scope)
            with self.assertRaises(search.LiteratureError):
                search.schema_materials(self.root, "token", sid, "unknown", "survey")
            search.schema_discovery(self.root, "token", sid, "paper:1")
            _, entry = search.schema_materials(self.root, "token", sid, "schema-1", "survey")
        self.assertEqual(request.call_count, 3)
        self.assertTrue(entry["response"]["items"][0]["counts"]["evidence"]["truncated"])
        search.revoke_sciverse(self.root)
        with self.assertRaises(search.LiteratureError):
            search.schema_materials(self.root, "token", sid, "schema-1", "survey")

    def test_resource_requires_recorded_path_and_validates_content(self):
        with patch.object(search, "_request", side_effect=[{"results": [{"unique_id": "paper:1", "doc_id": "doc-1"}]},
                                                            {"content": "Figure: images/fig1.png"}]):
            sid, _, _ = search.metadata_search(self.root, "token", "topic", scope_basis=self.scope)
            search.add_context(self.root, "token", sid, "doc-1", 0, 100)
        class Response(io.BytesIO):
            def __init__(self):
                super().__init__(b"\x89PNG\r\n\x1a\nfixture")
                self.headers = Message()
                self.headers["Content-Type"] = "image/png"
            def geturl(self):
                return search.API_ROOT + "/resource"
        class Opener:
            def open(self, request, timeout):
                return Response()
        with patch.object(search.urllib.request, "build_opener", return_value=Opener()):
            with self.assertRaises(search.LiteratureError):
                search.fetch_resource(self.root, "token", sid, "doc-1", "../secret")
            with self.assertRaises(search.LiteratureError):
                search.fetch_resource(self.root, "token", sid, "doc-1", "images/other.png")
            folder, entry = search.fetch_resource(self.root, "token", sid, "doc-1", "images/fig1.png")
        self.assertEqual(entry["status"], "complete")
        self.assertTrue((folder / entry["file"]).is_file())
        search.revoke_sciverse(self.root)
        with self.assertRaises(search.LiteratureError):
            search.fetch_resource(self.root, "token", sid, "doc-1", "images/fig1.png")


if __name__ == "__main__":
    unittest.main()
