"""Poll logic as plain functions over plain data.

Nothing here touches files or Streamlit. That's what makes it easy to test: every
function takes a poll and returns a value or a new poll.
"""

from __future__ import annotations

from typing import TypedDict


class Poll(TypedDict):
    question: str
    options: list[str]
    votes: dict[str, int]


def create_poll(question: str, options: list[str]) -> Poll:
    """Return a new poll with zero votes. Surrounding whitespace and blank options are dropped."""
    question = question.strip()
    cleaned = [option.strip() for option in options if option.strip()]
    if not question:
        raise ValueError("A poll needs a question.")
    if len(cleaned) < 2:
        raise ValueError("A poll needs at least two options.")
    if len(set(cleaned)) != len(cleaned):
        raise ValueError("Options must be unique.")
    return {"question": question, "options": cleaned, "votes": {option: 0 for option in cleaned}}


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


def shares(poll: Poll) -> list[tuple[str, int]]:
    """Whole-number percentages per option, in creation order, that add up to 100.

    Each option gets its share rounded down, then the leftover points go to the largest
    remainders. Equal remainders favour the option listed first. All zeros when nobody
    has voted.
    """
    counts = tally(poll)
    total = total_votes(poll)
    if total == 0:
        return [(option, 0) for option, _ in counts]
    floors_and_remainders = [divmod(count * 100, total) for _, count in counts]
    leftover = 100 - sum(floor for floor, _ in floors_and_remainders)
    by_remainder = sorted(range(len(counts)), key=lambda i: -floors_and_remainders[i][1])
    bumped = set(by_remainder[:leftover])
    return [
        (option, floors_and_remainders[i][0] + (1 if i in bumped else 0))
        for i, (option, _) in enumerate(counts)
    ]


def leaders(poll: Poll) -> list[str]:
    """Options with the most votes, in creation order. Ties all lead; nobody leads at zero."""
    counts = tally(poll)
    top = max(count for _, count in counts)
    if top == 0:
        return []
    return [option for option, count in counts if count == top]


def result_lines(poll: Poll) -> list[str]:
    """One line per option, in creation order, e.g. 'Pizza: 3 votes · 60% 🏆' for a leader."""
    leading = leaders(poll)
    lines = []
    for (option, count), (_, share) in zip(tally(poll), shares(poll), strict=True):
        noun = "vote" if count == 1 else "votes"
        trophy = " 🏆" if option in leading else ""
        lines.append(f"{option}: {count} {noun} · {share}%{trophy}")
    return lines
