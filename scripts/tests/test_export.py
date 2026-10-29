"""Tests for scripts/export.py and scripts/export/: reference documents, DOCX checks, builds, and releases.

The unit tests build small Word packages by hand and need no external tool. The integration tests run Pandoc and
pandoc-crossref from the workspace's .tools/ folder (or PATH) and are skipped where they are not installed; the
diagram test also needs mermaid-cli and a Chrome-family browser. They prove the build and its checks on this
computer, not Word's rendering, which is inspected separately.
"""

from __future__ import annotations

import json
import os
import runpy
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parent.parent
REPOSITORY = SCRIPTS.parent
EXPORT = SCRIPTS / "export.py"
sys.path.insert(0, str(SCRIPTS))

from export import docx, tools  # noqa: E402

VERIFY = runpy.run_path(str(EXPORT))["verify"]

W_NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math"'
STYLES = (f'<w:styles {W_NS}><w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:asciiTheme="minorHAnsi" w:eastAsiaTheme="minorEastAsia" '
          'w:hAnsiTheme="minorHAnsi" w:cstheme="minorBidi" /><w:sz w:val="24" /><w:szCs w:val="24" /></w:rPr></w:rPrDefault>'
          '<w:pPrDefault><w:pPr><w:spacing w:after="200" /></w:pPr></w:pPrDefault></w:docDefaults>'
          '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal" /></w:style>'
          '<w:style w:type="paragraph" w:styleId="BodyText"><w:name w:val="Body Text" /><w:basedOn w:val="Normal" /><w:pPr><w:spacing w:before="180" w:after="180" /></w:pPr></w:style>'
          '<w:style w:type="paragraph" w:styleId="Compact"><w:name w:val="Compact" /><w:basedOn w:val="BodyText" /><w:pPr><w:spacing w:before="36" w:after="36" /></w:pPr></w:style>'
          '<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1" /><w:rPr><w:rFonts w:asciiTheme="majorHAnsi" w:hAnsiTheme="majorHAnsi" />'
          '<w:color w:val="0F4761" w:themeColor="accent1" /></w:rPr></w:style></w:styles>')
DOCUMENT = f'<w:document {W_NS}><w:body><w:p /><w:sectPr><w:footnotePr><w:numRestart w:val="eachSect" /></w:footnotePr></w:sectPr></w:body></w:document>'


CORE = ('<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
        'xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:title>A study</dc:title><cp:keywords>{keywords}</cp:keywords></cp:coreProperties>')


def make_package(path: Path, document: str = DOCUMENT, styles: str = STYLES, footnotes: str | None = None, core: str | None = None) -> Path:
    with zipfile.ZipFile(path, "w") as package:
        package.writestr("[Content_Types].xml", '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"/>')
        package.writestr("word/document.xml", document)
        package.writestr("word/styles.xml", styles)
        if footnotes:
            package.writestr("word/footnotes.xml", footnotes)
        if core:
            package.writestr("docProps/core.xml", core)
    return path


def omml(inner: str, display: bool = False) -> str:
    math = f"<m:oMath>{inner}</m:oMath>"
    return f"<w:p>{'<m:oMathPara>' + math + '</m:oMathPara>' if display else math}</w:p>"


FRACTION = "<m:f><m:num><m:r><m:t>1</m:t></m:r></m:num><m:den><m:r><m:t>n</m:t></m:r></m:den></m:f>"


class ToolDiscoveryTests(unittest.TestCase):
    def test_windows_installations_use_environment_roots(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            browser = base / "Google/Chrome/Application/chrome.exe"
            word = base / "Microsoft Office/root/Office16/WINWORD.EXE"
            for path in (browser, word):
                path.parent.mkdir(parents=True)
                path.touch()
            with mock.patch.object(tools, "system", return_value="windows"), mock.patch.dict(
                    os.environ, {"ProgramFiles": str(base)}, clear=True):
                self.assertEqual(tools.browser(), str(browser))
                self.assertTrue(tools.word_available())

    def test_browser_can_use_an_explicit_puppeteer_path(self) -> None:
        with tempfile.NamedTemporaryFile() as browser:
            with mock.patch.dict(os.environ, {"PUPPETEER_EXECUTABLE_PATH": browser.name}):
                self.assertEqual(tools.browser(), browser.name)

    def test_numeric_release_order_and_non_executable_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for version in ("9.9", "10.2", "10.10"):
                path = root / ".tools" / "pandoc" / version / "bin" / "pandoc"
                path.parent.mkdir(parents=True)
                path.write_text("fixture", encoding="utf-8")
                path.chmod(0o755)
            with mock.patch.object(tools, "system", return_value="linux"):
                self.assertIn("10.10", str(tools.find_in_tools(root, "pandoc", "pandoc")))
                with mock.patch.object(tools.os, "access", return_value=False):
                    self.assertIsNone(tools.find_in_tools(root, "pandoc", "pandoc"))


class ReferenceDocTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Path(tempfile.mkdtemp(prefix="export test ä "))
        self.addCleanup(shutil.rmtree, self.base, ignore_errors=True)

    def test_final_docx_signature_check_covers_headers_and_author_properties(self) -> None:
        output = make_package(self.base / "signature.docx", core=CORE.format(keywords=""))
        with zipfile.ZipFile(output, "a") as package:
            package.writestr("word/header1.xml", f'<w:hdr {W_NS}><w:p><w:r><w:t>Generated by </w:t></w:r>'
                              '<w:r><w:t>ChatGPT</w:t></w:r></w:p></w:hdr>')
        facts = {"body": [], "notes": [], "mermaid_code": 0, "todo": 0}
        check = next(item for item in VERIFY(self.base, {}, output, facts, [], []) if item[0] == "AI signatures")
        self.assertFalse(check[1])
        self.assertIn("header1.xml", check[2])
        output = make_package(self.base / "author.docx", core=CORE.format(keywords="").replace(
            "</cp:coreProperties>", "<dc:creator>Claude</dc:creator></cp:coreProperties>"))
        check = next(item for item in VERIFY(self.base, {}, output, facts, [], []) if item[0] == "AI signatures")
        self.assertFalse(check[1])
        self.assertIn("creator", check[2])

    def test_final_docx_open_item_check_uses_shared_multilingual_rules(self) -> None:
        output = make_package(self.base / "open-item.docx", core=CORE.format(keywords=""))
        with zipfile.ZipFile(output, "a") as package:
            package.writestr("word/footer1.xml", f'<w:ftr {W_NS}><w:p><w:r><w:t>（要確認：补充实验）</w:t></w:r></w:p></w:ftr>')
        facts = {"body": [], "notes": [], "mermaid_code": 0, "todo": 0}
        check = next(item for item in VERIFY(self.base, {}, output, facts, [], []) if item[0] == "open items")
        self.assertFalse(check[1])
        self.assertIn("1 open marker", check[2])

    def test_settings_are_applied_and_section_children_keep_schema_order(self) -> None:
        source = make_package(self.base / "default.docx")
        target = self.base / "templates" / "reference.docx"
        applied = docx.build_reference_doc(source, target, {
            "page": "A4", "margins_cm": "2.5", "font": "Times New Roman", "east_asian_font": "SimSun", "size_pt": "12",
            "line_spacing": "double", "space_after_pt": "0", "table_line_spacing": "single", "heading_font": "Times New Roman",
            "heading_color": "black", "line_numbers": True})
        self.assertIn("A4 pages", applied)
        with zipfile.ZipFile(target) as package:
            document = package.read("word/document.xml").decode()
            styles = package.read("word/styles.xml").decode()
        section = document[document.index("<w:sectPr"):]
        self.assertLess(section.index("footnotePr"), section.index("pgSz"))
        self.assertLess(section.index("pgSz"), section.index("pgMar"))
        self.assertLess(section.index("pgMar"), section.index("lnNumType"))
        self.assertIn('w:ascii="Times New Roman"', styles)
        self.assertIn('w:eastAsia="SimSun"', styles)
        self.assertIn('<w:color w:val="000000" />', styles)
        facts = docx.layout(target)
        self.assertEqual(facts["page"], "A4")
        self.assertEqual(facts["margins_cm"], [2.5])
        self.assertTrue(facts["line_numbers"])
        self.assertEqual(facts["font"], "Times New Roman")
        self.assertEqual(facts["size_pt"], 12)
        self.assertEqual(facts["line_spacing"], "double")

    def test_untouched_settings_keep_the_defaults(self) -> None:
        source = make_package(self.base / "default.docx")
        target = self.base / "reference.docx"
        self.assertEqual(docx.build_reference_doc(source, target, {}), [])
        facts = docx.layout(target)
        self.assertEqual(facts["line_spacing"], "single")
        self.assertFalse(facts["line_numbers"])


class FormulaCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Path(tempfile.mkdtemp(prefix="export test ä "))
        self.addCleanup(shutil.rmtree, self.base, ignore_errors=True)

    def package(self, body: str, footnote: str = "") -> Path:
        footnotes = f'<w:footnotes {W_NS}><w:footnote>{footnote}</w:footnote></w:footnotes>' if footnote else None
        return make_package(self.base / "built.docx", f'<w:document {W_NS}><w:body>{body}<w:sectPr /></w:body></w:document>', footnotes=footnotes)

    def test_matching_formulas_pass(self) -> None:
        built = self.package(omml(FRACTION) + omml("<m:r><m:t>x</m:t></m:r>", display=True), omml("<m:r><m:t>a</m:t></m:r>"))
        facts = {"body": [{"display": False, "tex": "\\frac{1}{n}"}, {"display": True, "tex": "x"}], "notes": [{"display": False, "tex": "a"}]}
        self.assertEqual(docx.compare_formulas(facts, docx.omml_objects(built)), [])

    def test_missing_structure_unparsed_latex_placement_and_count_are_reported(self) -> None:
        built = self.package(omml("<m:r><m:t>1/n</m:t></m:r>") + omml("<m:r><m:t>\\sqrt{2}</m:t></m:r>"))
        facts = {"body": [{"display": False, "tex": "\\frac{1}{n}"}, {"display": True, "tex": "\\sqrt{2}"},
                          {"display": False, "tex": "y"}], "notes": []}
        problems = "\n".join(docx.compare_formulas(facts, docx.omml_objects(built)))
        self.assertIn("3 formula(s) in the body of the source, but 2 native equation(s)", problems)
        self.assertIn("lacks m:f", problems)
        self.assertIn("display and inline placement differ", problems)
        self.assertIn("unconverted LaTeX", problems)

    def test_ast_facts_count_formulas_figures_diagrams_and_open_items(self) -> None:
        ast = {"blocks": [{"t": "Para", "c": [{"t": "Math", "c": [{"t": "InlineMath"}, "x"]}, {"t": "Note", "c": [
            {"t": "Para", "c": [{"t": "Math", "c": [{"t": "InlineMath"}, "y"]}]}]}, {"t": "Str", "c": "[TODO:"}]},
            {"t": "Figure", "c": []}, {"t": "CodeBlock", "c": [["", ["mermaid"], []], "flowchart LR"]}]}
        facts = docx.ast_facts(ast)
        self.assertEqual((len(facts["body"]), len(facts["notes"]), facts["figures"], facts["mermaid_code"], facts["todo"]), (1, 1, 1, 1, 1))

    def test_the_front_matter_is_read_from_the_metadata_of_the_ast(self) -> None:
        def inlines(*words):
            parts = []
            for word in words:
                parts += ([{"t": "Space"}] if parts else []) + [{"t": "Str", "c": word}]
            return {"t": "MetaInlines", "c": parts}

        title = {"t": "MetaInlines", "c": [{"t": "Str", "c": "A"}, {"t": "Space"}, {"t": "Quoted", "c": [{"t": "DoubleQuote"}, [{"t": "Str", "c": "quoted"}]]},
                                           {"t": "Space"}, {"t": "Str", "c": "study"}]}
        authors = {"t": "MetaList", "c": [inlines("Test", "Author"), {"t": "MetaMap", "c": {"name": inlines("Second", "Author")}}]}
        keywords = {"t": "MetaList", "c": [inlines("urban", "heat"), inlines("城市热岛")]}
        self.assertEqual(docx.front_matter({"meta": {"title": title, "author": authors, "keywords": keywords}}),
                         {"title": "A quoted study", "authors": ["Test Author", "Second Author"], "keywords": ["urban heat", "城市热岛"]})
        self.assertEqual(docx.front_matter({"meta": {}}), {"title": "", "authors": [], "keywords": []})
        self.assertEqual(docx.front_matter({"meta": {"author": inlines()}})["authors"], [])

    def test_declared_front_matter_that_the_word_file_lacks_is_reported(self) -> None:
        body = "<w:p><w:r><w:t>A “quoted” study – 城市热岛</w:t></w:r></w:p><w:p><w:r><w:t>Test Author</w:t></w:r></w:p>"
        built = make_package(self.base / "front.docx", f'<w:document {W_NS}><w:body>{body}<w:sectPr /></w:body></w:document>',
                             core=CORE.format(keywords="urban heat, 城市热岛"))
        declared = {"title": "A quoted study – 城市热岛", "authors": ["Test Author"], "keywords": ["urban heat", "城市热岛"]}
        self.assertEqual(docx.compare_front_matter(declared, built), ([], ["the title", "1 author(s)", "2 keyword(s)"]))
        problems, found = docx.compare_front_matter({"title": "Another title", "authors": ["Test Author", "Second Author"],
                                                     "keywords": ["urban heat", "remote sensing"]}, built)
        self.assertEqual(found, [])
        self.assertEqual(problems, ["the title “Another title” is not in the Word file", "author(s) not in the Word file: Second Author",
                                    "keyword(s) not in the Word file: remote sensing"])
        self.assertEqual(docx.compare_front_matter({}, built), ([], []))
        bare = make_package(self.base / "bare.docx", f'<w:document {W_NS}><w:body><w:p><w:r><w:t>Keywords: remote sensing</w:t></w:r></w:p><w:sectPr /></w:body></w:document>')
        self.assertEqual(docx.compare_front_matter({"keywords": ["remote sensing", "urban heat"]}, bare)[0], ["keyword(s) not in the Word file: urban heat"])


class ReleaseTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Path(tempfile.mkdtemp(prefix="export test ä "))
        self.addCleanup(self.cleanup)
        self.root = self.base / "论文 workspace"
        self.preview = self.root / "outputs" / "preview" / "journal"
        self.preview.mkdir(parents=True)
        (self.root / "manuscript").mkdir()
        (self.root / "manuscript" / "01-intro.md").write_text("# Intro\n", encoding="utf-8")
        self.output = make_package(self.preview / "manuscript.docx")

    def cleanup(self) -> None:
        for path in self.base.rglob("*"):
            if path.is_file():
                os.chmod(path, stat.S_IWUSR | stat.S_IRUSR)
        shutil.rmtree(self.base, ignore_errors=True)

    def record(self, status: str = "passed", open_items: int = 0) -> None:
        import hashlib
        digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()  # noqa: E731
        checks = [{"name": "native equations", "passed": True, "detail": "ok"},
                  {"name": "open items", "passed": open_items == 0, "detail": f"{open_items} [TODO: ...] marker(s) in the text"}]
        (self.preview / "build.json").write_text(json.dumps({
            "schema": "paper-template.build/1", "profile": "journal", "built": "2026-10-29T10:00:00", "status": status,
            "inputs": [{"path": "manuscript/01-intro.md", "sha256": digest(self.root / "manuscript" / "01-intro.md")}],
            "tools": {}, "command": [], "warnings": [], "checks": checks,
            "output": {"file": "manuscript.docx", "sha256": digest(self.output)}}), encoding="utf-8")

    def run_export(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(EXPORT), "--root", str(self.root), *args], capture_output=True, text=True,
                              encoding="utf-8", timeout=120)

    def test_a_current_passing_build_is_frozen_once(self) -> None:
        self.record()
        released = self.run_export("release", "--profile", "journal", "--id", "2026-11-round-1")
        self.assertEqual(released.returncode, 0, released.stdout)
        folder = self.root / "outputs" / "releases" / "2026-11-round-1"
        record = json.loads((folder / "release.json").read_text(encoding="utf-8"))
        self.assertEqual([f["file"] for f in record["files"]], ["manuscript.docx"])
        self.assertTrue((folder / "README.md").is_file())
        self.assertFalse(os.access(folder / "manuscript.docx", os.W_OK))
        again = self.run_export("release", "--profile", "journal", "--id", "2026-11-round-1")
        self.assertIn("never overwritten", again.stdout)

    def test_failed_stale_or_unfinished_builds_are_not_released(self) -> None:
        self.record(status="failed")
        self.assertIn("did not pass", self.run_export("release", "--profile", "journal", "--id", "r1").stdout)
        self.record(open_items=2)
        refused = self.run_export("release", "--profile", "journal", "--id", "r1")
        self.assertIn("2 [TODO: ...] marker(s)", refused.stdout)
        self.assertEqual(self.run_export("release", "--profile", "journal", "--id", "r1", "--allow-open-items").returncode, 0)
        self.record()
        (self.root / "manuscript" / "01-intro.md").write_text("# Intro\n\nChanged.\n", encoding="utf-8")
        stale = self.run_export("release", "--profile", "journal", "--id", "r2")
        self.assertIn("out of date (manuscript/01-intro.md changed)", stale.stdout)
        self.assertEqual(self.run_export("release", "--profile", "journal", "--id", "Bad ID").returncode, 3)


INFO = tools.find(REPOSITORY)
HAVE_PANDOC = bool(INFO["pandoc"] and INFO["crossref"]) and not tools.problems(INFO, False)


@unittest.skipUnless(HAVE_PANDOC, "Pandoc and pandoc-crossref are not installed")
class BuildTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base = Path(tempfile.mkdtemp(prefix="export build ä "))
        self.addCleanup(shutil.rmtree, self.base, ignore_errors=True)
        self.root = self.base / "论文 workspace"
        (self.root / "manuscript" / "assets").mkdir(parents=True)
        (self.root / "references").mkdir()
        if (REPOSITORY / ".tools").is_dir():
            os.symlink(REPOSITORY / ".tools", self.root / ".tools")
        self.write("manuscript/manifest.yaml", "version: 1\nmetadata: metadata.yaml\nsections:\n  - 01-main.md\n")
        self.write("manuscript/metadata.yaml", "title: \"Build test\"\nauthor:\n  - Test Author\n")
        self.write("references/bibliography.bib", "@book{zhang2019fixture,\n  title = {Fixtures}, author = {Zhang, Wei}, year = {2019}\n}\n")
        self.write("manuscript/01-main.md", "# Main section\n\nWe cite @zhang2019fixture and refer to @eq:mean and @sec:main-section.\n\n"
                   "$$\n\\hat{\\mu} = \\frac{1}{n}\\sum_{i=1}^{n} x_i\n$$\n\n{#eq:mean}\n\nInline $\\sqrt{x}$ and 中文。\n")

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def run_export(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(EXPORT), "--root", str(self.root), *args], capture_output=True, text=True,
                              encoding="utf-8", timeout=300)

    def test_a_profile_build_passes_its_checks_and_records_its_inputs(self) -> None:
        self.assertEqual(self.run_export("profile-init", "--id", "neutral", "--name", "Neutral").returncode, 0)
        self.assertEqual(self.run_export("reference-doc", "--profile", "neutral", "--page", "A4", "--line-spacing", "double").returncode, 0)
        with open(self.root / "requirements/profiles/neutral/profile.yaml", "a", encoding="utf-8") as stream:
            stream.write("expect_page: A4\nexpect_line_spacing: double\nexpect_anonymized: true\nanonymize: true\n")
        built = self.run_export("build", "--profile", "neutral")
        self.assertEqual(built.returncode, 0, built.stdout)
        self.assertIn("[pass] native equations: 2 formula(s)", built.stdout)
        self.assertIn("[pass] page: expected A4, found A4", built.stdout)
        self.assertIn("[pass] anonymization", built.stdout)
        record = json.loads((self.root / "outputs/preview/neutral/build.json").read_text(encoding="utf-8"))
        self.assertIn("manuscript/01-main.md", [i["path"] for i in record["inputs"]])
        self.assertEqual(record["tools"]["pandoc"], INFO["pandoc_version"])
        self.assertNotIn("Test Author", docx.text_of(self.root / "outputs/preview/neutral/manuscript.docx"))
        self.assertEqual(self.run_export("verify", "--profile", "neutral").returncode, 0)

    def test_the_metadata_file_is_used_without_a_manifest_line(self) -> None:
        self.write("manuscript/manifest.yaml", "version: 1\nsections:\n  - 01-main.md\n")
        self.write("manuscript/metadata.yaml", "title: \"A study of heat -- 城市热岛\"\nauthor:\n  - Test Author\nkeywords: [urban heat, remote sensing]\n")
        self.run_export("profile-init", "--id", "neutral", "--name", "Neutral")
        built = self.run_export("build", "--profile", "neutral")
        self.assertEqual(built.returncode, 0, built.stdout)
        self.assertIn("[pass] front matter: in the Word file, from the manuscript metadata: the title, 1 author(s), 2 keyword(s)", built.stdout)
        output = self.root / "outputs/preview/neutral/manuscript.docx"
        self.assertIn("城市热岛", docx.text_of(output))
        self.assertIn("Test Author", docx.text_of(output))
        self.assertEqual(docx.core_properties(output)["keywords"], "urban heat, remote sensing")
        record = json.loads((self.root / "outputs/preview/neutral/build.json").read_text(encoding="utf-8"))
        self.assertIn("manuscript/metadata.yaml", [item["path"] for item in record["inputs"]])
        self.assertEqual(self.run_export("verify", "--profile", "neutral").returncode, 0)
        self.write("manuscript/metadata.yaml", "title: \"Another title\"\n")
        self.assertIn("out of date because these changed: manuscript/metadata.yaml", self.run_export("verify", "--profile", "neutral").stdout)

    def test_an_author_that_the_word_writer_leaves_out_fails_the_front_matter_check(self) -> None:
        # Pandoc 3.12.1 shows an author written as a mapping (name:, affiliation:) nowhere in a Word file.
        self.write("manuscript/metadata.yaml", "title: \"Build test\"\nauthor:\n  - Test Author\n  - name: Second Author\n    affiliation: Somewhere\n")
        self.run_export("profile-init", "--id", "neutral", "--name", "Neutral")
        built = self.run_export("build", "--profile", "neutral")
        self.assertEqual(built.returncode, 1, built.stdout)
        self.assertIn("[FAIL] front matter: author(s) not in the Word file: Second Author", built.stdout)
        record = json.loads((self.root / "outputs/preview/neutral/build.json").read_text(encoding="utf-8"))
        self.assertEqual(record["status"], "failed")

    def test_a_manuscript_without_metadata_builds_and_says_that_it_has_no_title(self) -> None:
        self.write("manuscript/manifest.yaml", "version: 1\nsections:\n  - 01-main.md\n")
        (self.root / "manuscript" / "metadata.yaml").unlink()
        self.run_export("profile-init", "--id", "neutral", "--name", "Neutral")
        built = self.run_export("build", "--profile", "neutral")
        self.assertEqual(built.returncode, 0, built.stdout)
        self.assertIn("[pass] front matter: the manuscript metadata declares no title, authors, or keywords, so the Word file has none", built.stdout)

    def test_a_manuscript_with_problems_is_not_built(self) -> None:
        self.run_export("profile-init", "--id", "neutral", "--name", "Neutral")
        self.write("manuscript/01-main.md", "# Main\n\nWe cite @missing2020.\n")
        refused = self.run_export("build", "--profile", "neutral")
        self.assertEqual(refused.returncode, 3)
        self.assertIn("the manuscript check reports 1 problem(s)", refused.stdout)

    def test_ai_signature_prevents_docx_build(self) -> None:
        self.run_export("profile-init", "--id", "neutral", "--name", "Neutral")
        self.write("manuscript/01-main.md", "# Main\n\nSynthetic manuscript.\n\nGenerated by ChatGPT\n")
        refused = self.run_export("build", "--profile", "neutral")
        self.assertEqual(refused.returncode, 3, refused.stdout)
        self.assertFalse((self.root / "outputs/preview/neutral/manuscript.docx").exists())

    @unittest.skipUnless(INFO["mmdc"] and INFO["browser"], "mermaid-cli or a browser is missing")
    def test_a_diagram_becomes_a_numbered_figure(self) -> None:
        self.run_export("profile-init", "--id", "neutral", "--name", "Neutral")
        self.write("manuscript/01-main.md", "# Main\n\nSee @fig:flow.\n\n```mermaid\nflowchart LR\n    A[\"阅读\"] --> B[\"Write\"]\n```\n\n: The flow. {#fig:flow}\n")
        built = self.run_export("build", "--profile", "neutral")
        self.assertEqual(built.returncode, 0, built.stdout)
        self.assertIn("[pass] figures: 1 image(s) in the source, 1 in the Word file", built.stdout)
        self.assertEqual(len(list((self.root / "outputs/preview/neutral/figures").glob("*.png"))), 1)


if __name__ == "__main__":
    unittest.main()
