import unittest

from load_test import percentile, summarize


class LoadTestTests(unittest.TestCase):
    def test_percentile(self):
        self.assertEqual(percentile([10, 20, 30, 40, 50], 0.95), 50)

    def test_summary(self):
        report = summarize([
            {"status": 200, "latency_ms": 100},
            {"status": 200, "latency_ms": 200},
            {"status": 429, "latency_ms": 50},
        ], 2)
        self.assertEqual(report["successes"], 2)
        self.assertEqual(report["statuses"]["429"], 1)
        self.assertEqual(report["requests_per_minute"], 90)


if __name__ == "__main__":
    unittest.main()
