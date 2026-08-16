# Hosted Model Source Ledger
## JARVIS Autonomous SWE System — Citation Registry

**Research Date:** August 17, 2026  
**Purpose:** Every factual claim in `docs/research/hosted-open-model-landscape.md` is traceable to a source in this ledger.

---

## Ledger Format

Each entry contains: Title, Publisher, URL, Publication/Access Date, Source Type, Models Covered, Claims Supported, Primary or Secondary, Trust Level, Conflicts.

Trust levels: **High** (official primary source; pricing/availability/model specs), **Medium** (independent analysis; benchmarks with disclosed methodology), **Low** (community reports; vendor claims without reproduction).

---

## Source Entries

---

### SRC-001 — OpenHands Official LLM Documentation

| Field | Value |
|-------|-------|
| Title | OpenHands LLM Usage Documentation — Model Recommendations |
| Publisher | All Hands AI |
| URL | https://docs.openhands.dev/openhands/usage/llms/llms |
| Access Date | August 17, 2026 |
| Source Type | Official product documentation |
| Models Covered | GLM-5.1 (openrouter/z-ai/glm-5.1), MiniMax M3 (openrouter/minimax/minimax-m3), Kimi K2.6 (openrouter/moonshotai/kimi-k2.6), GLM-5 (openrouter/z-ai/glm-5), Kimi K2.5 (openrouter/moonshotai/kimi-k2.5) |
| Claims Supported | OpenHands Index Average scores: GLM-5.1 = 58.2; MiniMax M3 = 57.2; Kimi K2.6 = 57.1; GLM-5 = 49.4; Kimi K2.5 = 49.2. Model string format for OpenHands configuration. LiteLLM compatibility. |
| Primary or Secondary | **Primary** |
| Trust Level | **High** — official product docs with links to results repository |
| Conflicts | None found |

---

### SRC-002 — DeepSeek API Official Pricing Page

| Field | Value |
|-------|-------|
| Title | Models & Pricing — DeepSeek API Docs |
| Publisher | DeepSeek |
| URL | https://api-docs.deepseek.com/quick_start/pricing |
| Access Date | August 17, 2026 |
| Source Type | Official API pricing documentation |
| Models Covered | deepseek-v4-flash (V4-Flash-0731), deepseek-v4-pro (V4-Pro-0813) |
| Claims Supported | Off-peak pricing: V4 Flash $0.22/$0.66 input/output; V4 Pro $0.66/$1.98. Peak pricing: V4 Flash $0.44/$1.32; V4 Pro $1.32/$3.96. Cache hit pricing (off-peak): V4 Flash $0.007; V4 Pro $0.022. Context window: 1M both models. Max output: 384K. Concurrency: V4 Flash 2500; V4 Pro 500. Tool calling: Yes. JSON output: Yes. Responses API: Yes. Anthropic API: Yes. Peak hours: 01:00–04:00 and 06:00–10:00 UTC. |
| Primary or Secondary | **Primary** |
| Trust Level | **High** |
| Conflicts | SRC-019 documents a recent 51–1100% price increase on August 16, 2026. Prices in this ledger are post-increase |

---

### SRC-003 — MiniMax Official Pricing Documentation

| Field | Value |
|-------|-------|
| Title | MiniMax API Pay-As-You-Go Pricing |
| Publisher | MiniMax |
| URL | https://platform.minimax.io/docs/guides/pricing-paygo.md |
| Access Date | August 17, 2026 |
| Source Type | Official API pricing documentation |
| Models Covered | MiniMax M3 |
| Claims Supported | Standard tier ≤512K: $0.30/$1.20 input/output; $0.06 cache read (permanent 50% off listed as ~~$0.60~~/$~~$2.40~~). Standard tier >512K: $0.60/$2.40; $0.12 cache read. Priority tier ≤512K: $0.45/$1.80; $0.09 cache read. Priority tier >512K: $0.90/$3.60; $0.18 cache read. |
| Primary or Secondary | **Primary** |
| Trust Level | **High** |
| Conflicts | None |

---

### SRC-004 — MiniMax M3 Launch Blog Post

| Field | Value |
|-------|-------|
| Title | MiniMax M3: Frontier Coding, 1M Context, Native Multimodality |
| Publisher | MiniMax Research |
| URL | https://www.minimax.io/blog/minimax-m3 |
| Access Date | August 17, 2026 |
| Source Type | Official model announcement |
| Models Covered | MiniMax M3 |
| Claims Supported | Release date: June 1, 2026. Architecture: MiniMax Sparse Attention (MSA). Context: up to 1M tokens. Modalities: text, image, video. Thinking toggle (on/off). Token plan pricing: Plus $20/mo (~1.7B tokens), Max $50/mo (~5.1B tokens), Ultra $120/mo (~9.8B tokens). SWE-bench Pro 59%. BrowseComp 83.5%. Open-weight release planned within ~10 days. |
| Primary or Secondary | **Primary** |
| Trust Level | **High** for availability and architecture; **Medium** for benchmark claims (vendor-reported) |
| Conflicts | None |

---

### SRC-005 — MiniMax M3 Detailed Specs (Third-Party)

| Field | Value |
|-------|-------|
| Title | MiniMax M3: API Pricing, Benchmarks & 1M Context |
| Publisher | minimax-ai.chat (independent documentation site) |
| URL | https://minimax-ai.chat/models/minimax-m3/ |
| Access Date | August 17, 2026 |
| Source Type | Secondary — independent compilation |
| Models Covered | MiniMax M3 |
| Claims Supported | ~428B total parameters; ~23B active per token. API formats: Anthropic-compatible and OpenAI-compatible. Maximum output: 524,288 tokens (hard max); recommended 131,072. Weights available on HuggingFace. MiniMax Community License. Pricing verified July 10, 2026. |
| Primary or Secondary | **Secondary** |
| Trust Level | **Medium** — verified against primary sources where checked |
| Conflicts | None found |

---

### SRC-006 — Kimi API Pricing Breakdown

| Field | Value |
|-------|-------|
| Title | Kimi (Moonshot AI) API Pricing & Agent Fit 2026 |
| Publisher | A8gent.com |
| URL | https://a8gent.com/models/moonshot-kimi |
| Access Date | August 17, 2026 |
| Source Type | Secondary — pricing analysis site |
| Models Covered | kimi-k3, kimi-k2.7-code, kimi-k2.7-code-highspeed, kimi-k2.6, kimi-k2.5 |
| Claims Supported | K3: $3.00/$15.00; cache hit $0.30; context 1,048,576; not batch-eligible. K2.7 Code: $0.95/$4.00; cache hit $0.19; batch-eligible; context 262,144. K2.7 Code Highspeed: $1.90/$8.00 (double standard). K2.6: $0.95/$4.00; batch-eligible. K2.5: $0.60/$3.00; cache hit $0.10; multimodal (text/image/video); batch-eligible. Batch discount: 60% of standard (40% off). Legacy moonshot-v1 family sunsets end of August 2026. |
| Primary or Secondary | **Secondary** |
| Trust Level | **High** — confirmed against Moonshot official pricing pages |
| Conflicts | None |

---

### SRC-007 — Kimi K3 API Technical Guide

| Field | Value |
|-------|-------|
| Title | Kimi K3 API Guide (2026): Pricing, Context, and Examples |
| Publisher | Verdent AI |
| URL | https://www.verdent.ai/guides/agents/kimi-k3-api-guide |
| Access Date | August 17, 2026 |
| Source Type | Secondary — developer guide |
| Models Covered | kimi-k3 |
| Claims Covered | API live: July 16, 2026. Base URL: https://api.moonshot.ai/v1. 2.8T-parameter MoE; 16 of 896 experts active (Kimi Delta Attention plus Attention Residuals). Reasoning: always-on max only. OpenAI-compatible Chat Completions. Agent compatibility note: must retain complete assistant message including reasoning content across tool calls. |
| Primary or Secondary | **Secondary** |
| Trust Level | **Medium** |
| Conflicts | None |

---

### SRC-008 — GLM-5.2 Model Card (HuggingFace)

| Field | Value |
|-------|-------|
| Title | zai-org/GLM-5.2 — HuggingFace Model Card |
| Publisher | Zhipu AI (Z.ai) |
| URL | https://huggingface.co/zai-org/GLM-5.2 |
| Access Date | August 17, 2026 |
| Source Type | Official model card |
| Models Covered | GLM-5.2, GLM-5.1, GLM-5 (with comparisons) |
| Claims Supported | Architecture: Sparse MoE; ~40B active / ~744B total (BF16). Context: 1M tokens. License: MIT. SWE-bench Pro 62.1%. NL2Repo 48.9%. Terminal-Bench (in card). Comparison table with Qwen3.7-Max, MiniMax M3, DeepSeek-V4-Pro, Claude Opus 4.8, GPT-5.5, Gemini 3.1 Pro. FP8 variant available. Inference frameworks: SGLang, vLLM, Transformers, KTransformers. Ascend NPU support. |
| Primary or Secondary | **Primary** |
| Trust Level | **High** for architecture/license/availability; **Medium** for benchmark claims (vendor-run) |
| Conflicts | None |

---

### SRC-009 — GLM-5.2 GitHub Repository

| Field | Value |
|-------|-------|
| Title | zai-org/GLM-5 GitHub Repository |
| Publisher | Zhipu AI |
| URL | https://github.com/zai-org/GLM-5 |
| Access Date | August 17, 2026 |
| Source Type | Official model repository |
| Models Covered | GLM-5, GLM-5.1, GLM-5.2 |
| Claims Supported | Model size table: GLM-5.2 = 744B-A40B BF16; FP8 variant. "GLM-5.2 is the strongest open-source model on standard coding benchmarks: 81.0 vs 62.0 on Terminal-Bench 2.1 and 62.1 vs 58.4 on SWE-bench Pro vs GLM-5.1." MIT license with no regional restrictions. Download links: HuggingFace and ModelScope. API available on Z.ai Platform. |
| Primary or Secondary | **Primary** |
| Trust Level | **High** |
| Conflicts | None |

---

### SRC-010 — GLM-5.2 Independent Review

| Field | Value |
|-------|-------|
| Title | GLM-5.2 Review — Zhipu's Open-Weight Coding Flagship |
| Publisher | agentguides.dev |
| URL | https://agentguides.dev/reviews/glm-5-2-review/ |
| Access Date | August 17, 2026 |
| Source Type | Secondary — editorial review |
| Models Covered | GLM-5.2 |
| Claims Supported | Release date: June 13, 2026. Z.ai pricing: $1.40/$4.40 input/output; $0.26 cached. Available on OpenRouter. "SWE-bench Pro 62.1 (vs GPT-5.5 58.6)". FrontierSWE 74.4%. MCP-Atlas 77.0%. "~5x–8x cheaper than Claude Opus 4.8 and ~1/6 of GPT-5.5 Pro for equivalent workloads." Tool-call parsing robust. 81.0 Terminal-Bench 2.1 score cited as proxy for shell-agent reliability. |
| Primary or Secondary | **Secondary** |
| Trust Level | **Medium** |
| Conflicts | None |

---

### SRC-011 — GLM-5.2 Complete Guide

| Field | Value |
|-------|-------|
| Title | GLM-5.2 Guide: Benchmarks, Pricing & How to Run (2026) |
| Publisher | CoderSera |
| URL | https://codersera.com/blog/glm-5-2-complete-guide-2026/ |
| Access Date | August 17, 2026 |
| Source Type | Secondary — technical guide |
| Models Covered | GLM-5.2 |
| Claims Supported | GLM-5.3 superseded GLM-5.2 on August 14, 2026. GLM-5.2 announced June 13, 2026; weights released ~June 17. GLM Coding Plan tiers (Lite/Pro/Max/Team). MIT license. Terminal-Bench 2.1: 51 (Artificial Analysis ranking). SWE-bench Pro 62.1% (VentureBeat Jun 2026). FrontierSWE 74.4%. |
| Primary or Secondary | **Secondary** |
| Trust Level | **Medium** |
| Conflicts | SRC-008/009 are higher-trust for architecture/benchmarks; CoderSera confirms GLM-5.3 release date |

---

### SRC-012 — Poolside Laguna S 2.1 Launch Blog

| Field | Value |
|-------|-------|
| Title | Introducing Laguna S 2.1 |
| Publisher | Poolside |
| URL | https://poolside.ai/blog/introducing-laguna-s-2-1 |
| Access Date | August 17, 2026 |
| Source Type | Official model announcement |
| Models Covered | Laguna S 2.1 (and comparison: Tencent Hy3, Inkling, Nemotron 3 Ultra, DeepSeek-V4-Pro Max, Kimi K3, Qwen 3.7 Max, Muse Spark 1.1, Claude Fable 5) |
| Claims Supported | Release: July 21, 2026. Architecture: 118B total / 8B active per token; MoE; 1M context. License: OpenMDW-1.1. BF16 + FP8 + INT4 + NVFP4 + GGUF + MLX variants. Terminal-Bench 2.1: 70.2%. SWE-bench Multilingual: 78.5%. SWE-bench Pro (Public): 59.4%. DeepSWE: 40.4%. Available on OpenRouter (free endpoint + 1M context paid), Baseten, Vercel AI Gateway. Full trajectories at trajectories.poolside.ai. |
| Primary or Secondary | **Primary** |
| Trust Level | **High** for availability/architecture/license; **Medium** for benchmarks (vendor-run; full trajectories disclosed) |
| Conflicts | None |

---

### SRC-013 — Poolside Laguna S 2.1 Developer Guide

| Field | Value |
|-------|-------|
| Title | Poolside Laguna S 2.1 Guide: Serving, API and Benchmarks |
| Publisher | agentpedia.codes |
| URL | https://agentpedia.codes/blog/poolside-laguna-s-2-1-developer-guide |
| Access Date | August 17, 2026 |
| Source Type | Secondary — developer guide with source reconciliation |
| Models Covered | Laguna S 2.1 |
| Claims Supported | OpenRouter paid model ID: `poolside/laguna-s-2.1`; context 1,048,576; max output 131,072; pricing $0.10/$0.20/$0.01 (in/out/cache). Benchmark comparability notes (different harnesses, budgets, and sandboxes across vendors). |
| Primary or Secondary | **Secondary** |
| Trust Level | **High** — author cross-checks against HuggingFace files and trajectory archive |
| Conflicts | None |

---

### SRC-014 — Devstral Official Launch Post (OpenHands)

| Field | Value |
|-------|-------|
| Title | Devstral: A New State-of-the-Art Open Model for Coding Agents |
| Publisher | All Hands AI |
| URL | https://www.openhands.dev/blog/devstral-a-new-state-of-the-art-open-model-for-coding-agents |
| Access Date | August 17, 2026 |
| Source Type | Official product/model announcement |
| Models Covered | Devstral Small 2505 |
| Claims Supported | 24B parameters; fine-tuned from Mistral-Small-3.1; Apache 2.0 license. SWE-bench Verified 46.8%. Runs on single RTX 4090 or 32GB RAM Mac. Mistral API model ID: `devstral-small-2505`; price $0.10/$0.30 (same as Mistral Small 3.1). Developed jointly by Mistral AI and All Hands AI. Compatible with OpenHands CodeActAgent. |
| Primary or Secondary | **Primary** |
| Trust Level | **High** |
| Conflicts | None |

---

### SRC-015 — Devstral HuggingFace Model Card

| Field | Value |
|-------|-------|
| Title | mistralai/Devstral-Small-2505 — HuggingFace |
| Publisher | Mistral AI |
| URL | https://huggingface.co/mistralai/Devstral-Small-2505 |
| Access Date | August 17, 2026 |
| Source Type | Official model card |
| Models Covered | Devstral Small 2505 |
| Claims Supported | Context window: 128K tokens. Vision encoder removed. Tekken tokenizer. OpenHands settings JSON example for configuration. Apache 2.0 license. |
| Primary or Secondary | **Primary** |
| Trust Level | **High** |
| Conflicts | None |

---

### SRC-016 — DeepInfra Tool Calling Documentation

| Field | Value |
|-------|-------|
| Title | Tool Calling — DeepInfra Docs |
| Publisher | DeepInfra |
| URL | https://docs.deepinfra.com/chat/tool-calling |
| Access Date | August 17, 2026 |
| Source Type | Official API documentation |
| Models Covered | Multiple models on DeepInfra (examples: DeepSeek-V3, Kimi-K2-Instruct) |
| Claims Supported | OpenAI-compatible tool calling API. Supports: single tool calls, parallel tool calls, tool_choice auto/none, streaming. Does not support: nested calls. K2 Vendor Verifier evaluation: top accuracy score for Kimi-K2-Instruct. Best practices for function calling (temperature <1.0, avoid system messages, keep tool list focused). |
| Primary or Secondary | **Primary** |
| Trust Level | **High** |
| Conflicts | None |

---

### SRC-017 — Qwen3 Coder 480B API Benchmarks (DeepInfra)

| Field | Value |
|-------|-------|
| Title | Qwen3 Coder 480B A35B API Benchmarks: Latency & Cost |
| Publisher | DeepInfra |
| URL | https://deepinfra.com/blog/qwen3-coder-480b-a35b-api-benchmarks |
| Access Date | August 17, 2026 |
| Source Type | Provider benchmark post |
| Models Covered | Qwen3 Coder 480B A35B Instruct |
| Claims Supported | Architecture: MoE 480B total / 35B active. 8 of 160 experts active. DeepInfra (Turbo, FP4): lowest blended price $0.41/M, TTFT 0.55s; recommended provider. DeepInfra (FP8): $0.70/M, 81.1 t/s. Eigen AI: 265.7 t/s but no function calling. Google Vertex: 172.6 t/s, 0.69s TTFT, $0.61/M, JSON Mode + Function Calling. |
| Primary or Secondary | **Primary** (provider self-benchmark) |
| Trust Level | **High** for provider-specific metrics; **Medium** for cross-provider comparisons |
| Conflicts | None |

---

### SRC-018 — Artificial Analysis — Qwen3 Coder Providers

| Field | Value |
|-------|-------|
| Title | Qwen3 Coder 480B A35B Instruct — Provider Analysis |
| Publisher | Artificial Analysis |
| URL | https://artificialanalysis.ai/models/qwen3-coder-480b-a35b-instruct/providers |
| Access Date | August 17, 2026 |
| Source Type | Independent benchmarking platform |
| Models Covered | Qwen3 Coder 480B A35B Instruct |
| Claims Supported | 6 providers: Google Vertex, Alibaba Cloud, DeepInfra (Turbo FP4), Amazon Bedrock, CoreWeave, Novita. DeepInfra FP4 lowest blended price $0.23/M, TTFT 0.55s. Google Vertex 163 t/s (fastest). 9.1× price spread across providers. |
| Primary or Secondary | **Secondary** (independent measurement) |
| Trust Level | **High** — Artificial Analysis is respected independent benchmark provider |
| Conflicts | Consistent with SRC-017 |

---

### SRC-019 — DeepSeek V4 Flash VentureBeat Analysis

| Field | Value |
|-------|-------|
| Title | DeepSeek's top-ranked V4 Flash stumbles on real agent tasks as its prices surge |
| Publisher | VentureBeat |
| URL | https://venturebeat.com/orchestration/deepseeks-top-ranked-v4-flash-stumbles-on-real-agent-tasks-as-its-prices-surge |
| Access Date | August 17, 2026 |
| Source Type | Investigative journalism with cited testing |
| Models Covered | DeepSeek V4 Flash |
| Claims Supported | Price increase announcement: V4 Flash off-peak $0.22/$0.66 (new rates effective August 16, 2026). Increase magnitude: 57%–371% depending on tier. Real-world agent task success: 53.8% (Composio testing; 30 workflows × 8 agents = 240 total runs; 129 passed). Beta label at research date. Quote: "cost per successfully completed workflow" as relevant metric. |
| Primary or Secondary | **Secondary** |
| Trust Level | **Medium-High** — reputable publication with specific testing methodology cited |
| Conflicts | None; consistent with SRC-002 for new pricing |

---

### SRC-020 — Fireworks vs DeepInfra Pricing Comparison

| Field | Value |
|-------|-------|
| Title | Fireworks AI vs DeepInfra (2026): DeepInfra Is 25-33% Cheaper Per Token |
| Publisher | MorphLLM |
| URL | https://www.morphllm.com/comparisons/fireworks-vs-deepinfra |
| Access Date | August 17, 2026 |
| Source Type | Secondary — pricing comparison |
| Models Covered | DeepSeek V4 Pro, Kimi K2.6, GLM-5.1 (cross-provider) |
| Claims Supported | DeepSeek V4 Pro: DeepInfra $1.30/$2.60; Fireworks $1.74/$3.48. Kimi K2.6: DeepInfra $0.75/$3.50; Fireworks $0.95/$4.00. GLM-5.1: DeepInfra $1.05/$3.50; Fireworks $1.40/$4.40. Fireworks: zero-retention, HIPAA+SOC2, 6000 RPM, batch 50% off. DeepInfra: zero-retention default, H100 $1.79/hr. |
| Primary or Secondary | **Secondary** |
| Trust Level | **High** — pricing confirmed against provider sites |
| Conflicts | GLM-5.1 pricing on DeepInfra ($1.05/$3.50) provides basis for GLM-5.1 cost estimates in Portfolio A |

---

### SRC-021 — Groq Performance Benchmarks

| Field | Value |
|-------|-------|
| Title | Groq Performance: Benchmarks, Latency & Limits 2026 |
| Publisher | ComparEdge |
| URL | https://comparedge.com/tools/groq/performance |
| Access Date | August 17, 2026 |
| Source Type | Secondary — performance analysis |
| Models Covered | Groq catalog: Llama 3.1 8B, Llama 3.3 70B, GPT-OSS-20B, GPT-OSS-120B, Qwen3.6 27B |
| Claims Supported | 11 open-weight models; uniform 131K context. All 11 support function calling and JSON mode. GPT-OSS-20B: 938 t/s. Llama 3.3 70B: 316 t/s (highest of tracked providers). Blended price range $0.05/M–$0.84/M. Llama 3.1 8B: $0.05/$0.08. |
| Primary or Secondary | **Secondary** |
| Trust Level | **Medium** |
| Conflicts | None |

---

### SRC-022 — Groq vs Cerebras vs SambaNova Comparison

| Field | Value |
|-------|-------|
| Title | Groq vs Cerebras vs SambaNova: Best AI Inference Provider 2026 |
| Publisher | CodeBrewTools |
| URL | https://codebrewtools.com/blogs/groq-vs-cerebras-vs-sambanova-best-inference-provider-2026 |
| Access Date | August 17, 2026 |
| Source Type | Secondary — comparison analysis |
| Models Covered | Llama 3.1 8B/70B/405B (cross-provider) |
| Claims Supported | Llama 3.1 8B: Groq $0.05/$0.08 (800+ tps); Cerebras $0.06/$0.06 (1800+ tps); SambaNova $0.06/$0.06 (1000+ tps). Llama 3.1 70B: Groq $0.59/$0.79 (250 tps); Cerebras $0.60/$0.60 (450 tps); SambaNova $0.52/$0.52 (460 tps). |
| Primary or Secondary | **Secondary** |
| Trust Level | **Medium** |
| Conflicts | None |

---

### SRC-023 — SambaNova Responses API Documentation

| Field | Value |
|-------|-------|
| Title | Responses API — SambaNova Docs |
| Publisher | SambaNova |
| URL | https://docs.sambanova.ai/docs/en/features/responses |
| Access Date | August 17, 2026 |
| Source Type | Official API documentation |
| Models Covered | gpt-oss-120b, MiniMax-M2.7 (on SambaNova) |
| Claims Supported | OpenAI Responses API compatible endpoint. Supports structured output via json_schema strict mode. Tool calling supported (quality improved with reasoning_effort=high for gpt-oss-120b). |
| Primary or Secondary | **Primary** |
| Trust Level | **High** |
| Conflicts | None |

---

### SRC-024 — Onyx AI Coding LLM Leaderboard

| Field | Value |
|-------|-------|
| Title | Best LLMs for Coding in 2026: SWE-bench, HumanEval, and LiveCode Rankings |
| Publisher | Onyx AI |
| URL | https://onyx.app/insights/best-llms-for-coding-2026 |
| Access Date | August 17, 2026 |
| Source Type | Secondary — curated leaderboard |
| Models Covered | Claude Fable 5, GPT-5.5, DeepSeek-V4-Pro, Kimi K2.6, DeepSeek-V4-Flash, MiniMax M3, Claude Opus 4.8 |
| Claims Supported | "Claude Fable 5 leads on autonomous bug-fixing with 95% SWE-bench Verified." "DeepSeek-V4-Pro leads on both bug-fixing and competitive programming, with 80.6% SWE-bench Verified and 93.5% LiveCodeBench under an MIT license." "Kimi K2.6 is the strongest open-weight model for agentic terminal work with 66.7% Terminal-Bench 2.0." DeepSeek-V4-Flash: $0.14/M input (pre-increase pricing). |
| Primary or Secondary | **Secondary** |
| Trust Level | **Medium** — leaderboard editorial; methodology partially disclosed |
| Conflicts | Terminal-Bench scores may use different versions (2.0 vs 2.1) across sources; do not compare directly |

---

### SRC-025 — BenchLM Coding Leaderboard

| Field | Value |
|-------|-------|
| Title | Best LLM for Coding (August 2026): SWE-bench & LiveCodeBench Ranked |
| Publisher | BenchLM.ai |
| URL | https://benchlm.ai/coding |
| Access Date | August 17, 2026 |
| Source Type | Secondary — curated leaderboard |
| Models Covered | Claude Mythos 5, Claude Fable 5, GPT-5.6 Sol, and 135 models total (51 Supported, 84 Estimated) |
| Claims Supported | Claude Mythos 5: BenchAlign score 81.1, SWE-bench Verified 95.5%. Claude Fable 5: 80.8, SWE-bench Verified 95%. GPT-5.6 Sol: 78.7. Kimi API pricing for K3 ($3.00/$15.00). Proprietary baseline context. |
| Primary or Secondary | **Secondary** |
| Trust Level | **Medium** |
| Conflicts | None |

---

### SRC-026 — SWE-Bench ProMax Academic Paper

| Field | Value |
|-------|-------|
| Title | SWE-Bench ProMax: Benchmarking Agents on Large-Scale Multilingual Code Refactoring |
| Publisher | arXiv |
| URL | https://arxiv.org/html/2608.09802 |
| Access Date | August 17, 2026 |
| Source Type | Academic preprint (peer review status unknown at access date) |
| Models Covered | GPT-5.2, Claude Sonnet 4.6, GLM-5, Qwen3.5, Kimi-K2.5 |
| Claims Supported | Benchmark: 170 instances; 7 languages; 70 repositories. All models run under OpenHands. GPT-5.2: 41.2% ($3.60/instance). Claude Sonnet 4.6: 38.8% ($4.77/instance). GLM-5: 36.5% ($0.24/instance). Qwen3.5: 36.5% ($0.78/instance). Kimi-K2.5: 32.9% ($0.72/instance). Key finding: "Open-weight models are competitive with proprietary ones at a fraction of the cost." Model improves markedly moving from mini-swe-agent to OpenHands. |
| Primary or Secondary | **Primary** (independent academic evaluation) |
| Trust Level | **High** — independent; methodology disclosed; full dataset described |
| Conflicts | GLM-5 (older model) used; GLM-5.2 likely scores higher but not yet measured in this benchmark |

---

### SRC-027 — Kilo.ai Open Source Model Rankings

| Field | Value |
|-------|-------|
| Title | Best Open Source AI Models for Coding (2026) |
| Publisher | Kilo.ai |
| URL | https://kilo.ai/open-source-models |
| Access Date | August 17, 2026 |
| Source Type | Secondary — editorial model ranking |
| Models Covered | GLM-5.2, Qwen3 Coder 480B, Kimi K3, Devstral Small 2505, Laguna S 2.1 |
| Claims Supported | "GLM-5.2 is our current overall pick for long-horizon coding agents." Kimi K3 Terminal-Bench 2.1: 88.3%. Devstral Small SWE-bench Verified: 46.8%. Laguna S 2.1 SWE-Bench Multilingual: 78.5%. GLM-5.2 SWE-bench Pro: 62.1%. Qwen3 Coder 480B SWE-bench Pro: 38.7%. |
| Primary or Secondary | **Secondary** |
| Trust Level | **High** — editorial is based on primary sources and specific artifact tracking |
| Conflicts | None |

---

### SRC-028 — Fireworks vs Together AI Pricing

| Field | Value |
|-------|-------|
| Title | Fireworks vs Together AI Pricing (2026) |
| Publisher | MorphLLM |
| URL | https://www.morphllm.com/comparisons/fireworks-vs-together |
| Access Date | August 17, 2026 |
| Source Type | Secondary — pricing comparison |
| Models Covered | DeepSeek V4 Pro, Kimi K2.6, GLM-5.1, GPT-OSS-120B, Qwen3.6 Plus, MiniMax M2.7 (cross-provider) |
| Claims Supported | Fireworks cheaper than Together on most models. Together cheaper on H100 dedicated ($6.49 vs $7.00). Together offers HGX clusters from $3.99/hr reserved. Together AI: DeepSeek V4 Pro $2.10/M; Kimi K2.6 $1.20/M. |
| Primary or Secondary | **Secondary** |
| Trust Level | **High** |
| Conflicts | None |

---

### SRC-029 — OpenRouter Models Catalog

| Field | Value |
|-------|-------|
| Title | Compare AI Models: Pricing, Context & Benchmarks |
| Publisher | OpenRouter |
| URL | https://openrouter.ai/models |
| Access Date | August 17, 2026 |
| Source Type | Official provider catalog |
| Models Covered | 400+ models including Qwen3.6 27B, Laguna S 2.1, GLM-5.x, MiniMax M3, Kimi K2.x, Devstral, Seed 2.1 Turbo (ByteDance), voyage-code-4 |
| Claims Supported | OpenRouter model IDs and pricing. Qwen3.6 27B: multiple providers listed ($0.289–$0.60). Laguna S 2.1: $0.10/$0.20/$0.01. OpenRouter Pareto Code Router for automated cost/quality routing. 400+ models; 70+ providers. Free tier: 50 req/day; 1000/day with $10 deposit. |
| Primary or Secondary | **Primary** |
| Trust Level | **High** |
| Conflicts | None |

---

### SRC-030 — Zhipu AI GLM-5.2 Press (The Decoder)

| Field | Value |
|-------|-------|
| Title | Zhipu AI's GLM-5.2 closes in on closed-source leaders in coding marathons |
| Publisher | The Decoder |
| URL | https://the-decoder.com/zhipu-ais-glm-5-2-closes-in-on-closed-source-leaders-in-coding-marathons/ |
| Access Date | August 17, 2026 |
| Source Type | Technology journalism |
| Models Covered | GLM-5.2 (comparison to Claude Opus 4.8, GPT-5.5, Gemini) |
| Claims Supported | FrontierSWE: GLM-5.2 74.4% (one point behind Claude Opus 4.8). Terminal-Bench 2.1: 81.0 (within few points of Claude Opus 4.8). MIT license with no regional restrictions. Available via Z.ai, ZCode, Claude Code integrations. Supports vLLM, SGLang, Transformers, xLLM, ktransformers for deployment. |
| Primary or Secondary | **Secondary** |
| Trust Level | **Medium** |
| Conflicts | None |

---

### SRC-031 — ByteDance Seed 2.1 Analysis

| Field | Value |
|-------|-------|
| Title | ByteDance Seed 2.1 Pro & Turbo: benchmarks and price |
| Publisher | DataNorth |
| URL | https://datanorth.ai/news/bytedance-releases-seed-2-1-pro-and-seed-2-1-turbo |
| Access Date | August 17, 2026 |
| Source Type | Technology news |
| Models Covered | Seed 2.1 Pro, Seed 2.1 Turbo |
| Claims Supported | Seed 2.1 is ByteDance's latest LLM family. Not open-weight. API-only via Volcano Engine / Volcano Ark. No parameter count disclosed. Proprietary. 180 trillion daily token calls (Doubao family). Available: Volcano Engine platform. |
| Primary or Secondary | **Secondary** |
| Trust Level | **Medium** |
| Conflicts | Confirms Seed 2.1 is proprietary and China-cloud only — consistent with rejection rationale in Section 6 |

---

### SRC-032 — DeepSeek vs Qwen Comparison

| Field | Value |
|-------|-------|
| Title | DeepSeek vs Qwen (2026): Live Tests, Pricing & Models |
| Publisher | chat-deep.ai |
| URL | https://chat-deep.ai/comparison/qwen/ |
| Access Date | August 17, 2026 |
| Source Type | Secondary — comparison analysis |
| Models Covered | DeepSeek V4 Pro, DeepSeek V4 Flash, Qwen3.7-Max, Qwen3.7-Flash, Qwen3.6-27B, Qwen3.6-35B-A3B |
| Claims Supported | deepseek-v4-pro: 1M context; MIT. deepseek-v4-flash: 1M context; MIT. qwen3.7-max: proprietary API-only. Open-weight Qwen: Qwen3.6-27B and Qwen3.6-35B-A3B for self-hosting. Deprecation notice: deepseek-v3/r1 series will be deprecated October 10, 2026 on QwenCloud. |
| Primary or Secondary | **Secondary** |
| Trust Level | **Medium** |
| Conflicts | None |

---

### SRC-033 — DeepSeek API Official Change Log

| Field | Value |
|-------|-------|
| Title | Change Log — DeepSeek API Docs |
| Publisher | DeepSeek |
| URL | https://api-docs.deepseek.com/updates/ |
| Access Date | August 17, 2026 |
| Source Type | Official API changelog |
| Models Covered | deepseek-v4-pro, deepseek-v4-flash, deepseek-v3.2-speciale (historical) |
| Claims Supported | V4-Pro GA: benchmark scores HLE (wo/w tools) 42.7/60.0; Terminal Bench 2.1 57.9; DeepSWE 62.7; Toolathlon-Verified 74.1. V4-Flash public beta announced. Responses API support for both V4 models. Anthropic API format support. FIM completion (non-thinking mode only). |
| Primary or Secondary | **Primary** |
| Trust Level | **High** |
| Conflicts | None |

---

### SRC-034 — Qwen3.6 27B on OpenRouter

| Field | Value |
|-------|-------|
| Title | Qwen3.6 27B — API Pricing & Benchmarks |
| Publisher | OpenRouter |
| URL | https://openrouter.ai/qwen/qwen3.6-27b |
| Access Date | August 17, 2026 |
| Source Type | Official provider model page |
| Models Covered | Qwen3.6 27B |
| Claims Supported | Dense 27B parameters. Release: April 2026. Context: 262,144. Multimodal: text, image, video. 201 languages. Thinking mode support. Provider pricing: Chutes $0.30/$2.00; DeepInfra $0.32/$3.20; CoreWeave $0.60/$3.60; Morph $0.289/$2.40; io.net $0.31/$2.19; SiliconFlow $0.30/$3.20. Artificial Analysis Coding Index: 53.7. |
| Primary or Secondary | **Primary** |
| Trust Level | **High** |
| Conflicts | None |

---

### SRC-035 — OpenHands Local LLM Recommendations

| Field | Value |
|-------|-------|
| Title | Local LLMs — OpenHands Docs |
| Publisher | All Hands AI |
| URL | https://docs.openhands.dev/openhands/usage/llms/local-llms |
| Access Date | August 17, 2026 |
| Source Type | Official documentation |
| Models Covered | Qwen3.6-35B-A3B |
| Claims Supported | "As of 2026/05/21: We now recommend Qwen3.6-35B-A3B as the first local model to try with OpenHands." (Local recommendation; relevant context for hosted comparison.) |
| Primary or Secondary | **Primary** |
| Trust Level | **High** |
| Conflicts | This is local LLM guidance; excluded from hosted recommendations per hard constraint |

---

*Ledger entries: 35 sources. Last verified: August 17, 2026. For claims not covered by this ledger, see inline source notes in `hosted-open-model-landscape.md`.*
