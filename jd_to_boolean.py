#!/usr/bin/env python3
"""JD -> sourcing plan.

Turns a job description into ready-to-paste search strings for LinkedIn,
Google X-ray and GitHub, plus the questions to clear up with the hiring
manager before sourcing starts.

Usage:
    python jd_to_boolean.py examples/sample_jd.txt --market "Argentina, LATAM"
    python jd_to_boolean.py examples/sample_jd.txt -o out/sourcing_plan.md
"""

import argparse

from common import ask_claude, read_text, write_output

SYSTEM = """You are a senior technical sourcer. You turn job descriptions into
precise, working search strings. You know how LinkedIn Boolean, Google X-ray
and GitHub search actually behave, and you keep strings short enough to paste
without hitting length limits. You never invent requirements that are not in
the job description; when something is ambiguous you flag it as a question for
the hiring manager instead of guessing."""

PROMPT = """Job description:
<jd>
{jd}
</jd>

Target market: {market}

Write a sourcing plan in Markdown with these sections:

## Role in one line
What this person will actually do, in plain words.

## Must-have vs nice-to-have
Two short lists. Only what the JD supports.

## Title variations
Real job titles people with this profile use on LinkedIn, including the
Spanish/Portuguese versions common in {market} when relevant.

## LinkedIn Boolean
Two strings: one narrow (high precision), one broad (high recall).
Use uppercase AND / OR / NOT and quotes for multi-word terms.

## Google X-ray
Two strings using site:linkedin.com/in, scoped to {market}.

## GitHub search
One or two queries using language:, location: and followers: qualifiers
where they help.

## Exclude
Terms to add with NOT to cut noise (e.g. intern, student, recruiter).

## Calibrate with the hiring manager
Three to five questions where the JD is vague or contradictory.

Keep it tight. No intro, no closing remarks."""


def main() -> None:
    parser = argparse.ArgumentParser(description="Turn a job description into search strings.")
    parser.add_argument("jd", help="Path to the job description (.txt or .md), or - for stdin")
    parser.add_argument("--market", default="Argentina and LATAM", help="Where you're sourcing")
    parser.add_argument("-o", "--output", help="Save the plan to this file")
    parser.add_argument("--dry-run", action="store_true", help="Print the prompt without calling the API")
    args = parser.parse_args()

    jd = read_text(args.jd)
    result = ask_claude(SYSTEM, PROMPT.format(jd=jd, market=args.market), dry_run=args.dry_run)
    write_output(result, args.output)


if __name__ == "__main__":
    main()
