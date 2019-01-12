from PyQt5.QtCore import QObject


class ClientModel(object):
    """
    Base class for representing a single object on the GUI
    """
    # Global Attribute
    id_attribute = 'Id'

    def __init__(self, details: dict = None):
        self.details = details
        if self.details is None:
            self.details = {}
        self.model = None

    @property
    def id(self):
        """
        ID of the object
        """
        return self.details.get(self.id_attribute)

    @property
    def short_id(self):
        """
        ID of the object, just truncated
        """

        return self.id[:10]
