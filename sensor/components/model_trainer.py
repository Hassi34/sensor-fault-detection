import sys

from sensor.ml.metric import calculate_metric

from sensor.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact,
)
from sensor.entity.config_entity import ModelTrainerConfig
from sensor.logger.exception import SensorException
from sensor.logger import logging
from sensor.ml.metric import calculate_metric
from sensor.ml.model.estimator import SensorModel
from sensor.utils.main_utils import load_numpy_array_data, load_object, save_object
from xgboost import XGBClassifier

class ModelTrainer:
    def __init__(self,
        data_transformation_artifact: DataTransformationArtifact,
        model_trainer_config: ModelTrainerConfig):

        self.data_transformation_artifact = data_transformation_artifact

        self.model_trainer_config = model_trainer_config

    def train_model(self, x_train, y_train):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x_train, y_train)
            logging.info("Created Sensor truck model object")
            return xgb_clf

        except Exception as e:
            raise SensorException(e, sys)

    def preform_hyper_param_tuning(self):...

    def initiate_model_trainer(self,) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            train_arr = load_numpy_array_data(
                file_path=self.data_transformation_artifact.transformed_train_file_path
            )

            test_arr = load_numpy_array_data(
                file_path=self.data_transformation_artifact.transformed_test_file_path
            )

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model = self.train_model(x_train, y_train)
            classification_train_metric = calculate_metric(model, x_train, y_train)
            classification_test_metric = calculate_metric(model, x_test, y_test)
            print(classification_test_metric)
            if (classification_test_metric.f1_score< self.model_trainer_config.expected_accuracy):
                logging.info("No best model found with score more than base score")
                raise Exception("No best model found with score more than base score")

            ## checking for over and underfitting 
            diff = abs (classification_train_metric.f1_score - classification_test_metric.f1_score)
            if diff > self.model_trainer_config.overfitting_underfitting_threshold:
                logging.info("Model is either overfitting or underfitting, more experiments required")
                raise Exception("Model is either overfitting or underfitting, more experiments required")

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

            sensor_model = SensorModel(preprocessing_object= preprocessor, trained_model_object = model) 
            save_object(file_path=self.model_trainer_config.trained_model_file_path, obj = sensor_model)

            model_trainer_artifact = ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                train_metric_artifact= classification_train_metric,
                                test_metric_artifact= classification_test_metric)
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise SensorException(e, sys) from e
