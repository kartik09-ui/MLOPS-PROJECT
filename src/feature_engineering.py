import os
import pandas as pd
from  sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from utils.helpers import *
import sys

logger = get_logger(__name__)

class FeatureEngineer:
    def __init__(self):
        self.data_path = PROCESSED_DATA_PATH
        self.df = None
        self.label_mapping={}

    def load_data(self):
        try:
            logger.info("Loading Data")
            self.df = pd.read_csv(self.data_path)
            logger.info("Data loaded successfully")
        except Exception as e:
            logger.error(f"Error while loading data : {e}")
            raise CustomException("Error while loading data" , sys)
        
    def feature_construction(self):
        try:
            logger.info("Starting Feature construction")
            self.df['Total Delay'] = self.df['Departure Delay in Minutes'] + self.df['Arrival Delay in Minutes']
            self.df['Delay Ratio'] = self.df['Total Delay'] / (self.df['Flight Distance'] + 1)

            logger.info("Feature Cuntruction done successfully")
        except Exception as e:
            logger.error(f"Error while feature construction : {e}")
            raise CustomException("Error while feature construction" , sys)
        
    def binning(self):
        try:
            logger.info("Starting Binning of age column")
            self.df['Age Group'] = pd.cut(self.df['Age'], bins=[0,18,30,50,100], labels=['Child', 'Youngster', 'Adult', 'Senoir'])
            logger.info("Binning of Age Column successfully")
        except Exception as e:
            logger.error(f"Error while Binning : {e}")
            raise CustomException("Error while Binning" , sys)
        
    def label_encoding(self):
        try:
            columns_to_encode = ['Gender', 'Customer Type', 'Type of Travel', 'Class', 'satisfaction', 'Age Group']
            logger.info(f"Performing label encoding on {columns_to_encode}")

            self.df , self.label_mapping = label_encode(self.df , columns_to_encode )
            
            for col, mapping in self.label_mapping.items():
                logger.info(f"Mapping for {col} : {mapping}")
            logger.info("Label encoding successfull !")
        except Exception as e:
            logger.error(f"Error while label encoding : {e}")
            raise CustomException("Error while label encoding" , sys)
        
    def feature_selection(self):
        try:
            logger.info("Starting Feature Selection")
            X = self.df.drop(columns = 'satisfaction')
            y = self.df['satisfaction'] 

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
            mutual_info = mutual_info_classif(X_train, y_train, discrete_features = True)
            mutual_info_df = pd.DataFrame({
                'Feature': X.columns,
                'Mutual Information': mutual_info
            }).sort_values(by='Mutual Information', ascending=False)
            logger.info(f"Mutual Information table is : \n{mutual_info_df} ")
            top_features = mutual_info_df.head(12)['Feature'].tolist()
            self.df = self.df[top_features + ['satisfaction']]
            logger.info(f"Top features : {top_features}")
            logger.info("Feature selection is successfull")
        except Exception as e:
            logger.error(f"Error while feature selection: {e}")
            raise CustomException("Error while feature selection" , sys)
        
    def save_data(self):
        try:
            logger.info("Saving your data...")
            os.makedirs(ENGINEERED_DIR,exist_ok=True)
            self.df.to_csv(ENGINEERED_DATA_PATH, index=False)
            logger.info(f"Data saved successfully at {ENGINEERED_DATA_PATH}")
        except Exception as e:
            logger.error(f"Error while saving data: {e}")
            raise CustomException("Error while saving data" , sys)
        
    def run(self):
        try:
            logger.info("Starting your feature engineering pipeline")
            self.load_data()
            self.feature_construction()
            self.binning()
            self.label_encoding()
            self.feature_selection()
            self.save_data()
            logger.info("Your Feature Engineering pipeline successfully done..")
        except Exception as e:
            logger.error(f"Error while running FE pipeline: {e}")
            raise CustomException("Error while running FE pipeline" , sys)
        
        finally:
            logger.info("End of FE Pipeline")

if __name__=="__main__":
    feature_engineer = FeatureEngineer()
    feature_engineer.run()
        

        