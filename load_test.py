"""Authorized load tester for OpenAI-compatible chat completion endpoints."""

from __future__ import annotations

import argparse
import json
import os
import statistics
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed


def percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((len(ordered) - 1) * fraction)))
    return ordered[index]


def summarize(results: list[dict], wall_seconds: float) -> dict:
    latencies = [item["latency_ms"] for item in results]
    statuses = Counter(str(item["status"]) for item in results)
    successes = sum(1 for item in results if 200 <= item["status"] < 300)
    return {
        "requests": len(results),
        "successes": successes,
        "success_rate": round(successes / len(results), 4) if results else 0,
        "requests_per_minute": round(len(results) / wall_seconds * 60, 2) if wall_seconds else 0,
        "latency_ms": {
            "mean": round(statistics.fmean(latencies), 2) if latencies else 0,
            "p50": round(percentile(latencies, 0.50), 2),
            "p95": round(percentile(latencies, 0.95), 2),
            "max": round(max(latencies), 2) if latencies else 0,
        },
        "statuses": dict(statuses),
    }


def send_request(url: str, api_key: str, payload: dict, timeout: float) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response.read()
            status = response.status
    except urllib.error.HTTPError as error:
        error.read()
        status = error.code
    except Exception:
        status = 0
    return {"status": status, "latency_ms": (time.perf_counter() - started) * 1000}


def main() -> None:
    parser = argparse.ArgumentParser(description="Load-test an authorized OpenAI-compatible API endpoint.")
    parser.add_argument("--base-url", default=os.getenv("AI_API_BASE_URL", "https://api.apimart.ai/v1"))
    parser.add_argument("--model", required=True)
    parser.add_argument("--requests", type=int, default=10)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--timeout", type=float, default=60)
    parser.add_argument("--prompt", default="Reply with the single word OK.")
    parser.add_argument("--output", help="Optional JSON report path")
    args = parser.parse_args()

    if not 1 <= args.requests <= 10_000:
        parser.error("--requests must be between 1 and 10000")
    if not 1 <= args.concurrency <= 100:
        parser.error("--concurrency must be between 1 and 100")
    api_key = os.getenv("APIMART_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        parser.error("Set APIMART_API_KEY or OPENAI_API_KEY in the environment")

    url = f"{args.base_url.rstrip('/')}/chat/completions"
    payload = {"model": args.model, "messages": [{"role": "user", "content": args.prompt}], "max_tokens": 8}
    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        futures = [executor.submit(send_request, url, api_key, payload, args.timeout) for _ in range(args.requests)]
        results = [future.result() for future in as_completed(futures)]
    report = summarize(results, time.perf_counter() - started)
    rendered = json.dumps(report, indent=2)
    print(rendered)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\n")


if __name__ == "__main__":
    main()
