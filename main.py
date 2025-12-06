from data_pipeline.pipeline import DataPipeline

if __name__ == "__main__":
    pipeline = DataPipeline(
        input_file="data/titanic_raw.csv",
        output_file="data/titanic_clean.csv"
    )
    pipeline.run()
