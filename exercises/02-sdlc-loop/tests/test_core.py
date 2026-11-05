from datetime import datetime

import pytest

from poll.core import create_poll, created_label, tally, total_votes, vote


def make_poll():
    return create_poll("Lunch?", ["Pizza", "Sushi", "Salad"])


def test_create_poll_starts_with_zero_votes():
    poll = make_poll()

    assert poll["question"] == "Lunch?"
    assert poll["options"] == ["Pizza", "Sushi", "Salad"]
    assert poll["votes"] == {"Pizza": 0, "Sushi": 0, "Salad": 0}


def test_create_poll_trims_whitespace_and_drops_blank_options():
    poll = create_poll("  Lunch?  ", [" Pizza ", "", "   ", "Sushi"])

    assert poll["question"] == "Lunch?"
    assert poll["options"] == ["Pizza", "Sushi"]


def test_create_poll_needs_a_question():
    with pytest.raises(ValueError, match="question"):
        create_poll("   ", ["Pizza", "Sushi"])


def test_create_poll_needs_two_options():
    with pytest.raises(ValueError, match="two options"):
        create_poll("Lunch?", ["Pizza", ""])


def test_create_poll_rejects_duplicate_options():
    with pytest.raises(ValueError, match="unique"):
        create_poll("Lunch?", ["Pizza", "Pizza"])


def test_vote_adds_one_vote_to_the_option():
    poll = vote(make_poll(), "Sushi")

    assert poll["votes"]["Sushi"] == 1
    assert poll["votes"]["Pizza"] == 0


def test_vote_leaves_the_original_poll_unchanged():
    original = make_poll()

    vote(original, "Pizza")

    assert original["votes"]["Pizza"] == 0


def test_vote_for_an_unknown_option_raises():
    with pytest.raises(ValueError, match="Unknown option"):
        vote(make_poll(), "Burgers")


def test_tally_keeps_the_order_options_were_created_in():
    poll = vote(vote(make_poll(), "Salad"), "Salad")

    assert tally(poll) == [("Pizza", 0), ("Sushi", 0), ("Salad", 2)]


def test_total_votes_counts_every_vote():
    poll = vote(vote(vote(make_poll(), "Pizza"), "Sushi"), "Pizza")

    assert total_votes(poll) == 3


def test_total_votes_is_zero_for_a_new_poll():
    assert total_votes(make_poll()) == 0


def test_create_poll_records_when_it_was_created():
    poll = create_poll("Lunch?", ["Pizza", "Sushi"], created_at=datetime(2026, 11, 5, 10, 31, 24))

    assert poll["created_at"] == "2026-11-05T10:31:24"


def test_create_poll_without_a_time_has_no_created_at():
    assert make_poll()["created_at"] is None


def test_vote_keeps_the_created_at():
    poll = create_poll("Lunch?", ["Pizza", "Sushi"], created_at=datetime(2026, 11, 5, 10, 31))

    assert vote(poll, "Pizza")["created_at"] == poll["created_at"]


def test_created_label_shows_date_and_time():
    poll = create_poll("Lunch?", ["Pizza", "Sushi"], created_at=datetime(2026, 11, 5, 9, 7, 59))

    assert created_label(poll) == "Created 2026-11-05 09:07"


def test_created_label_is_none_for_a_poll_without_a_time():
    assert created_label(make_poll()) is None


def test_created_label_is_none_for_a_poll_saved_before_created_at_existed():
    old_poll = make_poll()
    del old_poll["created_at"]

    assert created_label(old_poll) is None
