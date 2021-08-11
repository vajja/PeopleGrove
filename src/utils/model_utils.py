"""
loading model
"""

import pickle

from starlette.config import Config

from src.utils.logger_utils import Logger

LOGGER = Logger.get_instance()

config = Config("configs/props.env")


class LoadModel:
    """
    Loading model file
    """
    __model = None

    def __init__(self):
        if LoadModel.__model is None:
            LoadModel.load_model()

    @staticmethod
    def load_model(reload=False):
        """
        loading model when it none or new model file is updated
        :param reload:
        :return:
        """
        try:
            if LoadModel.__model is None or reload:
                LoadModel.__model = pickle.load(open(config.get("MODEL_PATH"), 'rb'))
            LOGGER.logger.info("Sucessfully loaded the model")
        except Exception as e:
            LOGGER.log_err.exception("Error while loading model: " + str(e))

    @staticmethod
    def get_model():
        """
        directly accessing the model
        :return:
        """
        if LoadModel.__model is None:
            LoadModel()
        return LoadModel.__model
