# Example: Flaky Integration Test

A test passes locally but fails ~30% of the time in CI.

## Represent

**Model A (primary):** The test depends on insertion order from a database query that has no `ORDER BY`. Locally the DB returns rows in insertion order by coincidence; CI uses a parallel test runner that seeds data differently.

**Model B (alternative):** The test has a race condition — it reads before an async write completes, and CI machines are slower.

**Divergence:** Model A predicts the failure is deterministic for a given data seed. Model B predicts the failure rate changes with machine load.

**Least confident about:** Whether CI actually uses a parallel test runner. Check that first.

## Predict

If Model A: adding `ORDER BY` to the query fixes it with 100% reliability.
If Model B: adding a sleep or explicit wait fixes it, but `ORDER BY` does not.

## Intervene

Check CI config for parallel test runner (distinguishes the models cheaply). Then add `ORDER BY` and run 50 iterations in CI.

## Observe

CI config confirms parallel runner. After adding `ORDER BY`, 50/50 green.

## Update

Model A confirmed. No structural revision needed — the model was right, the query was incomplete.
