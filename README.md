# ☕ Café Aurora Prompt Bench

36 single-file landing pages, 4 models, 1 question: **what makes AI actually try harder?**

- 🌐 Live: https://calneymgp.github.io/cafe-aurora-prompt-bench/
- Same task (coffee-shop landing, 7 requirements) × 26 runs `muse-spark-1.3` + 10 runs via OpenRouter (`deepseek-v4.1-flash`, `glm-5.3-flash`, `gemini-3.8-flash`, thinking=max)
- Ranked by full-page audit score (0–10, desktop + mobile + code)
- Prompts byte-identical per bench; telemetry re-extracted with a single per-turn-sum rule

**Findings:** emotional appeal doesn't work (5.5–7.0) · explicit bar + numeric self-gate wins on every model · model self-scores inflate (3× self-declared "≥9.5", external ceiling 9.0)
