# Recruiting AI Toolkit

Three small command-line tools I use to speed up technical recruiting with Claude.
They handle the repetitive first pass so I can spend my time on the parts that need
judgment: calibrating with hiring managers, talking to candidates, closing.

Built by [Marcela Mengual](https://linkedin.com/in/marmengual), Engineering Talent Lead
hiring for US startups across Argentina, LATAM, the US and India.

## What's inside

| Tool | Input | Output |
|---|---|---|
| `jd_to_boolean.py` | A job description | LinkedIn Boolean, Google X-ray and GitHub search strings, title variations, and questions to calibrate with the hiring manager |
| `cv_screener.py` | A JD and one CV or a folder of CVs | An evidence-based scorecard per candidate, with tailored screening-call questions |
| `outreach_writer.py` | A candidate profile and a role | Personalized first messages from different angles, plus a follow-up, in English, Spanish or Portuguese |

## Setup

Python 3.10+ and an [Anthropic API key](https://console.anthropic.com). No packages to install.

```bash
git clone https://github.com/marmengualfalcon-boop/recruiting-ai-toolkit.git
cd recruiting-ai-toolkit
export ANTHROPIC_API_KEY=your_key
```

## Usage

**1. Turn a JD into a sourcing plan**

```bash
python jd_to_boolean.py examples/sample_jd.txt --market "Argentina, LATAM"
```

**2. Screen CVs against the JD**

```bash
python cv_screener.py --jd examples/sample_jd.txt --cv examples/sample_cv.txt
python cv_screener.py --jd jd.txt --cv cvs/ -o out/screening.md   # a whole folder
```

**3. Write outreach**

```bash
python outreach_writer.py --profile examples/sample_profile.txt --role examples/sample_jd.txt
python outreach_writer.py --profile p.txt --role jd.txt --lang es --channel email
```

Every tool accepts `-o file.md` to save the result and `--dry-run` to print the
prompt without calling the API, so you can read and adjust it.

## How I designed the prompts

- **No invented requirements.** If the JD is vague, the sourcing plan turns it into
  a question for the hiring manager instead of guessing.
- **Evidence or nothing.** The screener has to point to the CV for every claim and
  writes "not shown" when it can't. Gaps become questions, not rejections.
- **Fair by default.** The screener is told to ignore name, age, gender, nationality,
  photos and university prestige.
- **Outreach that sounds human.** One specific detail from the profile, a clear
  pitch, one small ask. No "rockstar", no emojis.
- **The recruiter decides.** These are first drafts and first passes.

## Privacy

Don't commit real CVs or candidate data. Keep them in a local folder listed in
`.gitignore` (`cvs/` and `out/` already are). The examples in this repo are fictional.

## License

MIT
