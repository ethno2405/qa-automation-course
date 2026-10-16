"""Switch for the seeded defects of the course shop.

The environment variable SUT_DEFECTS selects the active defects:

- empty or "none": no defects (the shop follows REQUIREMENTS.md)
- "all": all defects
- a comma-separated list of defect IDs, for example "D01,D04"

The mentor document docs/mentor/sut-defects.md describes each defect.
"""

import os

ALL_DEFECTS = frozenset(f"D{number:02d}" for number in range(1, 11))


def _parse(value: str) -> frozenset[str]:
    value = value.strip()
    if value.lower() in ("", "none", "off", "0"):
        return frozenset()
    if value.lower() == "all":
        return ALL_DEFECTS
    requested = {item.strip().upper() for item in value.split(",") if item.strip()}
    return frozenset(requested & ALL_DEFECTS)


_active = _parse(os.environ.get("SUT_DEFECTS", ""))


def on(defect_id: str) -> bool:
    """Return True if the defect is active."""
    return defect_id in _active


def mode() -> str:
    """Return "off" if no defect is active, otherwise "on"."""
    return "on" if _active else "off"
