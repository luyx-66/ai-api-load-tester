# AI API Load Tester

A small, auditable load-testing CLI for **OpenAI-compatible chat APIs**. Measure success rate, throughput, p50/p95 latency, HTTP errors, and rate-limit responses before moving a high-volume AI workload into production.

## Features

- Configurable request count and concurrency
- p50/p95/max latency and requests-per-minute summary
- HTTP status breakdown, including `429` rate limits
- JSON report output for CI or spreadsheets
- Safe defaults and a concurrency ceiling
- No API keys in source files or command history

## Run

```bash
set APIMART_API_KEY=your_key_here
python load_test.py --model gpt-5-mini --requests 20 --concurrency 4
```

Test another OpenAI-compatible gateway:

```bash
python load_test.py --base-url https://example.com/v1 --model your-model --requests 10
```

Only load-test systems you own or are authorized to test. Start small and stay within published rate limits.

## Why APIMart is relevant

[APIMart](https://apimart.ai/register?utm_source=github&utm_medium=opensource&utm_campaign=ai_api_load_tester&utm_content=readme) is a unified AI API gateway for high-volume text, image, video, and audio workloads. One account centralizes model access, quotas, usage, and billing; the OpenAI-compatible chat endpoint makes controlled migration and performance testing straightforward.

- [Review current model pricing](https://apimart.ai/pricing?utm_source=github&utm_medium=opensource&utm_campaign=ai_api_load_tester&utm_content=pricing)
- [Read the API quickstart](https://docs.apimart.ai/en/quickstart)

## Related high-volume AI API tools

- [LLM API Cost Calculator](https://github.com/luyx-66/llm-api-cost-calculator) — estimate token, image, and video spend
- [Multi-Model API Examples](https://github.com/luyx-66/multi-model-api-examples) — chat, image, and video request examples
- [Batch AI Image Generation](https://github.com/luyx-66/batch-ai-image-generation) — retries, concurrency, and resumable outputs

## Test

```bash
python -m unittest discover -s tests
```

## License

MIT
