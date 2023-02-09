import sys, os

from pandas import DataFrame
from sklearn.pipeline import Pipeline

from sensor.logger.exception import SensorException
from sensor.logger import logging

from sensor.constant.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME


class TargetValueMapping:
    def __init__(self):
        self.neg: int = 0

        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()

        return dict(zip(mapping_response.values(), mapping_response.keys()))


class SensorModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        self.preprocessing_object = preprocessing_object

        self.trained_model_object = trained_model_object

    def predict(self, dataframe: DataFrame) -> DataFrame:
        logging.info("Entered predict method of SensorTruckModel class")

        try:
            logging.info("Using the trained model to get predictions")

            transformed_feature = self.preprocessing_object.transform(dataframe)

            logging.info("Used the trained model to get predictions")

            return self.trained_model_object.predict(transformed_feature)

        except Exception as e:
            raise SensorException(e, sys) from e

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"

class ModelResolver:
    def __init__(self, model_dir = SAVED_MODEL_DIR):
        try:
            self.model_dir = model_dir
            os.makedirs(model_dir, exist_ok=True)
            self.timestamps = list(map(int, os.listdir(self.model_dir)))

        except Exception as e:
            raise SensorException(e, sys)

    def get_latest_model_path(self) :
        try:
            if len(self.timestamps) > 0:
                latest_timestamp = max(self.timestamps)
                latest_model_path = os.path.join(self.model_dir, f"{latest_timestamp}", MODEL_FILE_NAME)
                return latest_model_path
            else:
                logging.info(f"There are no saved model available at {self.model_dir}")
                return None
        except Exception as e:
            raise SensorException(e, sys)

    def is_model_exists(self) -> bool:
        latest_model_path = self.get_latest_model_path()
        try:
            if not os.path.exists(self.model_dir) or latest_model_path is None or not os.path.exists(latest_model_path):
                return False
            else:
                logging.info(f"Saved model timestamps found: {self.timestamps}")
                return True
        except Exception as e:
            raise e 
