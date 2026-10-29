#!/usr/bin/env python3
"""CV screener.

Scores one or more CVs against a job description and returns an
evidence-based scorecard per candidate, plus the questions to ask on the
screening call. It's a first pass: the recruiter makes the call.

Usage:
    python cv_screener.py --jd examples/sample_jd.txt --cv examples/sample_cv.txt
    python cv_screener.py --jd examples/sample_jd.txt --cv cvs/ -o out/screening.md

Accepts .txt and .md CVs (export PDFs to text first).
"""

import argparse
from pathlib import Path

from common import ask_claude, read_text, write_output

SYSTEM = """You are an experienced technical recruiter doing a first-pass CV
screen. You are rigorous and fair.

Rules:
- Judge only job-relevant evidence: skills, scope, impact, seniority signals.
- Ignore name, age, gender, nationality, photos, marital status, university
  prestige and anything else not tied to doing the job.
- Every claim you make about a candidate must point to something in the CV.
  If the CV doesn't show it, say "not shown". Never assume or invent.
- Career gaps and short tenures are questions to ask, not red flags.
- Be direct. Recruiters read dozens of these a day."""

PROMPT = """Job description:
<jd>
{jd}
</jd>

Candidate CV ({name}):
<cv>
{cv}
</cv>

Write a scorecard in Markdown:

### {name}

**Recommendation:** Advance / Hold / Pass, with one sentence why.

**Fit score:** X/5

| Requirement | Met? | Evidence from CV |
|---|---|---|
(one row per must-have in the JD; Met? is Yes / Partial / Not shown)

**Strengths:** two or three bullets.

**Gaps to probe:** two or three bullets.

**Screening call questions:** five questions tailored to this candidate's
gaps and claims, not generic ones."""


def collect_cvs(path: str) -> list[Path]:
    target = Path(path)
    if target.is_dir():
        files = sorted(p for p in target.iterdir() if p.suffix.lower() in {".txt", ".md"})
        if not files:
            raise SystemExit(f"No .txt or .md CVs found in {path}")
        return files
    return [target]


def main() -> None:
    parser = argparse.ArgumentParser(description="Screen CVs against a job description.")
    parser.add_argument("--jd", required=True, help="Path to the job description")
    parser.add_argument("--cv", required=True, help="A CV file or a folder of CVs")
    parser.add_argument("-o", "--output", help="Save the report to this file")
    parser.add_argument("--dry-run", action="store_true", help="Print the prompts without calling the API")
    args = parser.parse_args()

    jd = read_text(args.jd)
    sections = ["# Screening report\n\n_AI-assisted first pass. The recruiter makes the final call._\n"]

    for cv_file in collect_cvs(args.cv):
        name = cv_file.stem.replace("_", " ").title()
        print(f"Screening {name}...")
        prompt = PROMPT.format(jd=jd, cv=read_text(str(cv_file)), name=name)
        sections.append(ask_claude(SYSTEM, prompt, dry_run=args.dry_run))

    write_output("\n\n---\n\n".join(sections), args.output)


if __name__ == "__main__":
    main()
