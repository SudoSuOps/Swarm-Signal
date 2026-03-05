"""Tests for core/config.py — SwarmConfig defaults and properties."""

from swarm.core.config import SwarmConfig


# --- Default Values ---

def test_model_defaults():
    cfg = SwarmConfig()
    assert cfg.default_base_model == "Qwen/Qwen3.5-9B"
    assert cfg.max_seq_length == 4096


def test_lora_defaults():
    cfg = SwarmConfig()
    assert cfg.default_lora_r == 64
    assert cfg.default_lora_alpha == 32


def test_training_defaults():
    cfg = SwarmConfig()
    assert cfg.default_batch_size == 4
    assert cfg.default_grad_accum == 8
    assert cfg.default_learning_rate == 5e-5
    assert cfg.default_epochs == 1


def test_quality_thresholds():
    cfg = SwarmConfig()
    assert cfg.min_pair_length == 200
    assert cfg.max_pair_length == 32000
    assert cfg.quality_score_threshold == 0.7


# --- Path Properties ---

def test_project_root_is_dir():
    cfg = SwarmConfig()
    assert cfg.project_root.is_dir()
    assert (cfg.project_root / "core").is_dir()


def test_contracts_dir():
    cfg = SwarmConfig()
    assert cfg.contracts_dir.name == "contracts"
    assert cfg.contracts_dir.is_dir()


def test_pair_schema_path():
    cfg = SwarmConfig()
    assert cfg.pair_schema_path.name == "pair.schema.json"
    assert cfg.pair_schema_path.exists()


def test_eval_schema_path():
    cfg = SwarmConfig()
    assert cfg.eval_schema_path.name == "eval.schema.json"
    assert cfg.eval_schema_path.exists()


def test_dataset_schema_path():
    cfg = SwarmConfig()
    assert cfg.dataset_schema_path.name == "dataset.schema.json"
    assert cfg.dataset_schema_path.exists()
