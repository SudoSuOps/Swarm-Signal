# vLLM 0.17.0 Deployment — Swarm Compute Upgrade

**Date**: 2026-03-08
**Status**: LIVE on swarmrails dual-GPU fleet

## Summary

Replaced llama-server with vLLM 0.17.0 for serving SwarmCurator-9B and SwarmCurator-27B. Native Blackwell SM120 support, continuous batching, bf16 inference with zero quantization loss.

## Benchmark Results

```
============================================================
vLLM THROUGHPUT BENCHMARK — 4 requests x 512 max_tokens
============================================================
  9B (3090 Ti)    | Sequential     |  44.8s | 2048 tok |  45.7 tok/s
  9B (3090 Ti)    | Concurrent x4  |  12.4s | 2048 tok | 164.8 tok/s

  27B (Blackwell)  | Sequential     |  90.8s | 2048 tok |  22.6 tok/s
  27B (Blackwell)  | Concurrent x4  |  23.3s | 2048 tok |  87.9 tok/s
============================================================
```

**3.6x throughput from continuous batching. ~1,740 pairs/hour combined.**

## Before / After

| Metric | llama-server | vLLM 0.17.0 |
|--------|-------------|-------------|
| Blackwell support | sm_86 emulated | sm_120 native |
| Batching | Sequential (1 req/GPU) | Continuous |
| 9B throughput | ~46 tok/s | 165 tok/s |
| 27B throughput | ~23 tok/s | 88 tok/s |
| 27B precision | Q8_0 GGUF | bf16 native |
| Pairs/hour | ~140 | ~1,740 |

## Hardware

```
GPU 0: RTX 3090 Ti 24GB (sm_86)  — SwarmCurator-9B bf16 :8081
GPU 1: RTX PRO 6000 Blackwell 96GB (sm_120) — SwarmCurator-27B bf16 :8082
```

## Key Discovery: Qwen3.5 Vision Config Fix

Unsloth's merge strips `vision_config` from Qwen3.5 models. vLLM needs it because Qwen3.5 uses `Qwen3_5ForConditionalGeneration` (VL architecture) even for text-only fine-tunes.

**Fix**: Copy `vision_config` from the base model into the merged `config.json`. Critical field: `out_hidden_size` must match the text model's `hidden_size` (4096 for 9B, 5120 for 27B).

## Required vLLM Flags

| Flag | Reason |
|------|--------|
| `--skip-mm-profiling` | Text-only fine-tunes can't run visual profiling |
| `--enforce-eager` | GDN conv1d cache bug in CUDA graph warmup |
| `--limit-mm-per-prompt '{"image": 0}'` | No multimodal inputs |

## Full Deployment Guide

See [github.com/SudoSuOps/swarm-vllm](https://github.com/SudoSuOps/swarm-vllm) for launch scripts, config fix tool, and benchmark suite.
