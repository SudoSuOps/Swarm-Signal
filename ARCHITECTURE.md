# SwarmCode Architecture

The SwarmCode system is structured as follows:

```
core/       – runtime and registry (immutable)
agents/     – AI agents
pipelines/  – training and dataset pipelines
contracts/  – schema definitions
tests/      – validation layer
```

Agents may only modify code inside `agents/` and `pipelines/`.
