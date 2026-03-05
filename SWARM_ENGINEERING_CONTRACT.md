# Swarm Engineering Contract

You are modifying a production system.
Your primary goal is stability, not refactoring.

---

## Locked Files (READ-ONLY)

```
core/runtime.py
core/config.py
contracts/*
tests/*
```

Do NOT modify these files unless explicitly instructed.

## Editable Zones

```
agents/
pipelines/
scripts/
```

---

## Rules

### 1. Core directory is read-only.

Never touch `core/runtime.py` or `core/config.py`. These define the runtime and config interfaces.

### 2. Contracts directory defines dataset schema.

All pipeline outputs must conform to the schemas in `contracts/`. The canonical dataset schema:

```json
{
  "instruction": "string",
  "response": "string",
  "score": "float",
  "domain": "string",
  "metadata": "object"
}
```

### 3. Pipelines must output valid schema.

Every pipeline that produces data must emit records matching `contracts/pair.schema.json`. No exceptions.

### 4. Agents must register in registry.py.

All swarm agents must be registered in the `AGENTS` dictionary:

```python
AGENTS = {
    "swarmjudge": SwarmJudgeAgent,
    "swarmcode": SwarmCodeAgent,
    "swarmcre": SwarmCREAgent,
    "swarmmed": SwarmMedAgent,
}
```

Agents cannot create new ones randomly. New agents require a registry entry.

### 5. Architecture cannot be changed.

You may **NOT**:
- Rename modules
- Restructure folders
- Remove interfaces
- Refactor system architecture

You may **ONLY** implement functionality inside existing modules.

### 6. Modification scope: 200 lines max.

If more changes are required, propose a plan first.

### 7. Minimal changes only.

Fix the task with the smallest safe modification. Never refactor unrelated code.

---

## Mandatory Test Gate

Nothing merges unless all three pass:

```
pytest
ruff
mypy
```

If tests fail, the change is rejected.

---

## Workflow

1. Analyze the repository structure
2. Identify the minimal file to modify
3. Explain the change in a short plan
4. Implement the change
5. Run test gate
6. Confirm tests pass
