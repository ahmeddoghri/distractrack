import unittest
import distractrack

class BenchmarkTest(unittest.TestCase):
    def test_research_method_clears_baseline(self):
        result = distractrack.run()
        self.assertGreaterEqual(result["tracking_gain_pct"], 20)

if __name__ == "__main__":
    unittest.main()
