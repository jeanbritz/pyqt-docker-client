import logging
import logging.config
import yaml

class Log:

    def __init__(self):
        with open('config/logging.yml', 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)

        global logger
        logger = logging.getLogger()


    @staticmethod
    def i(msg=None):
        """
        Log info message
        :param self:
        :param msg:
        :return:
        """
        logger.info(msg)

    @staticmethod
    def e(msg=None):
        """
        Log error message
        :param self:
        :param msg:
        :return:
        """
        logger.error(msg, exc_info=True)

    @staticmethod
    def w(msg=None):
        """
        Log warning message
        :param self:
        :param msg:
        :return:
        """
        logger.warning(msg)
