
class DEnvEnvironment:

    def __init__(self, _id=None, name=None, settings=None) -> None:
        self._id = _id
        self._name = name
        self._settings = settings

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def settings(self) -> list:
        return self._settings

    @property
    def settings_to_dict(self) -> dict:
        result = {}
        for setting in self._settings:
            result[setting.name] = setting.value
        return result

    def __repr__(self) -> str:
        return "[id: %d, name: %s, settings: %s]" % (self._id, self._name, self._settings)

