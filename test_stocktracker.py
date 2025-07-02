# test_stocktracker.py

import unittest
import pandas as pd
import stocktracker

class TestStockTracker(unittest.TestCase):

    def test_stock_data_returns_dataframe(self):
        #stock_data should return a pandas DataFrame."""
        df = stocktracker.stock_data("TSLA")
        self.assertIsInstance(df, pd.DataFrame)

    def test_stock_data_has_at_most_seven_rows(self):
        #stock_data should return at most 7 rows (last 7 days).
        df = stocktracker.stock_data("AAPL")
        self.assertLessEqual(len(df), 7)

    def test_genai_analysis_returns_string(self):
        #genai_analysis should return a non-empty string.
        text = stocktracker.genai_analysis("NVDA")
        self.assertIsInstance(text, str)
        self.assertTrue(len(text) > 0)

if __name__ == "__main__":
    unittest.main()


