from data_pipeline.pipeline import DataPipeline

if __name__ == "__main__":
    pipeline = DataPipeline("data/titanic_raw.csv", "data/titanic_clean.csv")
    pipeline.read_csv()
    pipeline.clean_data()
    pipeline.write_csv()
