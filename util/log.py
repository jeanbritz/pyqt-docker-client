import logging


class Log:

    def __init__(self):
        global logger
        logger = logging.getLogger(__name__)

    @staticmethod
    def i(self, msg=None):
        """
        Log info message
        :param self:
        :param msg:
        :return:
        """
        logger.info(msg)

    @staticmethod
    def e(self, msg=None):
        self.logger.error(msg)
