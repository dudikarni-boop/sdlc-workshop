# Plan: Percentages and a winner

Spec: [spec.md](spec.md)

## Approach

All rules live in `poll/core.py` as pure functions over the existing `Poll` dict, next to
`tally` and `total_votes`; no new module, no change to the stored format or `poll/store.py`.

- `shares(poll) -> list[tuple[str, int]]`: whole-number percentages in creation order,
  by largest remainder. Floor each `votes * 100 / total`, then hand the leftover points to
  the largest remainders; equal remainders go to the option listed first (stable sort on
  `-remainder`). Integer arithmetic (`divmod(votes * 100, total)`) so there's no float
  rounding. Zero total → every share is 0.
- `leaders(poll) -> list[str]`: options with the highest count, in creation order; empty
  when the total is zero.
- `result_lines(poll) -> list[str]`: `"<option>: <n> vote(s) · <p>%"` plus `" 🏆"` for
  leaders, built from `tally`, `shares` and `leaders`.

`app.py` calls `result_lines(poll)` and renders each line with `st.text` between the bar
chart and the "N votes so far" caption. `st.text` rather than `st.markdown`, so option
names typed by users aren't interpreted as markdown, and the caption stays `caption[0]`
for the existing smoke test.

Tests are written first in `tests/test_core.py` (red, then green) for each function;
`tests/test_app.py` gets one wiring assertion.

## Tasks

### Task 1: Whole-number shares that add up to 100

- Acceptance criteria: spec #1, #2, #3, #4 (shares part), #7, #9.
- Test that proves it: `test_shares_*` in `tests/test_core.py`: zero votes → all 0;
  1/1/1 → 34/33/33; 1/1/3/3 → 13/13/37/37; one option with all votes → 100/0/0; sum is
  100 for a mixed poll; creation order kept; input poll unchanged.
- Files: `poll/core.py`, `tests/test_core.py`.

### Task 2: Leaders, with ties and zero votes

- Acceptance criteria: spec #4 (no leader), #5, #6, #9.
- Test that proves it: `test_leaders_*`: zero votes → `[]`; single leader → `[it]`; two-way
  tie → both, in creation order; input poll unchanged.
- Files: `poll/core.py`, `tests/test_core.py`.

### Task 3: Results lines in the app

- Acceptance criteria: spec #8, #10, #11 (and "1 vote" singular from the edge-case table).
- Test that proves it: `test_result_lines_*` in `tests/test_core.py` (leader gets ` 🏆`,
  others don't, singular/plural, zero votes has no 🏆); `tests/test_app.py` asserts that
  after one vote for Sushi the page shows `Sushi: 1 vote · 100% 🏆` and
  `Pizza: 0 votes · 0%`.
- Files: `poll/core.py`, `tests/test_core.py`, `app.py`, `tests/test_app.py`.

### Checkpoint: after Task 3

- Full suite and ruff pass: `uv run python -m pytest -q` and `uv run python -m ruff check .`
- Manual: run the app, vote a few times including a tie, and check the lines.

## Risks

- **Tie-break on equal remainders depends on sort stability.** Covered by the 1/1/1 and
  1/1/3/3 tests, which fail if the extra point lands on the wrong option.
- **`AppTest` element access for `st.text`.** If `app.text` isn't exposed the way the plan
  assumes, the wiring test in Task 3 may need a different query; we'd notice when the test
  is written red.
- **The shell is blocked by enterprise policy in this session**, so the user runs
  `pytest`, `ruff` and `git` and pastes the results; evidence lines record their output.

## SDLC command coverage

- [x] /sdlc:spec: approved 2026-11-05 after 6 questions
- [x] /sdlc:plan: 3 tasks
- [x] /sdlc:build: 3 tasks, one commit each
- [x] /sdlc:test: 11 criteria + 8 edge cases mapped, 4 gaps closed, no bugs
- [x] /sdlc:review: 3 findings (all Suggestions): 2 fixed, 1 won't fix
- [x] /sdlc:code-simplify: nothing to simplify (R3 readability fix already landed in review)

## Test evidence

- 2026-11-05 · task 1 RED · `uv run python -m pytest tests/test_core.py -q` → 1 error during collection: `ImportError: cannot import name 'shares' from 'poll.core'` (expected)
- 2026-11-05 · task 1 GREEN · `uv run python -m pytest -q` → 25 passed in 7.65s; `uv run python -m ruff check .` → All checks passed!
- 2026-11-05 · task 2 RED · `uv run python -m pytest tests/test_core.py -q` → 1 error during collection: `ImportError: cannot import name 'leaders' from 'poll.core'` (expected)
- 2026-11-05 · task 2 GREEN · `uv run python -m pytest -q` → 29 passed in 2.77s; `uv run python -m ruff check .` → All checks passed!
- 2026-11-05 · task 3 RED · `uv run python -m pytest -q` → 1 error during collection: `ImportError: cannot import name 'result_lines' from 'poll.core'` (expected; collection error interrupted the run before the new `test_app.py` assertion ran)
- 2026-11-05 · task 3 GREEN · `uv run python -m pytest -q` → 33 passed in 10.78s; `uv run python -m ruff check .` → All checks passed!
- 2026-11-05 · /sdlc:test gap pass · `uv run python -m pytest -q` → 36 passed in 3.09s; `uv run python -m ruff check .` → All checks passed! (4 gaps closed; new tests passed first run, no bugs found)
- 2026-11-05 · review R2 fix · `uv run python -m pytest -q` → 36 passed in 3.21s; `uv run python -m ruff check .` → All checks passed!
- 2026-11-05 · review R3 fix · `uv run python -m pytest -q` → 36 passed in 3.15s; `uv run python -m ruff check .` → All checks passed!
- 2026-11-05 · /sdlc:code-simplify · `uv run python -m pytest -q` → 36 passed in 3.11s; `uv run python -m ruff check .` → All checks passed! (nothing to simplify)

