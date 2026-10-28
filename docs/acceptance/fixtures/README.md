# Acceptance Fixtures

Generators for the synthetic, rights-cleared test material of the acceptance checklists. Every generated document says that it is a synthetic test document and contains no research results. Generate the material into a folder outside the test workspace, so that the agent under test receives it the way a researcher's files arrive.

- [`make_mvp2_fixtures.py`](make_mvp2_fixtures.py) builds the MVP 2 folder: a twelve-page report with a figure, a table, two formulas, two columns, and running headers; an exact duplicate with a non-ASCII, spaced name; a scanned page; a different file with the same name in a subfolder; a Word source with a heading, a table, and a figure; a Markdown file; a corrupt PDF; an unsupported format; a Word decision letter with comments and tracked changes; and a PDF reviewer report with annotations. It needs reportlab, Pillow, and python-docx, which the local MinerU environment provides: `.tools/mineru/bin/python docs/acceptance/fixtures/make_mvp2_fixtures.py OUTPUT_FOLDER`.

Only the template maintainer uses these generators. They are never copied into a researcher's workspace or a test copy.
