class Album:

    def __init__(self, album_id=None, name=None) -> None:
        self._id = album_id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
