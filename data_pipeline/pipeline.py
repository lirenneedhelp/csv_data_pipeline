import csv
import statistics
import logging

from data_pipeline.utils import to_float

# -----------------------------
# Logging Configuration
# -----------------------------
logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,  # DEBUG for more verbosity
    format="%(asctime)s [%(levelname)s] %(message)s",
)


class DataPipeline:
    def __init__(self, input_file: str, output_file: str):
        self.input_file = input_file
        self.output_file = output_file
        self.header = []
        self.data = []

        logging.info(f"Initialized DataPipeline with input={input_file}, output={output_file}")

    def read_csv(self) -> bool:
        """Read CSV file with error handling."""
        try:
            with open(self.input_file, mode="r", newline="") as csv_file:
                csv_reader = csv.reader(csv_file)
                self.data = [[cell.strip() for cell in row] for row in csv_reader]

                self.header = self.data[1]  # header row
                self.data = self.data[2:]   # data rows

                logging.info("CSV read successfully.")
                return True

        except FileNotFoundError:
            logging.error(f"File not found: {self.input_file}")
            return False
        
        except UnicodeDecodeError:
            logging.error("Unicode decode error in file.")
            return False

    def fill_columns(self) -> bool:
        """Fill empty column names."""

        changed = False
        for idx, col in enumerate(self.header):
            if col == "":
                self.header[idx] = "name"
                changed = True
                logging.warning(f"Filled missing column name at index {idx}.")
        
        return changed

    def clean_data(self):
        """Run all cleaning functions."""
        logging.info("Cleaning dataset...")

        self.clean_age()
        self.clean_embarked()
        self.clean_fare()
        self.clean_date()

        # Remove duplicates
        seen = set()
        unique_data = []
        for row in self.data:
            t = tuple(row)
            if t not in seen:
                seen.add(t)
                unique_data.append(row)

        removed = len(self.data) - len(unique_data)
        logging.info(f"Removed {removed} duplicate rows.")

        self.data = unique_data

    def write_csv(self):
        """Write cleaned CSV."""
        try:
            with open(self.output_file, mode="w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(self.header)
                writer.writerows(self.data)

            logging.info(f"Successfully wrote cleaned data to {self.output_file}")

        except Exception as e:
            logging.error(f"Failed to write CSV: {e}")

    # --------------------------
    # Cleaning Functions
    # --------------------------

    def clean_age(self):
        age_idx = self.header.index("age")
        ages = []

        for row in self.data:
            try:
                val = int(row[age_idx])
                ages.append(val)
                row[age_idx] = val
            except ValueError:
                pass

        median_age = statistics.median(ages)
        logging.info(f"Median age calculated: {median_age}")

        for row in self.data:
            try:
                row[age_idx] = int(row[age_idx])
            except ValueError:
                logging.debug(f"Replacing missing age with median for row: {row}")
                row[age_idx] = int(median_age)

    def clean_embarked(self):
        embarked_idx = self.header.index("embarked")
        for row in self.data:
            if row[embarked_idx] == "":
                logging.debug(f"Filling missing embarked with 'S' for row: {row}")
                row[embarked_idx] = "S"

    def clean_fare(self):
        fare_idx = self.header.index("fare")
        fares = []

        for row in self.data:
            val = to_float(row[fare_idx])
            if val is not None:
                fares.append(val)
                row[fare_idx] = val

        median_fare = statistics.median(fares)
        logging.info(f"Median fare calculated: {median_fare}")

        for row in self.data:
            row[fare_idx] = to_float(row[fare_idx], median_fare)

    def clean_date(self):
        date_idx = self.header.index("date")
        before = len(self.data)
        self.data = [row for row in self.data if row[date_idx] != ""]
        removed = before - len(self.data)
        logging.info(f"Removed {removed} rows due to missing date.")
