# Example: "The Cache Is Fine"

A developer reports that search results are stale after a data migration. The team assumes the migration was clean and focuses on cache invalidation.

## Name the Frame

"The migration was correct; the problem is that cached data hasn't been refreshed."

## Check Freshness

The migration ran 3 hours ago. Has anyone verified that the migrated data is correct in the database? No — everyone jumped straight to cache debugging because the migration script "worked" (exited 0).

## Check Scope

The team is solving "how to invalidate the cache." But the actual problem might be "the migration corrupted data." These have completely different fixes. One is a cache flush; the other is a data repair.

**Reframe:** Before debugging cache invalidation, run a query comparing pre- and post-migration data for a sample of records.

## Name the Blind Spots

The migration script has no validation step — it reports success based on zero errors, not on data correctness. The team's vocabulary doesn't distinguish between "migration ran" and "migration is correct."

## Rate Confidence

Least confident about: whether the migration actually preserved data integrity. This is where verification effort should go first.

## Outcome

Sample query reveals the migration dropped a foreign key relationship. Search results are stale because the data is wrong, not because the cache is stale. Cache invalidation would have served stale-from-source data.
