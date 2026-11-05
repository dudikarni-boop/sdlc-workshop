"""Poll logic as plain functions over plain data.

Nothing here touches files or Streamlit. That's what makes it easy to test: every
function takes a poll and returns a value or a new poll.
"""

from __future__ import annotations

from datetime import datetime
from typing import TypedDict


class Poll(TypedDict):
    question: str
    options: list[str]
    votes: dict[str, int]
    created_at: str | None  # ISO time; missing from polls saved before it existed


def create_poll(question: str, options: list[str], created_at: datetime | None = None) -> Poll:
    """Return a new poll with zero votes. Surrounding whitespace and blank options are dropped.

    `created_at` is passed in rather than read from the clock, so this stays pure.
    """
    question = question.strip()
    cleaned = [option.strip() for option in options if option.strip()]
    if not question:
        raise ValueError("A poll needs a question.")
    if len(cleaned) < 2:
        raise ValueError("A poll needs at least two options.")
    if len(set(cleaned)) != len(cleaned):
        raise ValueError("Options must be unique.")
    return {
        "question": question,
        "options": cleaned,
        "votes": {option: 0 for option in cleaned},
        "created_at": created_at.isoformat(timespec="seconds") if created_at else None,
    }


def vote(poll: Poll, option: str) -> Poll:
    """Return a copy of the poll with one more vote for `option`."""
    if option not in poll["votes"]:
        raise ValueError(f"Unknown option: {option!r}")
    votes = {**poll["votes"], option: poll["votes"][option] + 1}
    return {**poll, "votes": votes}


def tally(poll: Poll) -> list[tuple[str, int]]:
    """Vote counts per option, in the order the options were created."""
    return [(option, poll["votes"][option]) for option in poll["options"]]


def total_votes(poll: Poll) -> int:
    return sum(poll["votes"].values())


def created_label(poll: Poll) -> str | None:
    """'Created YYYY-MM-DD HH:MM', or None for a poll with no creation time."""
    created_at = poll.get("created_at")
    if not created_at:
        return None
    return f"Created {datetime.fromisoformat(created_at):%Y-%m-%d %H:%M}"
