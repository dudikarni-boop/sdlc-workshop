# PR: feat: show each option's vote share and a trophy for the leader

- **Base:** `main`
- **Head:** `feat/percentages`
- **Why this file instead of a PR:** the `gh` account `dudikarni-boop` has only READ access to `origin` (`haco29/sdlc-workshop`), so no PR could be opened there.

---

## Why

People watching a live poll should see at a glance how the vote is split and who is winning. Under the existing bar chart, each option now gets one line showing its vote count, its whole-number share of the vote, and a 🏆 when it leads, e.g. `Pizza: 3 votes · 60% 🏆`.

Spec: [`sdlc/feat/percentages/spec.md`](sdlc/feat/percentages/spec.md)

## What changed

- **Task 1:** `shares(poll)` in `poll/core.py` gives whole-number shares that always add up to 100. It rounds every share down, then gives the leftover points to the largest remainders. When remainders are equal, the option listed first gets the point.
- **Task 2:** `leaders(poll)` returns the leader. Every option tied for the most votes leads, and nobody leads while there are no votes.
- **Task 3:** `result_lines(poll)` formats one line per option, and `app.py` shows those lines with `st.text` between the chart and the "N votes so far" caption.

## How it was tested

The test runs below are copied verbatim from the Test evidence log in `plan.md`:

- 2026-11-05 · /sdlc:test gap pass · `uv run python -m pytest -q` → 36 passed in 3.09s; `uv run python -m ruff check .` → All checks passed! (4 gaps closed; new tests passed first run, no bugs found)
- 2026-11-05 · review R2 fix · `uv run python -m pytest -q` → 36 passed in 3.21s; `uv run python -m ruff check .` → All checks passed!
- 2026-11-05 · review R3 fix · `uv run python -m pytest -q` → 36 passed in 3.15s; `uv run python -m ruff check .` → All checks passed!
- 2026-11-05 · /sdlc:code-simplify · `uv run python -m pytest -q` → 36 passed in 3.11s; `uv run python -m ruff check .` → All checks passed! (nothing to simplify)
- 2026-11-05 12:32 · /sdlc:pr G4 · `uv run python -m pytest -q` → 36 passed in 3.10s; `uv run python -m ruff check .` → All checks passed!

Every task was built test-first: the new tests failed first, then passed once the code was written. Those runs are also in `plan.md`.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 Spec | pass | `spec.md:3` reads `Status: Approved (2026-11-05)`, and no template text is left. |
| G2 Plan | pass | `plan.md` has 3 tasks with acceptance criteria, plus the coverage and evidence sections. |
| G3 Tasks | pass | All 3 boxes in `todo.md` are ticked. |
| G4 Evidence | pass | After the last commit: 36 passed and ruff clean (`plan.md`, evidence line 12:32). |
| G5 Alignment | pass | All 11 success criteria map to code and a test (`review.md`). Only `app.py`, `poll/core.py`, the tests and `sdlc/` changed. |
| G6 Coverage | pass | All 6 coverage lines are ticked. |

## Review

Five-axis review by a separate `code-reviewer` agent. It found 3 Suggestions and nothing at Critical or Important level. The reviewer also deliberately broke the code in 6 small ways: the tests caught 5, and the sixth changed nothing, so no test could catch it. The full findings are in `review.md`.

- **Fixed, R2:** the test that checks where the result lines appear now casts a vote first, so it's checked with real shares and not only at 0%.
- **Fixed, R3:** `shares` now writes `1 if i in bumped else 0` instead of adding a true/false value to a number.
- **Won't fix, R1:** the caption still says "1 votes so far". The spec only asked for the singular "vote" in the result lines, so this is left for a follow-up.

## Out of scope

- Decimal percentages, sorting results by votes, and any change to the bar chart.
- Changes to the stored poll format, `poll/store.py`, or the create/vote flow.
- Auto-refresh and CSV export.
- **Follow-up:** a shared "vote"/"votes" helper so the "N votes so far" caption also uses the singular (R1).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
