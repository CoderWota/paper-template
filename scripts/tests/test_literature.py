"""Tests for literature discovery, evidence locators, and resumable public-PDF retrieval.

Sciverse adapter responses are synthetic; download tests use a local HTTP fixture server.
These tests do not claim live publisher access or full-text service compatibility.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))

from ingestion import library  # noqa: E402
from ingestion.common import safe_http_url  # noqa: E402
from literature import downloads, search  # noqa: E402

SCOPE = "This isolated test workspace permits synthetic queries and identifiers to OpenDataLab Sciverse for integration testing only."
QUERY = "paper-template connectivity check"
PDF = b"%PDF-1.7\n1 0 obj\n<< /Type /Catalog >>\nendobj\n%%EOF\n"


class LiteratureWorkspaceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="literature test ä ")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "workspace é"
        for relative in ("requirements", "references", "references/searches", "references/downloads",
                         "references/originals", "references/extracted", "references/notes", "manuscript"):
            (self.root / relative).mkdir(parents=True, exist_ok=True)
        (self.root / "requirements" / "privacy.md").write_text(
            "# Privacy and Processing Requirements\n\nNo document-processing or external query-sharing choices have been confirmed yet.\n",
            encoding="utf-8",
        )
        (self.root / "references" / "index.md").write_text(
            "# Reference Index\n\nNo sources have been collected yet.\n", encoding="utf-8"
        )
        self.scope_record = self.root / "confirmation.md"
        self.write_scope()

    def write_scope(self, scope: str = SCOPE, *, replace: bool = False) -> None:
        self.scope_record.write_text(
            "Sciverse integration test\n\nScope: " + scope + "\n\nConfirmation: synthetic-only test authorization.\n",
            encoding="utf-8",
        )
        search.authorize_sciverse(self.root, self.scope_record, replace=replace)


class FixtureHTTPServer:
    """A small local-only HTTP service for deterministic download tests."""

    def __init__(self, replies: dict[str, tuple[int, str, bytes]]) -> None:
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                self.server.requests.append(self.path)
                status, content_type, body = self.server.replies.get(
                    self.path, (404, "text/plain", b"not found")
                )
                self.send_response(status)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, _format: str, *args) -> None:
                return

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.server.replies = replies
        self.server.requests = []
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_port}"

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=5)


class LiteratureSearchTests(LiteratureWorkspaceTestCase):
    def test_sciverse_search_requires_active_scope_and_matching_excerpt(self) -> None:
        search.revoke_sciverse(self.root)
        with patch.object(search, "_request") as request:
            with self.assertRaisesRegex(search.LiteratureError, "No confirmed Sciverse"):
                search.sciverse_search(self.root, "synthetic-token", QUERY, scope_basis=SCOPE)
        self.write_scope()
        with patch.object(search, "_request") as request:
            with self.assertRaisesRegex(search.LiteratureError, "exact excerpt"):
                search.sciverse_search(self.root, "synthetic-token", QUERY, scope_basis="unapproved scope")
        request.assert_not_called()

    def test_cli_checks_scope_before_looking_for_a_credential(self) -> None:
        search.revoke_sciverse(self.root)
        environment = os.environ.copy()
        environment.pop(search.API_KEY_NAME, None)
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "literature.py"), "--root", str(self.root),
             "search-sciverse", "--query", QUERY, "--scope-basis", SCOPE],
            capture_output=True, text=True, encoding="utf-8", timeout=30, env=environment,
        )
        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        self.assertIn("No confirmed Sciverse query-sharing scope", result.stdout)
        self.assertNotIn("credential is not set", result.stdout)

    def test_agentic_search_records_provider_scope_query_ids_and_locators(self) -> None:
        hit = {"doc_id": "doc-1", "chunk_id": "chunk-7", "offset": 34, "page_no": 5,
               "title": "Synthetic paper", "chunk": "a candidate passage"}
        with patch.object(search, "_request", return_value={"hits": [hit]}) as request:
            search_id, folder, data = search.sciverse_search(
                self.root, "synthetic-token-do-not-store", QUERY, scope_basis=SCOPE, top_k=3
            )
        request.assert_called_once()
        route = data["routes"][0]
        result = route["results"][0]
        self.assertEqual(route["provider"], "OpenDataLab Sciverse")
        self.assertEqual(route["query"], QUERY)
        self.assertTrue(route["created_at"])
        self.assertEqual(route["scope_basis"], SCOPE)
        self.assertEqual(result["inspection"], "search-snippet")
        self.assertEqual(result["snippet"], "a candidate passage")
        self.assertEqual(result["provider_id"], "doc-1")
        self.assertEqual(result["locator"], {"doc_id": "doc-1", "chunk_id": "chunk-7", "offset": 34, "page_no": 5})
        record = (folder / "search.json").read_text(encoding="utf-8")
        self.assertNotIn("synthetic-token-do-not-store", record)
        self.assertEqual(data["search_id"], search_id)

    def test_provider_payload_scrubber_removes_signed_urls(self) -> None:
        cleaned = search._scrub({"landing_page": "https://example.test/paper?token=secret#page=2"})
        self.assertEqual(cleaned["landing_page"], "https://example.test/paper")
        self.assertNotIn("token=secret", json.dumps(cleaned))

    def test_metadata_results_remain_metadata_only(self) -> None:
        response = {"results": [{"unique_id": "meta-1", "doc_id": "doc-meta", "title": "Synthetic title",
                                 "doi": "10.1234/example"}], "total_count": 1, "page": 1}
        with patch.object(search, "_request", return_value=response):
            _, _, data = search.metadata_search(self.root, "synthetic-token", "10.1234/example", scope_basis=SCOPE)
        route = data["routes"][0]
        self.assertEqual(route["endpoint"], "meta-search")
        self.assertEqual(route["results"][0]["inspection"], "metadata-only")
        self.assertNotIn("snippet", route["results"][0])

    def test_host_search_requires_coverage_and_keeps_its_own_query(self) -> None:
        with patch.object(search, "_request", return_value={"hits": []}):
            search_id, _, _ = search.sciverse_search(self.root, "synthetic-token", QUERY, scope_basis=SCOPE)
        missing_note = self.root / "missing-note.json"
        missing_note.write_text(json.dumps({"query": "expanded query", "results": []}), encoding="utf-8")
        with self.assertRaisesRegex(search.LiteratureError, "gap or cross-check"):
            search.add_host_search(self.root, search_id, missing_note)

        host_input = self.root / "host-search.json"
        host_input.write_text(json.dumps({"query": "expanded literature query", "provider": "synthetic host search",
                                          "coverage_note": "broadened terminology", "results": [{"title": "Lead"}]}),
                              encoding="utf-8")
        search.add_host_search(self.root, search_id, host_input)
        record = json.loads((self.root / "references" / "searches" / search_id / "search.json").read_text(encoding="utf-8"))
        route = record["routes"][1]
        self.assertEqual(route["query"], "expanded literature query")
        self.assertNotEqual(route["query"], record["query"])
        self.assertEqual(route["coverage_note"], "broadened terminology")
        self.assertTrue(route["created_at"])

    def test_standalone_host_search_records_its_exact_query(self) -> None:
        host_input = self.root / "standalone-host-search.json"
        host_input.write_text(json.dumps({"query": "fallback query", "provider": "synthetic host search",
                                          "coverage_note": "Sciverse was unavailable", "results": []}),
                              encoding="utf-8")
        search_id, _ = search.add_host_search(self.root, None, host_input)
        record = json.loads((self.root / "references" / "searches" / search_id / "search.json").read_text(encoding="utf-8"))
        route = record["routes"][0]
        self.assertEqual(route["query"], "fallback query")
        self.assertEqual(record["query"], "fallback query")
        self.assertTrue(route["created_at"])


    def test_content_context_requires_a_recorded_id_and_active_scope(self) -> None:
        with patch.object(search, "_request", return_value={"hits": [{"doc_id": "doc-1", "chunk": "snippet"}]}):
            search_id, _, _ = search.sciverse_search(self.root, "synthetic-token", QUERY, scope_basis=SCOPE)
        with patch.object(search, "_request") as request:
            with self.assertRaisesRegex(search.LiteratureError, "not present"):
                search.add_context(self.root, "synthetic-token", search_id, "other-doc", 0, 100)
            request.assert_not_called()

        with patch.object(search, "_request", return_value={"text": "retrieved range", "next_offset": 40, "more": False}):
            _, context = search.add_context(self.root, "synthetic-token", search_id, "doc-1", 0, 100)
        self.assertEqual(context["text"], "retrieved range")
        self.assertEqual(context["doc_id"], "doc-1")
        self.assertEqual(context["offset"], 0)
        self.assertTrue(context["created_at"])

        search.revoke_sciverse(self.root)
        self.write_scope("This narrower test permits a different synthetic query only.")
        with patch.object(search, "_request") as request:
            with self.assertRaisesRegex(search.LiteratureError, "exact excerpt"):
                search.context_request(self.root, search_id, "doc-1", 0, 100)
            request.assert_not_called()

    def test_local_search_records_extraction_revision_and_non_page_locator(self) -> None:
        source_id = "src-aaaaaaaaaaaa"
        extracted = self.root / "references" / "extracted" / source_id
        extracted.mkdir()
        (extracted / "document.md").write_text("# Findings\n\nThe supported claim appears here.\n", encoding="utf-8")
        (extracted / "provenance.json").write_text(json.dumps({"revision": "rev-3"}), encoding="utf-8")
        _, folder, results = search.local_search(self.root, "supported claim", [source_id])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["line"], 3)
        self.assertEqual(results[0]["extraction_revision"], "rev-3")
        self.assertEqual(results[0]["locator_status"], "markdown-line-only")
        record = json.loads((folder / "search.json").read_text(encoding="utf-8"))
        self.assertIn("Markdown line numbers are extraction locators", record["routes"][0]["limitations"][0])

    def test_bibliography_audit_separates_key_link_errors_from_claim_support(self) -> None:
        valid_source = "src-aaaaaaaaaaaa"
        archived = self.root / "references" / "originals" / valid_source
        archived.mkdir()
        (archived / "source.pdf").write_bytes(PDF)
        bibliography = self.root / "references" / "bibliography.bib"
        bibliography.write_text(
            "@article{duplicate,\n  sourceid = {" + valid_source + "},\n}\n"
            "@article{duplicate,\n  sourceid = {src-bbbbbbbbbbbb},\n}\n"
            "@article{noid,\n  title = {No source link},\n}\n",
            encoding="utf-8",
        )
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "literature.py"), "--root", str(self.root), "audit-bibliography"],
            capture_output=True, text=True, encoding="utf-8", timeout=30,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate citation key", result.stdout)
        self.assertIn("has no archived original", result.stdout)
        self.assertIn("no sourceid", result.stdout)
        self.assertIn("not whether a source supports a claim", result.stdout)

    def test_request_does_not_retry_http_429(self) -> None:
        class LimitedOpener:
            calls = 0

            def open(self, request, timeout=0):
                self.calls += 1
                raise urllib.error.HTTPError(request.full_url, 429, "rate limited", {}, io.BytesIO(b"limited"))

        opener = LimitedOpener()
        with patch.object(search.urllib.request, "build_opener", return_value=opener), patch.object(search.time, "sleep"):
            with self.assertRaises(search.LiteratureError):
                search._request(search.API_ROOT + "/agentic-search", "synthetic-token", {"query": QUERY})
        self.assertEqual(opener.calls, 1)

    def test_request_retries_server_errors_with_backoff(self) -> None:
        class Response:
            def __init__(self, url: str) -> None:
                self.url = url

            def __enter__(self):
                return self

            def __exit__(self, *_args) -> None:
                return None

            def geturl(self) -> str:
                return self.url

            def read(self) -> bytes:
                return b'{"hits": []}'

        class RecoveringOpener:
            calls = 0

            def open(self, request, timeout=0):
                self.calls += 1
                if self.calls < 3:
                    raise urllib.error.HTTPError(request.full_url, 503, "service unavailable", {}, io.BytesIO(b"retry"))
                return Response(request.full_url)

        opener = RecoveringOpener()
        with patch.object(search.urllib.request, "build_opener", return_value=opener), patch.object(search.time, "sleep") as pause:
            self.assertEqual(search._request(search.API_ROOT + "/agentic-search", "synthetic-token", {"query": QUERY}), {"hits": []})
        self.assertEqual(opener.calls, 3)
        self.assertEqual(pause.call_count, 2)


class LiteratureDownloadTests(LiteratureWorkspaceTestCase):
    def start_server(self, replies: dict[str, tuple[int, str, bytes]]) -> FixtureHTTPServer:
        server = FixtureHTTPServer(replies)
        self.addCleanup(server.close)
        return server

    def test_safe_url_removes_credentials_query_and_fragment(self) -> None:
        self.assertEqual(
            safe_http_url("https://user:pass@[2001:db8::1]:8443/paper.pdf?token=secret#page=3"),
            "https://[2001:db8::1]:8443/paper.pdf",
        )

    def test_bibtex_markdown_and_text_reference_lists_are_read(self) -> None:
        bibliography = self.root / "references" / "list.bib"
        bibliography.write_text("@article{synthetic,\n  title = {Synthetic item},\n  doi = {10.1234/example},\n}\n", encoding="utf-8")
        markdown = self.root / "references" / "list.md"
        markdown.write_text("- https://doi.org/10.2345/second\n", encoding="utf-8")
        text = self.root / "references" / "list.txt"
        text.write_text("A citation without an identifier\nhttps://example.test/paper.pdf\n", encoding="utf-8")

        bib_item = downloads.read_references([str(bibliography)], self.root)[0]
        markdown_item = downloads.read_references([str(markdown)], self.root)[0]
        text_items = downloads.read_references([str(text)], self.root)
        self.assertEqual(bib_item["doi"], "10.1234/example")
        self.assertEqual(markdown_item["doi"], "10.2345/second")
        self.assertEqual(text_items[0]["status"], "metadata-only")
        self.assertEqual(text_items[1]["url"], "https://example.test/paper.pdf")

    def test_public_pdf_download_archives_unchanged_and_records_identity(self) -> None:
        server = self.start_server({"/paper.pdf": (200, "application/pdf", PDF)})
        url = server.base_url + "/paper.pdf"
        batch_id, folder, data = downloads.new_batch(self.root, [url])
        result = downloads.run_batch(self.root, folder, data, emit=lambda _line: None)
        item = result["items"][0]
        archived = self.root / item["archive_path"]
        self.assertEqual(item["status"], "downloaded")
        self.assertEqual(archived.read_bytes(), PDF)
        self.assertEqual(item["sha256"], hashlib.sha256(PDF).hexdigest())
        self.assertEqual(item["final_url"], url)
        self.assertEqual(item["identity_status"], "unverified")
        checked = downloads.verify_identity(self.root, batch_id, 1, "match", "Synthetic title and DOI match the fixture.")
        self.assertEqual(checked["identity_status"], "match")
        self.assertIn("identity_evidence", checked)

    def test_duplicate_doi_is_requested_once(self) -> None:
        server = self.start_server({"/paper.pdf": (200, "application/pdf", PDF)})
        batch_id, folder, data = downloads.new_batch(self.root, ["10.1234/example", "10.1234/example"])
        with patch.object(downloads, "_target_url", return_value=server.base_url + "/paper.pdf"):
            result = downloads.run_batch(self.root, folder, data, emit=lambda _line: None)
        self.assertEqual(server.server.requests, ["/paper.pdf"])
        self.assertEqual([item["status"] for item in result["items"]], ["downloaded", "duplicate"])
        self.assertEqual(result["items"][0]["source_id"], result["items"][1]["source_id"])
        self.assertTrue((folder / "batch.json").is_file())
        self.assertEqual(result["batch_id"], batch_id)

    def test_doi_already_archived_is_not_requested_again(self) -> None:
        server = self.start_server({"/paper.pdf": (200, "application/pdf", PDF)})
        first_folder, first_data = downloads.new_batch(self.root, ["10.1234/example"])[1:]
        with patch.object(downloads, "_target_url", return_value=server.base_url + "/paper.pdf"):
            first = downloads.run_batch(self.root, first_folder, first_data, emit=lambda _line: None)
        self.assertEqual(first["items"][0]["status"], "downloaded")
        second_folder, second_data = downloads.new_batch(self.root, ["10.1234/example"])[1:]
        with patch.object(downloads, "_target_url", return_value=server.base_url + "/paper.pdf"):
            second = downloads.run_batch(self.root, second_folder, second_data, emit=lambda _line: None)
        self.assertEqual(second["items"][0]["status"], "existing")
        self.assertEqual(second["items"][0]["source_id"], first["items"][0]["source_id"])
        self.assertEqual(server.server.requests, ["/paper.pdf"])

    def test_rate_limited_item_retries_only_after_explicit_reset_flag(self) -> None:
        server = self.start_server({"/paper.pdf": (429, "text/plain", b"quota")})
        _, folder, data = downloads.new_batch(self.root, [server.base_url + "/paper.pdf"])
        first = downloads.run_batch(self.root, folder, data, emit=lambda _line: None)
        self.assertEqual(first["items"][0]["status"], "rate-limited")
        server.server.replies["/paper.pdf"] = (200, "application/pdf", PDF)
        skipped = downloads.run_batch(self.root, folder, first, emit=lambda _line: None)
        self.assertEqual(skipped["items"][0]["status"], "rate-limited")
        self.assertEqual(len(server.server.requests), 1)
        retried = downloads.run_batch(self.root, folder, skipped, retry_rate_limited=True, emit=lambda _line: None)
        self.assertEqual(retried["items"][0]["status"], "downloaded")
        self.assertEqual(len(server.server.requests), 2)

    def test_unavailable_non_pdf_and_incomplete_pdf_keep_distinct_statuses(self) -> None:
        replies = {
            "/missing.pdf": (404, "text/plain", b"missing"),
            "/page": (200, "text/html", b"Service notice without a sign-in prompt"),
            "/partial.pdf": (200, "application/pdf", b"%PDF-1.7\npartial body without end marker"),
        }
        server = self.start_server(replies)
        _, folder, data = downloads.new_batch(
            self.root, [server.base_url + "/missing.pdf", server.base_url + "/page", server.base_url + "/partial.pdf"]
        )
        with patch.object(downloads.time, "sleep"):
            result = downloads.run_batch(self.root, folder, data, emit=lambda _line: None)
        self.assertEqual([item["status"] for item in result["items"]], ["unavailable", "metadata-only", "failed"])
        self.assertEqual(list((self.root / "references" / "originals").iterdir()), [])

    def test_login_page_is_not_archived_as_a_pdf(self) -> None:
        server = self.start_server({"/login": (200, "text/html", b"<html>Sign in to continue</html>")})
        _, folder, data = downloads.new_batch(self.root, [server.base_url + "/login"])
        result = downloads.run_batch(self.root, folder, data, emit=lambda _line: None)
        self.assertEqual(result["items"][0]["status"], "login/manual-access-needed")
        self.assertIsNone(result["items"][0].get("source_id"))
        self.assertEqual(list((self.root / "references" / "originals").iterdir()), [])

    def test_rate_limit_stops_further_requests_to_the_same_host(self) -> None:
        server = self.start_server({"/limited.pdf": (429, "text/plain", b"quota"),
                                    "/later.pdf": (200, "application/pdf", PDF)})
        _, folder, data = downloads.new_batch(
            self.root, [server.base_url + "/limited.pdf", server.base_url + "/later.pdf"]
        )
        with patch.object(downloads.time, "sleep"):
            result = downloads.run_batch(self.root, folder, data, emit=lambda _line: None)
        self.assertEqual(server.server.requests, ["/limited.pdf"])
        self.assertEqual([item["status"] for item in result["items"]], ["rate-limited", "rate-limited"])

    def test_failed_item_retries_without_reprocessing_completed_item(self) -> None:
        first_url = "https://example.test/first.pdf"
        second_url = "https://example.test/second.pdf"
        _, folder, data = downloads.new_batch(self.root, [first_url, second_url])
        calls: list[str] = []

        def fake_fetch(url: str, temporary: Path) -> tuple[str, str, int, str]:
            calls.append(url)
            if url == first_url and calls.count(first_url) == 1:
                return "failed", url, 0, "synthetic interrupted transfer"
            temporary.parent.mkdir(parents=True, exist_ok=True)
            content = PDF if url == first_url else PDF.replace(b"1 0 obj", b"2 0 obj")
            temporary.write_bytes(content)
            return "downloaded", url, len(content), hashlib.sha256(content).hexdigest()

        with patch.object(downloads, "_target_url", side_effect=lambda item: item["url"]), \
             patch.object(downloads, "_fetch", side_effect=fake_fetch), patch.object(downloads.time, "sleep"):
            first = downloads.run_batch(self.root, folder, data, emit=lambda _line: None)
            self.assertEqual([item["status"] for item in first["items"]], ["failed", "downloaded"])
            second = downloads.run_batch(self.root, folder, first, emit=lambda _line: None)

        self.assertEqual(calls, [first_url, second_url, first_url])
        self.assertEqual([item["status"] for item in second["items"]], ["downloaded", "downloaded"])
        self.assertEqual(second["items"][0]["attempts"], 2)
        self.assertEqual(second["items"][1]["attempts"], 1)

    def test_signed_url_is_not_stored_or_requested(self) -> None:
        _, folder, data = downloads.new_batch(self.root, ["https://example.test/paper.pdf?signature=secret"])
        item = data["items"][0]
        self.assertEqual(item["status"], "login/manual-access-needed")
        self.assertEqual(item["url"], "https://example.test/paper.pdf")
        self.assertNotIn("signature=secret", json.dumps(data))
        with patch.object(downloads, "_fetch") as fetch:
            result = downloads.run_batch(self.root, folder, data, emit=lambda _line: None)
        fetch.assert_not_called()
        self.assertEqual(result["items"][0]["status"], "login/manual-access-needed")


if __name__ == "__main__":
    unittest.main()
