# ====================ORG_BUILD_NOTES====================
"""The Build Notes tab: a markdown file loaded at runtime, not code.

Every build carries a final tab called **Build Notes**, rendered from
`app/<SHORT_CODE>__readme.md` — the same prefix as the application file, so the
two travel together and neither can be shipped without the other being obvious
by its absence.

It is a **loaded reference, not part of the code**. The markdown is read from
disk and rendered, never embedded as a string literal in the `.py`. Three
reasons that matters:

  * It can be edited, reviewed and diffed as prose, by someone who is not
    reading Python.
  * It is the same file a reader can open in the repository, so the tab and the
    repository cannot drift apart.
  * A 300-line string literal in the middle of an application file makes every
    other function harder to find.

The tab exists to show **the concept of flipping the data team** — building from
the business outcome backwards to the data, rather than modelling the data and
hoping a useful application falls out. Its heading says so.

**It is published.** It renders in a public application and ships in a public
repository, so it must carry no personal or machine-specific detail: no email
address, no absolute local path, no machine or user name. `scan_for_pii()`
enforces that at build time; run it before publishing.

    python org_build_notes.py app/my_platform__readme.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

BUILD_NOTES_SUFFIX = "__readme.md"

TAB_LABEL = "📓 Build Notes"

REQUIRED_HEADING = "Flipping the Data Team"


# ====================PII_GATE====================
# Each pattern is something that must not reach a published page. The message
# says what to write instead — "remove it" without a replacement is how these
# get argued away at build time.
PII_PATTERNS: list[tuple[str, str, str]] = [
    (
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        "email address",
        "name the organisation instead of a person — \"Celnic Consulting\".",
    ),
    (
        r"(?i)\b[a-z]:[\\/][^\s`'\"|)]*",
        "absolute local path",
        "use the repository-relative path — `scripts/05_stage.py`, not a drive letter.",
    ),
    (
        r"(?i)\b(?:c:\\users|/home/|/users/)[^\s`'\"|)]*",
        "user home directory",
        "use a repository-relative path.",
    ),
    (
        r"(?i)\\\\[a-z0-9._-]+\\[^\s`'\"|)]*",
        "UNC network path",
        "describe the location in words.",
    ),
    (
        r"(?i)\bphase\s+(?:one|two|three|1|2|3)\b",
        "phase reference",
        "describe the step by what it does — \"the staging layer\", not \"Phase Two\".",
    ),
]


def scan_for_pii(text: str) -> list[tuple[int, str, str, str]]:
    """Find anything that must not be published. Returns (line, kind, match, fix).

    Runs line by line so the report points at somewhere editable.
    """
    findings: list[tuple[int, str, str, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern, kind, fix in PII_PATTERNS:
            for m in re.finditer(pattern, line):
                findings.append((lineno, kind, m.group(0), fix))
    return findings


def check_build_notes(path: str | Path) -> list[str]:
    """Build-time gate. Returns a list of problems; empty means publishable."""
    p = Path(path)
    problems: list[str] = []

    if not p.exists():
        return [f"{p} does not exist — every build carries a Build Notes file."]
    if not p.name.endswith(BUILD_NOTES_SUFFIX):
        problems.append(
            f"{p.name} must end with {BUILD_NOTES_SUFFIX} and share the "
            "application file's prefix."
        )

    text = p.read_text(encoding="utf-8")

    first_heading = next(
        (ln for ln in text.splitlines() if ln.startswith("# ")), ""
    )
    if REQUIRED_HEADING.lower() not in first_heading.lower():
        problems.append(
            f"the first heading must name \"{REQUIRED_HEADING}\" — the tab exists "
            f"to show that concept. Found: {first_heading!r}"
        )

    for lineno, kind, match, fix in scan_for_pii(text):
        problems.append(f"line {lineno}: {kind} {match!r} — {fix}")

    return problems


# ====================APP_SIDE====================
def notes_path(app_file: str | Path) -> Path:
    """The Build Notes file beside an application file.

    `app/my_platform.py` -> `app/my_platform__readme.md`
    """
    p = Path(app_file)
    return p.with_name(p.stem + BUILD_NOTES_SUFFIX)


def notes_fingerprint(path: str | Path) -> tuple | None:
    """Size and mtime, used as a cache key.

    Same reasoning as the DuckDB extract: Community Cloud hot-reloads on a push
    without clearing caches, so without a fingerprint the tab keeps rendering
    the notes as they were before the pull.
    """
    p = Path(path)
    if not p.exists():
        return None
    s = p.stat()
    return (str(p), s.st_size, int(s.st_mtime))


def load_build_notes(path: str | Path, fingerprint=None) -> str:
    """Read the notes. `fingerprint` is the cache key, not used for reading.

    Wrap this in `@st.cache_data` in the application and pass
    `notes_fingerprint(path)`.
    """
    p = Path(path)
    if not p.exists():
        return (
            "Build notes are not available in this deployment. They live in "
            "`app/` in the repository, alongside the application file."
        )
    return p.read_text(encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        raise SystemExit(2)
    issues = check_build_notes(sys.argv[1])
    if issues:
        print(f"Build notes NOT publishable — {len(issues)} problem(s):\n")
        for i in issues:
            print(f"  - {i}")
        raise SystemExit(1)
    print(f"{sys.argv[1]}: publishable — no PII, no phase references, heading correct.")
