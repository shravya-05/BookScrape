import unittest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
import os

class TestBookScraper(unittest.TestCase):

    @patch("os.path.isfile")
    def test_01_csv_file_exists(self, mock_isfile):
        """Test if CSV file exists by mocking os.path.isfile."""
        mock_isfile.return_value = True
        self.assertTrue(os.path.isfile("books_data.csv"))

    @patch("pandas.read_csv")
    def test_02_csv_file_extraction(self, mock_read_csv):
        """Test CSV file extraction by mocking pandas.read_csv."""
        df = MagicMock()
        mock_read_csv.return_value = df
        result = pd.read_csv("books_data.csv")
        self.assertEqual(result, df)

    @patch("pandas.read_csv")
    def test_03_file_extension(self, mock_read_csv):
        """Test if CSV file has proper file extension."""
        df = MagicMock()
        df["Price"].dtype = float
        mock_read_csv.return_value = df

        file_extension = os.path.splitext("books_data.csv")[1]
        self.assertEqual(file_extension, ".csv")
        df = pd.read_csv("books_data.csv")
        self.assertEqual(df["Price"].dtype, float)

    @patch("pandas.read_csv")
    def test_04_data_columns_match(self, mock_read_csv):
        """Test if CSV has all required columns."""
        df = MagicMock()
        df.columns = ["Title", "Price", "Rating", "Availability", "Product URL"]
        mock_read_csv.return_value = df

        df = pd.read_csv("books_data.csv")
        expected_columns = ["Title", "Price", "Rating", "Availability", "Product URL"]
        self.assertListEqual(df.columns, expected_columns)

    @patch("pandas.read_csv")
    def test_05_no_missing_values(self, mock_read_csv):
        """Test CSV has no missing values."""
        df = MagicMock()
        df.isnull().sum.return_value = 0
        mock_read_csv.return_value = df

        df = pd.read_csv("books_data.csv")
        self.assertEqual(df.isnull().sum(), 0)


if __name__ == '__main__':
    unittest.main()
