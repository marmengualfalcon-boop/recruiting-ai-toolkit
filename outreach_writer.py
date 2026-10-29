#!/usr/bin/env python3
"""Outreach writer.

Writes short, personalized outreach messages from a candidate's profile and
the role you're hiring for, in English, Spanish or Portuguese. Gives you a
few angles to pick from plus a follow-up.

Usage:
    python outreach_writer.py --profile examples/sample_profile.txt --role examples/sample_jd.txt
    python outreach_writer.py --profile p.txt --role jd.txt --lang es --channel email
"""

import argparse

from common import ask_claude, read_text, write_output

LANGUAGES = {"en": "English", "es": "Spanish (Rioplatense, using 'vos')", "pt": "Brazilian Portuguese"}

SYSTEM = """You write recruiting outreach that engineers actually answer.

Rules:
- Sound like a real person who read the profile, not a template.
- Open with one specific detail from the candidate's profile and why it
  connects to this role. One detail, not a list.
- Say what the role is and what makes it worth a look in plain words:
  the problem, the team, the stage, remote setup, pay currency if stated.
- End with one low-effort ask (a 15-minute call, or a reply).
- No flattery clichés ("impressive background", "rockstar", "ninja"),
  no "I hope this message finds you well", no emojis, no exclamation marks.
- Never invent facts about the candidate or the company."""

PROMPT = """Candidate profile:
<profile>
{profile}
</profile>

Role:
<role>
{role}
</role>

Channel: {channel}
Language: {language}

Write {variants} first-message variants, each taking a different angle
(for example: the technical problem, the team/stage, career growth).
Under each variant, add one line in italics naming the angle.

Length: {length}.
{subject_rule}

Then write one follow-up message to send 4-5 days later if there's no reply:
two or three sentences that add something new instead of "just bumping this".

Output Markdown only, no intro or closing remarks."""


def main() -> None:
    parser = argparse.ArgumentParser(description="Write personalized outreach messages.")
    parser.add_argument("--profile", required=True, help="Candidate profile text (LinkedIn/GitHub copy-paste)")
    parser.add_argument("--role", required=True, help="Job description or short role pitch")
    parser.add_argument("--lang", choices=LANGUAGES, default="en", help="Message language")
    parser.add_argument("--channel", choices=["linkedin", "email"], default="linkedin")
    parser.add_argument("--variants", type=int, default=3, help="How many first-message options")
    parser.add_argument("-o", "--output", help="Save the messages to this file")
    parser.add_argument("--dry-run", action="store_true", help="Print the prompt without calling the API")
    args = parser.parse_args()

    if args.channel == "email":
        length = "under 120 words"
        subject_rule = "Give each variant a subject line under 8 words."
    else:
        length = "under 80 words (LinkedIn InMail)"
        subject_rule = "No subject line."

    prompt = PROMPT.format(
        profile=read_text(args.profile),
        role=read_text(args.role),
        channel=args.channel,
        language=LANGUAGES[args.lang],
        variants=args.variants,
        length=length,
        subject_rule=subject_rule,
    )
    write_output(ask_claude(SYSTEM, prompt, max_tokens=1500, dry_run=args.dry_run), args.output)


if __name__ == "__main__":
    main()
