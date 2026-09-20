# Architecture

AgentForge separates workflow semantics from platform mechanics.

```text
skills/<skill>/          portable policy/procedure
        |
        +-- adapters/claude   model/tool/subagent wiring
        +-- adapters/codex
        +-- adapters/gemini
```

Core policy never depends on a proprietary repository-analysis tool. External indexes, search or static-analysis systems are optional deterministic/context providers.
