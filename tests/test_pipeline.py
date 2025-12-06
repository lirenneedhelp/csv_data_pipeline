import unittest
from data_pipeline.pipeline import DataPipeline
from data_pipeline.pipeline import to_float

class TestDataPipeline(unittest.TestCase):

    def setUp(self):
        # Create a tiny sample dataset for testing
        with open("test.csv", "w") as f:
            f.write(
                "X,X,X,X\n"
                "sn,age,embarked,fare,date\n"
                "1,22,S,7.25,01-Jan-90\n"
                "2,,Q,8.05,01-Jan-90\n"
                "3,35,,,\n"
            )

        self.pipeline = DataPipeline("test.csv", "cleaned_test.csv")
        self.pipeline.read_csv()

    def test_fill_columns(self):
        # No empty column names here, should return False
        result = self.pipeline.fill_columns()
        self.assertFalse(result)

    def test_clean_age(self):
        self.pipeline.clean_age()
        age_idx = self.pipeline.header.index("age")

        ages = [row[age_idx] for row in self.pipeline.data]
        self.assertTrue(all(isinstance(a, int) for a in ages))

    def test_clean_embarked(self):
        self.pipeline.clean_embarked()
        embarked_idx = self.pipeline.header.index("embarked")

        self.assertTrue(all(row[embarked_idx] != "" for row in self.pipeline.data))

    def test_to_float(self):
        self.assertEqual(to_float("3.14"), 3.14)
        self.assertEqual(to_float("abc", 99), 99)

if __name__ == "__main__":
    unittest.main()
