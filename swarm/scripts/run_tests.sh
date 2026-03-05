#!/usr/bin/env bash
# run_tests.sh — Mandatory test gate. All three must pass.
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

echo "=== pytest ==="
PYTHONPATH=. python3 -m pytest swarm/tests/ -v

echo ""
echo "=== ruff ==="
python3 -m ruff check swarm/

echo ""
echo "=== mypy ==="
PYTHONPATH=. python3 -m mypy swarm/ --ignore-missing-imports

echo ""
echo "=== All gates passed ==="
