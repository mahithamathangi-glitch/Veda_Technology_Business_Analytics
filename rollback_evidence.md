# Rollback Evidence

## Version Control Strategy

Git was used to maintain project history and provide version
traceability.

## Stable Version

The initial stable version of the project is identified by:

`v1.0`

## Rollback Process

If a future project version introduces an issue, the repository
can be reviewed or restored to the stable `v1.0` version.

## Verification Commands

```bash
git log --oneline
git tag
The output of these commands is captured in:

images/rollback_evidence.png