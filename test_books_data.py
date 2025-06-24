import unittest
import os
import pandas as pd

class TestBookScraper(unittest.TestCase):

    def setUp(self):
        self.filename = "books_data.csv"


    def test_01_csv_file_exists(self):
        """test Case 1: check if csv file exists"""
        print("books_data.csv exists:", os.path.isfile("books_data.csv"))  #should return True

  
    def test_02_csv_file_extraction(self):
        """test case 2:verify csv file extraction"""
        try:
            df = pd.read_csv(self.filename)
            print("\nFirst 5 rows of the dataset:\n", df.head())  
            self.assertIsInstance(df, pd.DataFrame)
        except Exception as e:
            self.fail(f"CSV extraction failed: {e}")
   
   
    def test_03_file_extension(self):
        """test Case 3: verify fileType and datatype"""
        df = pd.read_csv("books_data.csv")
        print("File extension:", os.path.splitext("books_data.csv")[1])  # Should return '.csv'
        print(df["Price"].dtype)  #should be 'float'    
              

    def test_04_data_columns_match(self):
        """test case 4: validate required columns exist"""
        df = pd.read_csv(self.filename)
        expected_columns = ["Title", "Price", "Rating", "Availability", "Product URL"]
        print(df.columns.tolist() == expected_columns)  #should return True

    def test_05_no_missing_values(self):
        """Test Case 5: Handle Missing or Invalid Data"""
        df = pd.read_csv(self.filename)
        print(df.isnull().sum())  #should show zero missing values

if __name__ == '__main__':
    unittest.main()
