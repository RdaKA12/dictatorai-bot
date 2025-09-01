"""
Moderation utilities for dictatorai-bot.

- Denylist regex check (hard block)
- Optional OpenAI moderation (when MODERATION=1)
- Fail-closed: if moderation is ON and external check errors, block.
"""

import os
import re
from typing import Tuple, List

from dotenv import load_dotenv

load_dotenv()

MODERATION_ON = os.getenv("MODERATION", "1") == "1"
MODERATION_MODEL = os.getenv("MODERATION_MODEL", "omni-moderation-latest")
BLOCKLIST_WORDS = [w.strip() for w in os.getenv("BLOCKLIST_WORDS", "").split(",") if w.strip()]

# Compile denylist pattern
_DENYLIST_PATTERNS: List[re.Pattern] = []
if BLOCKLIST_WORDS:
    pat = r"(" + r"|".join(re.escape(w) for w in BLOCKLIST_WORDS) + r")"
    _DENYLIST_PATTERNS.append(re.compile(pat, re.IGNORECASE))

# Try OpenAI client
try:
    from openai import OpenAI  # type: ignore
    _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
except Exception:
    _client = None

def _check_denylist(text: str) -> Tuple[bool, str]:
    for pattern in _DENYLIST_PATTERNS:
        if pattern.search(text or ""):
            return False, "Blocked by denylist pattern"
    return True, ""

def _check_openai(text: str) -> Tuple[bool, str]:
    if not _client:
        return False, "Moderation client not configured"
    try:
        # OpenAI moderations v1 style
        resp = _client.moderations.create(model=MODERATION_MODEL, input=text)  # type: ignore[attr-defined]
        if hasattr(resp, "results") and resp.results:
            res = resp.results[0]
            flagged = getattr(res, "flagged", False)
            if flagged:
                return False, "Flagged by model moderation"
        return True, ""
    except Exception as e:
        return False, f"Moderation API error: {e}"

def is_allowed(text: str) -> Tuple[bool, str]:
    """
    Returns (allowed, reason). reason is non-empty only when blocked.
    Fail-closed: if moderation is ON and the external check fails, we block.
    """
    ok, reason = _check_denylist(text)
    if not ok:
        return False, reason

    if MODERATION_ON:
        ok, reason = _check_openai(text)
        if not ok:
            return False, reason

    return True, ""
