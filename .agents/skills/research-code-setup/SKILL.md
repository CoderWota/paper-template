---
name: research-code-setup
description: Use when the research needs code, data analysis, simulation, or other computation, when the researcher asks to set up an analysis environment or a code project, asks to run an analysis and record what it found, or asks which chart suits a result. Finds out the actual needs before creating code/, sets up a proportionate structure with its own environment, runs authorized analyses with recorded inputs, code version, parameters, and outputs, checks the results, and writes result records in research/results/ that keep proposed, observed, checked, and failed results distinct. Creates nothing for research that needs no code.
---

# Research code setup and runs

Outcome: when the research needs computation, a proportionate `code/` folder with its own environment and READMEs; each authorized analysis run with recorded provenance in `code/runs/<run-id>/`; and a result record in `research/results/` that links the inputs, method, parameters, run, outputs, checks, limitations, and the claims that use it.

## Step 1: Find out the needs before creating anything

1. Read `requirements/project.md`, `research/plan.md`, the active decisions in `research/decisions/index.md`, `research/results/index.md`, and `code/README.md` if it exists.
2. From the plan and the researcher, establish: the computation (analysis, simulation, data processing, or figures); the language and tools that the researcher uses or prefers; the data (where it is, its size, sensitivity, license, and whether it may be copied into the workspace or kept in version history); compute needs; existing code (reuse it where it lives; do not copy a large external repository); and reproducibility needs such as seeds and versions. Ask one question at a time, only for what the plan and the workspace do not answer.
3. If the research needs no code, create nothing and say so.
4. A data or material scope, sensitive data, a new external service, or a new cost is a major decision: ask first. Never upload research data to a service as part of this skill.

## Step 2: Set up proportionately

5. Create only the parts the work needs:

   ```text
   python scripts/research.py code-init --part src [--part data] [--part runs] [--part outputs] [--part notebooks] [--venv]
   ```

   It writes the README of each folder and keeps text that someone added outside its maintained block.
6. Research code gets its own environment, separate from `scripts/` and `.tools/`. `--venv` creates `code/.venv` with the current Python; use `environment-management` when a different interpreter or a consented installation is needed. Install packages with the research interpreter (`code/.venv/bin/python -m pip ...`, or `code\.venv\Scripts\python.exe` on Windows) and record the exact versions in `code/requirements.txt`. For R, Julia, or other tools, record the interpreter and package versions in `code/README.md`. Never install research packages into `.tools/` or the scripts' environment, and never change the document-conversion tools to suit research code.
7. Keep raw inputs unchanged in `code/data/raw/`, or reference data where it lives by path and checksum. Put generated data in `code/data/derived/`. For large or sensitive data, ask whether it may be kept in version history; add an ignore rule only after the answer.

## Step 3: Run with provenance

8. First run a small smoke task on clearly labeled test data to show that the environment works.
9. Run every analysis whose output may support a result through the recorder, from the workspace root:

   ```text
   python scripts/research.py run --name <short name> --note "<purpose>" --input <path> ... --output <path> ... [--code <path>] [--freeze] -- <command> <arguments>
   ```

   It records the command, a checksum of the code (by default `code/src`), the Git commit when there is one, the interpreter, the inputs and outputs with their checksums, the logs, and the exit status in `code/runs/<run-id>/`, and prints the input and output lines for the result record.
10. A chart of results is an output of a recorded run: choose its form with the [figure guide](figure-guide.md), keep the plotting code in `code/src`, and list the figure as an output of the run.
11. Investigate routine failures yourself: errors, missing packages, data problems. Ask the researcher only for what you cannot resolve, and say exactly what is needed.
    Keep the original run and logs. Try at most two repairs of a failing technical action within the confirmed method and permissions, stopping earlier when the same failure repeats without progress. Record the attempts and remaining blocker in the existing work item or result record. Use `--timeout` when a run needs a duration bound. A valid negative result is not a technical failure; do not alter parameters or select runs to obtain a preferred conclusion.
12. Stay inside the confirmed method and scope. Changing the method, the data scope, or a parameter that affects the conclusions, or excluding an analysis, is a major decision.

## Step 4: Check and record the results

13. Check each result with methods that suit the work: run it again and compare, compare with a reference result or a known case, test sensitivity to parameters or seeds, look for counterexamples, or compare with the sources. Your own judgment of plausibility, or agreement between two models, is not a check. Record failed checks too.
14. Write `research/results/<result-id>.md` with the layout in `research/results/README.md`, and add it to `research/results/index.md`. Copy the input, output, and run lines that the recorder printed. Use the status that matches what was done: observed before checks, checked only after the listed checks. The researcher's review is a separate line.
15. Never invent data, numbers, or results, and never select favorable runs silently: report every run that bears on a conclusion, including failed and negative ones.
16. Run `python scripts/research.py check`. A result reported as stale (its inputs or outputs changed) supports no claim until it is run and checked again.

## Interpret and hand off

- Explain the observed result separately from its interpretation and any untested hypothesis. Link the actual output and checks, retain negative findings, and state what the design can and cannot establish.
- If the result contradicts expectations, inspect calculation, data handling, and the agreed checks first. Present the evidence for keeping, narrowing, or abandoning the explanation where warranted; changing the scientific method or main claim needs the researcher's choice.
- Populate `Used by` with the manuscript passages, figures, tables, or checks that rely on the result. When an input, output, or recorded code version changes, list those dependents for rechecking; do not silently rewrite them or update checksums to make an old result appear current. State explicitly when the recorded dependency list is incomplete.
- Hand checked results and their limits to writing that is already in scope. Otherwise deliver the result and the one useful next check or judgment, without starting an unsolicited manuscript.

## Completion check

- `code/` exists only because the research needs computation, with only the parts the work uses, each with its README.
- The research environment is separate from the workspace tools, and its package versions are recorded.
- Every reported result has a run record or a described procedure, inputs and outputs with checksums, the checks made, and its limitations.
- Statuses match what was actually done, failed and negative results that matter are kept, and nothing was invented.
- `python scripts/research.py check` reports no problem and no stale result for the results you report.
