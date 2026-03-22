# Example: API Endpoint Latency Spike

An endpoint that normally responds in 50ms is now taking 2-3 seconds after a deploy.

## Represent

**Model A (primary):** The deploy introduced an N+1 query — a new feature loads related records one at a time instead of batch.

**Model B (alternative):** The deploy coincided with a data growth milestone — the table crossed a threshold where the existing index no longer fits in memory.

**Divergence:** Model A predicts latency scales with the number of related records per request. Model B predicts latency is uniformly high regardless of request shape.

**Least confident about:** Whether the deploy actually touched the query code. Check the diff first.

## Predict

If Model A: requests with few related records are still fast; requests with many are slow. Query count per request will be high.
If Model B: all requests are uniformly slow. Query count is normal but each query is slow.

## Intervene

**Executable verification:** Enable query logging, hit the endpoint with a minimal request (1 related record) and a heavy one (50 related records). Count queries and measure per-query time.

## Observe

Minimal request: 3 queries, 45ms. Heavy request: 52 queries, 2400ms. Per-query time is normal (~5ms).

## Update

Model A confirmed — N+1 query. Structural model is correct; the fix is a batch load (`WHERE id IN (...)`).
