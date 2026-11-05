# Spec: Percentages and a winner

Status: Approved (2026-11-05)

## Objective

People watching a live poll should see at a glance how the vote is split and who is
winning. Under the existing bar chart, each option gets one line with its vote count, its
whole-number share of the vote, and a 🏆 when it leads, e.g. `Pizza: 3 votes · 60% 🏆`.

## Scope

In scope:
- A pure function in `poll/core.py` that turns a poll into per-option shares: whole-number
  percentages that add up to 100% (largest-remainder rounding), in creation order.
- A pure function in `poll/core.py` that says which options lead (most votes, ties share
  the lead, nobody leads at zero votes).
- A pure function in `poll/core.py` that formats one results line per option, so `app.py`
  only renders strings.
- `app.py`: render those lines under the bar chart, above the "N votes so far" caption.
- Tests first in `tests/test_core.py`; one wiring check in `tests/test_app.py`.

Out of scope:
- Decimal percentages.
- Sorting results by votes.
- Changing, replacing or labelling the bar chart (no percentages or 🏆 inside it).
- Changes to the stored poll format, `poll/store.py`, or the create/vote flow.
- Auto-refresh and CSV export.

## Success criteria

1. Given a poll with votes, when shares are computed, then each option has a whole-number
   percentage and the percentages add up to exactly 100.
2. Given votes 1/1/1 across three options, then the shares are `34 / 33 / 33` (the leftover
   point goes to the first-listed option), not `33 / 33 / 33`.
3. Given votes where plain rounding would overshoot (1/1/3/3 → 12.5/12.5/37.5/37.5), then
   the shares still add up to 100 (`13 / 13 / 37 / 37`).
4. Given a poll with zero votes, then every option's share is 0 and no option leads.
5. Given one option with strictly the most votes, then exactly that option leads.
6. Given two or more options tied for the most votes, then every tied option leads.
7. Given any poll, results are listed in the order the options were created.
8. Given a poll, each results line reads `<option>: <n> votes · <p>%`, with ` 🏆` appended
   for each leading option.
9. Computing shares, leaders or lines does not change the poll passed in.
10. When the app shows a poll with votes, the results lines appear in the page under the
    chart (smoke test in `tests/test_app.py`).
11. `uv run python -m pytest -q` and `uv run python -m ruff check .` both pass.

## Edge cases and decisions

| Case | Decision | Why |
|---|---|---|
| Rounding | Whole numbers, largest-remainder method, total always 100 | Answered in grilling: a room seeing 99% thinks it's a bug |
| Equal remainders (incl. tied counts that can't split evenly) | Extra point goes to the option listed first | Answered in grilling: deterministic and testable; 🏆 already marks the tie |
| Zero votes | Every option `0%`, no 🏆 | Answered in grilling: nobody leads yet; "0 votes so far" explains it |
| Tie for the lead | Every tied option gets 🏆 | Answered in grilling: honest, no obscure tie-break |
| Result order | Creation order, same as the form and chart | Answered in grilling: options shouldn't jump while votes arrive |
| Placement | Keep the bar chart; one line per option under it | Answered in grilling: `st.bar_chart` can't label bars |
| `1 vote` vs `1 votes` | Singular `vote` for a count of 1 | Confirmed with the spec's approval |
| A single option with all the votes | `100%` and 🏆; the rest `0%` | Follows from the rules above |

## Open questions

- None.

## Decisions

- No ADR: no decision here has a trade-off big enough to record beyond this table.
