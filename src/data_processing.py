import pandas as pd
from config.path_config import *
from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

class DataProcessor:

    def __init__(self):
        self.train_path = TRAIN_DATA_PATH
        self.processed_data_path = PROCESSED_DATA_PATH

    def load_data(self):
        try:
            logger.info("Data Processing started")
            df = pd.read_csv(self.train_path)
            logger.info(f"Data read successfull : Data shape : {df.shape}")
            return df
        except Exception as e:
            logger.error("Problem while  Loading Data")
            raise CustomException("Error while loading data: ",sys)
        
    def drop_unnecessary_columns(self, df, columns):
        try:
            logger.info(f"Dropping unnecessary colunms : {columns}")
            df = df.drop(columns = columns, axis=1)
            logger.info(f"Columns dropped successfully : Shape = {df.shape}")
            return df
        except Exception as e:
            logger.error("Problem while  Dropping Columns")
            raise CustomException("Error while Dropping Columns: ",sys)
        
    def handle_outliers(self, df, columns):
        try:
            logger.info(f"Handling Outliers : Colmns = {columns}")
            for column in columns:
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)
                IQR = Q3 - Q1

                lower_bound = Q1 - 1.5 *IQR
                upper_bound = Q3 + 1.5 * IQR
                df[column] = df [column].clip(lower = lower_bound, upper = upper_bound)
            logger.info(f"Outliers handle successfully : {df.shape}")
            return df
        except Exception as e:
            logger.error("Problem while  Outlier Handling")
            raise CustomException("Error while Outlier Handling: ",sys)
        
    def handle_null_values(self, df, columns):
        try:
            logger.info("Handling null vlaues")
            df[columns] = df[columns].fillna(df[columns].median()) ## if multiple columns has null values then apply it with loop
            logger.info(f"Missing values handled successfully : shape = {df.shape}")
            return df
        except Exception as e:
            logger.error("Problem while  null values Handling")
            raise CustomException("Error while Null Values Handling: ",sys)
        
    def save_data(self, df):
        try:
            os.makedirs(PROCESSED_DIR , exist_ok=True)
            df.to_csv(self.processed_data_path, index=False)
            logger.info("Processed data saved successfully")
        except Exception as e:
            logger.error("Problem while saving data")
            raise CustomException("Error while saving data : ", sys)
        
    def run(self):
        try:
            logger.info("Starting the pipeline of Data Processing")
            df = self.load_data()
            df = self.drop_unnecessary_columns(df, ["MyUnknownColumn", "id"])
            columns_to_handle =['Flight Distance','Departure Delay in Minutes','Arrival Delay in Minutes','Checkin service']
            df = self.handle_outliers(df, columns_to_handle)
            df = self.handle_null_values(df, 'Arrival Delay in Minutes')
            self.save_data(df)
            logger.info("Data Processing Pipeline Completed Successfully")

        except CustomException as ce:
            logger.error(f"Error occured in Data Processing Pipeline : {str(ce)}")


if __name__ == "__main__":
    processor = DataProcessor()
    processor.run()