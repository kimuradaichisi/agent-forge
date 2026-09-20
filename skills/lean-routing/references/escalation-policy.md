# Escalation Policy

Cheap workers must return control when requirements are contradictory, multiple materially different behaviors are plausible, public API or persistence semantics may change, security/privacy/destructive operations are involved, schema migration is involved, concurrency/transactions/distributed state are central, ownership is unclear, a failing test cannot be locally explained, a business rule would need invention, or delegated scope must materially expand.

Return:

```text
ESCALATE
Reason: <why cheap execution is no longer safe>
Evidence: <paths, symbols, test output, conflicting facts>
Smallest next question/decision: <one decision that unblocks the task>
```
