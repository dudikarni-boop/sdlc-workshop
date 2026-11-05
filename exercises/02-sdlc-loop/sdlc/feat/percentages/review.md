# Review: percentages and a winner

Reviewed 2026-11-05 by the `code-reviewer` agent, starting fresh without the author's reasoning, against `spec.md` and `plan.md`.
Scope: `git diff $(git merge-base HEAD main)` at `4aa7c63`.

**Checks at review time:**
- `uv run python -m pytest -q`: 36 passed
- `uv run python -m ruff check .`: All checks passed!

**Mutation run on `poll/core.py`:** 5 of 6 mutants killed. The survivor (sorting with `reverse=True`) is equivalent, because the sort is stable and gives the same result.

**Spec alignment:** complete. All 11 success criteria and every edge case map to code and a test, and nothing outside the spec's scope changed.

| ID | Severity | Axis | Location | Finding | Fix | Status |
|---|---|---|---|---|---|---|
| R1 | Suggestion | Correctness / UX | `app.py:41`, `tests/test_app.py:35` | The caption reads "1 votes so far" right under "Sushi: 1 vote · 100% 🏆". The spec limits the singular rule to the result lines, so this branch follows the spec. | Follow-up outside this spec: add a `votes_label(n)` helper to the core, use it for both the lines and the caption, and update the assertion. | open |
| R2 | Suggestion | Tests | `tests/test_app.py:42-54` | The placement test never votes. That leaves spec #10 ("a poll with votes") checked only for placement when every line is `0%`. | Vote before checking the order, or fold the order check into `test_create_a_poll_then_vote`. | fixed |
| R3 | Suggestion | Readability | `poll/core.py:64` | `floors_and_remainders[i][0] + (i in bumped)` adds a bool to an int, which the reader has to decode. | Use `+ (1 if i in bumped else 0)`, or leave it for `/sdlc:code-simplify`. | fixed |
