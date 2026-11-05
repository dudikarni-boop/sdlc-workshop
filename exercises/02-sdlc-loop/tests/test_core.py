import pytest

from poll.core import create_poll, leaders, shares, tally, total_votes, vote


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


def poll_with_votes(counts):
    poll = create_poll("Lunch?", list(counts))
    for option, count in counts.items():
        for _ in range(count):
            poll = vote(poll, option)
    return poll


def test_shares_are_zero_when_nobody_has_voted():
    assert shares(make_poll()) == [("Pizza", 0), ("Sushi", 0), ("Salad", 0)]


def test_shares_give_the_leftover_point_to_the_first_listed_option():
    poll = poll_with_votes({"Pizza": 1, "Sushi": 1, "Salad": 1})

    assert shares(poll) == [("Pizza", 34), ("Sushi", 33), ("Salad", 33)]


def test_shares_add_up_to_100_when_plain_rounding_would_overshoot():
    poll = poll_with_votes({"Pizza": 1, "Sushi": 1, "Salad": 3, "Tacos": 3})

    assert shares(poll) == [("Pizza", 13), ("Sushi", 13), ("Salad", 37), ("Tacos", 37)]


def test_shares_give_the_leftover_point_to_the_largest_remainder():
    poll = poll_with_votes({"Pizza": 1, "Sushi": 2, "Salad": 4})

    # 14.28 / 28.57 / 57.14: Sushi has the largest remainder.
    assert shares(poll) == [("Pizza", 14), ("Sushi", 29), ("Salad", 57)]


def test_shares_give_100_to_an_option_with_every_vote():
    poll = poll_with_votes({"Pizza": 0, "Sushi": 5, "Salad": 0})

    assert shares(poll) == [("Pizza", 0), ("Sushi", 100), ("Salad", 0)]


def test_shares_always_add_up_to_100():
    poll = poll_with_votes({"Pizza": 3, "Sushi": 5, "Salad": 9, "Tacos": 1, "Soup": 11})

    assert sum(share for _, share in shares(poll)) == 100


def test_shares_keep_the_order_options_were_created_in():
    poll = poll_with_votes({"Pizza": 1, "Sushi": 0, "Salad": 3})

    assert [option for option, _ in shares(poll)] == ["Pizza", "Sushi", "Salad"]


def test_shares_leave_the_poll_unchanged():
    poll = poll_with_votes({"Pizza": 1, "Sushi": 2})
    before = {**poll, "votes": dict(poll["votes"])}

    shares(poll)

    assert poll == before


def test_nobody_leads_when_nobody_has_voted():
    assert leaders(make_poll()) == []


def test_the_option_with_the_most_votes_leads():
    poll = poll_with_votes({"Pizza": 1, "Sushi": 3, "Salad": 2})

    assert leaders(poll) == ["Sushi"]


def test_every_option_tied_for_the_most_votes_leads():
    poll = poll_with_votes({"Pizza": 2, "Sushi": 1, "Salad": 2})

    assert leaders(poll) == ["Pizza", "Salad"]


def test_leaders_leave_the_poll_unchanged():
    poll = poll_with_votes({"Pizza": 1, "Sushi": 2})
    before = {**poll, "votes": dict(poll["votes"])}

    leaders(poll)

    assert poll == before
