"""Tests for the mineru.net route against a fake service on this computer.

The fake follows the documented precision API (v4): signed upload addresses, batch results, and a
result archive per file. It proves the workspace's handling of tokens, uploads, failures, and
resumption. It does not prove compatibility with the live service, which needs a real account.
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import re
import subprocess
import sys
import threading
import unittest
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from ingestion.routes import CloudRoute  # noqa: E402
from test_ingest import WorkspaceTestCase, make_docx, make_pdf  # noqa: E402

TOKEN = "test-token-0123456789abcdef"
SIGNATURE = "Signature=secret-signature-value"


class FakeService:
    def __init__(self):
        self.mode, self.polls_until_done, self.failing = "ok", 0, set()
        self.requests, self.uploads, self.batches, self.polls = [], {}, {}, {}
        service = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def reply(self, status: int, body: bytes, kind: str = "application/json") -> None:
                self.send_response(status)
                self.send_header("Content-Type", kind)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def record(self) -> None:
                service.requests.append({"method": self.command, "path": self.path, "headers": {k.lower(): v for k, v in self.headers.items()}})

            def do_POST(self):  # noqa: N802
                self.record()
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                if self.headers.get("Authorization") != f"Bearer {TOKEN}":
                    return self.reply(200, json.dumps({"code": "A0202", "msg": "token error"}).encode())
                if service.mode == "expired":
                    return self.reply(200, json.dumps({"code": "A0211", "msg": "token expired"}).encode())
                if service.mode == "quota":
                    return self.reply(200, json.dumps({"code": -60018, "msg": "daily limit"}).encode())
                batch = f"batch-{len(service.batches) + 1}"
                service.batches[batch] = body
                port = self.server.server_address[1]
                urls = [f"http://127.0.0.1:{port}/upload/{batch}/{n}?{SIGNATURE}" for n in range(len(body["files"]))]
                self.reply(200, json.dumps({"code": 0, "msg": "ok", "data": {"batch_id": batch, "file_urls": urls}}).encode())

            def do_PUT(self):  # noqa: N802
                self.record()
                service.uploads[self.path.split("?")[0]] = self.rfile.read(int(self.headers["Content-Length"]))
                self.reply(200, b"")

            def do_GET(self):  # noqa: N802
                self.record()
                port = self.server.server_address[1]
                match = re.match(r"^/api/v4/extract-results/batch/([^/?]+)$", self.path)
                if match:
                    batch = match.group(1)
                    service.polls[batch] = service.polls.get(batch, 0) + 1
                    results = []
                    for n, spec in enumerate(service.batches[batch]["files"]):
                        entry = {"file_name": spec["name"], "data_id": spec["data_id"], "err_msg": ""}
                        if service.polls[batch] <= service.polls_until_done:
                            entry.update(state="running", extract_progress={"extracted_pages": 0, "total_pages": 1})
                        elif spec["name"].split(".")[0] in service.failing:
                            entry.update(state="failed", err_msg="文件读取失败")
                        else:
                            entry.update(state="done", full_zip_url=f"http://127.0.0.1:{port}/zip/{batch}/{n}")
                        results.append(entry)
                    return self.reply(200, json.dumps({"code": 0, "msg": "ok", "data": {"batch_id": batch, "extract_result": results}}).encode())
                match = re.match(r"^/zip/([^/]+)/(\d+)$", self.path)
                if match:
                    uploaded = service.uploads[f"/upload/{match.group(1)}/{match.group(2)}"]
                    pages = len(re.findall(rb"/Type\s*/Page(?![A-Za-z])", uploaded)) or 1
                    buffer = io.BytesIO()
                    with zipfile.ZipFile(buffer, "w") as archive:
                        archive.writestr("full.md", "".join(f"Cloud text of page {p + 1}, written only for a test.\n\n" for p in range(pages)) + "![](images/a.jpg)\n")
                        archive.writestr("images/a.jpg", b"\xff\xd8 synthetic")
                        archive.writestr("layout.json", json.dumps({"_backend": "pipeline", "pdf_info": [
                            {"page_idx": p, "para_blocks": [{"type": "text", "lines": [{"spans": [{"type": "text", "content": f"Cloud text of page {p + 1}, written only for a test."}]}]}],
                             "discarded_blocks": [{"type": "discarded", "lines": [{"spans": [{"type": "text", "content": "Running head"}]}]}]} for p in range(pages)]}))
                        archive.writestr("x_content_list.json", "[]")
                        archive.writestr("x_origin.pdf", uploaded)
                    return self.reply(200, buffer.getvalue(), "application/zip")
                self.reply(404, b"{}")

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def close(self) -> None:
        self.server.shutdown()
        self.server.server_close()


class CloudImportTests(WorkspaceTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.service = FakeService()
        self.addCleanup(self.service.close)
        self.privacy = self.root / "requirements" / "privacy.md"
        self.privacy.write_text("# 隐私与处理要求\n\n- 处理方式：云端，MinerU 官方服务 mineru.net\n- 范围：已发表的参考文献\n", encoding="utf-8")
        make_pdf(self.inputs / "a paper.pdf", 2)
        make_docx(self.inputs / "letter.docx")
        self.token = TOKEN
        self.timeout = "10"

    def cloud(self, *args: str) -> subprocess.CompletedProcess:
        env = {k: v for k, v in os.environ.items() if k.lower() not in ("http_proxy", "https_proxy", "all_proxy")}
        env.update(INGEST_MINERU_API_URL=self.service.url, INGEST_POLL_INTERVAL="0.01", INGEST_POLL_TIMEOUT=self.timeout,
                   NO_PROXY="127.0.0.1,localhost")
        env.pop("MINERU_API_TOKEN", None)
        if self.token:
            env["MINERU_API_TOKEN"] = self.token
        return subprocess.run([sys.executable, str(SCRIPTS / "ingest.py"), "--root", str(self.root), *args], capture_output=True,
                              text=True, encoding="utf-8", env=env, timeout=300)

    def test_refuses_without_a_confirmed_choice_or_a_token(self) -> None:
        self.privacy.write_text("# Privacy\n\nThe researcher wants cloud parsing; the scope is not confirmed yet.\n", encoding="utf-8")
        result = self.cloud("run", "--route", "cloud", str(self.inputs))
        self.assertEqual(result.returncode, 3)
        self.assertIn("names mineru.net", result.stdout)
        self.privacy.write_text("Processing: mineru.net, published papers only.\n", encoding="utf-8")
        self.token = ""
        result = self.cloud("run", "--route", "cloud", str(self.inputs))
        self.assertEqual(result.returncode, 3)
        self.assertIn("MINERU_API_TOKEN", result.stdout)
        self.assertEqual(self.service.requests, [])

    def test_uploads_converts_and_keeps_the_token_private(self) -> None:
        result = self.cloud("run", "--route", "cloud", str(self.inputs))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        record = self.record()
        # The live service is not verified yet, so every cloud result is flagged for review, and nothing else is.
        self.assertEqual({i["name"]: i["status"] for i in record["items"]}, {"a paper.pdf": "needs-review", "letter.docx": "needs-review"})
        api = [r for r in self.service.requests if r["path"].startswith("/api/")]
        transfers = [r for r in self.service.requests if not r["path"].startswith("/api/")]
        self.assertTrue(api and all(r["headers"].get("authorization") == f"Bearer {TOKEN}" for r in api))
        self.assertTrue(transfers and all("authorization" not in r["headers"] for r in transfers))
        self.assertTrue(all("content-type" not in r["headers"] for r in transfers if r["method"] == "PUT"))
        sent = self.service.batches["batch-1"]["files"]
        self.assertEqual(sorted(f["name"] for f in sent), sorted(f"{i['target']}{Path(i['name']).suffix}" for i in record["items"]))
        source_id = next(i["target"] for i in record["items"] if i["name"] == "a paper.pdf")
        folder = self.root / "references" / "extracted" / source_id
        provenance = json.loads((folder / "provenance.json").read_text(encoding="utf-8"))
        self.assertEqual(provenance["conversion"]["route"], "cloud")
        self.assertEqual(provenance["conversion"]["model_version"], "vlm")
        self.assertEqual({w["code"] for w in provenance["warnings"] if w["level"] != "info"}, {"unverified-format"})
        self.assertEqual((provenance["coverage"]["expected"], provenance["coverage"]["expected_from"], provenance["coverage"]["processed"]), (2, "file structure", 2))
        self.assertNotIn("x_origin.pdf", provenance["outputs"]["native"])
        self.assertIn("![](assets/a.jpg)", (folder / "document.md").read_text(encoding="utf-8"))
        for path in self.root.rglob("*"):
            if path.is_file():
                data = path.read_bytes()
                self.assertNotIn(TOKEN.encode(), data, path)
                self.assertNotIn(SIGNATURE.encode(), data, path)

    def test_an_expired_token_stops_the_batch_once(self) -> None:
        self.service.mode = "expired"
        result = self.cloud("run", "--route", "cloud", str(self.inputs))
        self.assertEqual(result.returncode, 2)
        record = self.record()
        self.assertEqual(record["stopped"]["code"], "token-expired")
        self.assertEqual({i["status"] for i in record["items"]}, {"pending"})
        self.assertEqual(len([r for r in self.service.requests if r["method"] == "POST"]), 1)

    def test_unfinished_work_is_collected_later_without_a_second_upload(self) -> None:
        self.service.polls_until_done, self.timeout = 10_000, "0.3"
        result = self.cloud("run", "--route", "cloud", str(self.inputs))
        self.assertEqual(result.returncode, 2, result.stdout)
        record = self.record()
        self.assertEqual({i["status"] for i in record["items"]}, {"submitted"})
        self.service.polls_until_done, self.timeout = 0, "10"
        resumed = self.cloud("run", "--import-id", record["import_id"])
        self.assertEqual(resumed.returncode, 0, resumed.stdout)
        self.assertEqual(len(self.service.uploads), 2)
        self.assertEqual(len([r for r in self.service.requests if r["method"] == "PUT"]), 2)

    def test_a_file_that_fails_at_the_service_fails_alone(self) -> None:
        make_pdf(self.inputs / "second.pdf", 1)
        self.service.failing = {"src-" + hashlib.sha256((self.inputs / "second.pdf").read_bytes()).hexdigest()[:12]}
        result = self.cloud("run", "--route", "cloud", str(self.inputs))
        self.assertEqual(result.returncode, 1)
        statuses = {i["name"]: i["status"] for i in self.record()["items"]}
        self.assertEqual(statuses["second.pdf"], "failed")
        self.assertEqual(statuses["a paper.pdf"], "needs-review")

    def test_only_the_official_address_or_this_computer_is_accepted(self) -> None:
        with self.assertRaises(ValueError):
            CloudRoute(TOKEN, base_url="http://example.com")
        with self.assertRaises(ValueError):
            CloudRoute(TOKEN, base_url="https://mineru.example.org")
        self.assertEqual(CloudRoute(TOKEN).base, "https://mineru.net")


if __name__ == "__main__":
    unittest.main()
