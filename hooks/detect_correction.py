#!/usr/bin/env python3
"""UserPromptSubmit hook: when a message reads like a correction, remind Claude to run neva-neva-neva.

Reads the hook event as JSON on stdin. Prints nothing for ordinary messages. Never blocks a message.
Set NEVA_QUIET=1 to turn it off.
"""
import json
import os
import re
import sys

# Phrases people use when they are correcting or repeating themselves.
PATTERNS = [
    r"\bi (?:already )?told you\b",
    r"\bi (?:already )?said\b(?! (?:hi|hello|thanks|thank you)\b)",
    r"\b(?:like|as) i said\b",
    r"\bhow many times\b",
    r"\byou keep\b",
    r"\byou always\b",
    r"\byou never\b",
    r"\bstop (?:doing|using|adding|writing|putting|saying|making)\b",
    r"\bfrom now on\b",
    r"\bgoing forward\b",
    r"\bnever (?:do|use|add|write|put|say|make|ever)\b",
    r"\bdon'?t (?:ever|do that again)\b",
    r"\bagain\s*[?!]",
    r"\bwhy did you\b",
    r"\bwhy do you keep\b",
    r"\bremember (?:to|that)\b",
    r"\bthat'?s (?:not what i (?:asked|said|wanted)|wrong again)\b",
]
REGEX = re.compile("|".join(PATTERNS), re.IGNORECASE)

REMINDER = (
    "[neva-neva-neva] This message may be a correction or a repeated instruction. If it is, use the "
    "neva-neva-neva skill before you go on: say the rule back in one line, check .claude/neva-neva-neva.md "
    "for repeats, write it into the strongest home that fits, and tell the user in one line where it "
    "went. If it is not a correction, ignore this note."
)


def is_correction(prompt: str) -> bool:
    return bool(prompt) and REGEX.search(prompt) is not None


def main() -> int:
    if os.environ.get("NEVA_QUIET") == "1":
        return 0
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    if is_correction(event.get("prompt") or ""):
        json.dump(
            {"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": REMINDER}},
            sys.stdout,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
