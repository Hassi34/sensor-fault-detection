import sys, os

from sensor.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from sensor.entity.config_entity import ModelPusherConfig
from sensor.logger.exception import SensorException
from sensor.logger import logging
import shutil


class ModelPusher:
    def __init__(self,
        model_eval_artifact: ModelEvaluationArtifact,
        model_pusher_config: ModelPusherConfig):
        try:
            self.model_eval_artifact = model_eval_artifact
            self.model_pusher_config = model_pusher_config

        except Exception as e:
            raise SensorException(e, sys)
            
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        logging.info("Entered initiate_model_pusher method of ModelPusher class")

        try:
            trained_model_path = self.model_eval_artifact.trained_model_path 
            #creating model pusher dir to save model
            model_file_path  = self.model_pusher_config.model_file_path
            print("...........................rrrr")
            print(trained_model_path, model_file_path)
            os.makedirs(os.path.dirname(model_file_path), exist_ok=True)
            shutil.copy(src = trained_model_path, dst = model_file_path )

            #saved model dir
            saved_model_path = self.model_pusher_config.saved_model_path
            os.makedirs(os.path.dirname(saved_model_path), exist_ok= True)
            shutil.copy(src = trained_model_path, dst = saved_model_path)

            #prepare artifact
            model_pusher_artifact = ModelPusherArtifact(
                saved_model_path=saved_model_path,
                model_file_path=model_file_path
            )

            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")

            logging.info("Exited initiate_model_pusher method of ModelPusher class")

            return model_pusher_artifact

        except Exception as e:
            raise SensorException(e, sys) from e
