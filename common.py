"""Shared helpers: one call to the Claude API using only the Python standard library."""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

API_URL = "https://api.anthropic.com/v1/messages"
DEFAULT_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5")


def ask_claude(system: str, prompt: str, max_tokens: int = 2500, dry_run: bool = False) -> str:
    """Send one prompt to Claude and return the text reply.

    With dry_run=True nothing is sent; the full prompt is returned so you can
    inspect or tweak it.
    """
    if dry_run:
        return f"--- SYSTEM ---\n{system}\n\n--- PROMPT ---\n{prompt}\n"

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("Missing ANTHROPIC_API_KEY. Run: export ANTHROPIC_API_KEY=your_key")

    body = json.dumps({
        "model": DEFAULT_MODEL,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")

    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            data = json.load(response)
    except urllib.error.HTTPError as err:
        sys.exit(f"API error {err.code}: {err.read().decode('utf-8', 'ignore')}")
    except urllib.error.URLError as err:
        sys.exit(f"Network error: {err.reason}")

    return "".join(block.get("text", "") for block in data.get("content", []) if block.get("type") == "text")


def read_text(path: str) -> str:
    """Read a text file, or stdin when path is '-'."""
    if path == "-":
        return sys.stdin.read()
    file = Path(path)
    if not file.exists():
        sys.exit(f"File not found: {path}")
    return file.read_text(encoding="utf-8")


def write_output(text: str, path: str | None) -> None:
    """Print the result, or save it when an output path is given."""
    if path:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(text, encoding="utf-8")
        print(f"Saved to {path}")
    else:
        print(text)
