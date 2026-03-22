# Example: "We Need a Rate Limiter"

A ticket says: "Implement rate limiting on the /export endpoint — users are generating too many large exports and it's causing CPU spikes."

## Name the Frame

"The problem is too many requests; the solution is fewer requests."

## Check Freshness

When was this ticket written? Two sprints ago. Since then, the team migrated to async job processing for exports. Does the CPU spike still happen? Nobody has checked since the migration.

## Check Scope

The ticket assumes the problem is request volume. But "large exports causing CPU spikes" could also mean:
- The export query is unoptimized (problem is per-request cost, not request count)
- The export runs synchronously and blocks the event loop (problem is architecture, not volume)
- A single user is exporting the entire dataset (problem is missing pagination, not rate limiting)

Rate limiting treats all of these as "too many requests" and solves none of them precisely.

## Name the Blind Spots

The ticket's vocabulary is "requests per time window." It can't see per-request resource cost, query efficiency, or whether async processing already solved the problem.

## Rate Confidence

Least confident about: whether the CPU spike still reproduces after the async migration. Check that before writing any code.

## Outcome

Monitoring shows CPU spikes stopped after async migration. The ticket is obsolete. A rate limiter would have added complexity for a problem that no longer exists.
