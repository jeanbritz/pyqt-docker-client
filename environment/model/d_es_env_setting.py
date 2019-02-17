
class DEsEnvSetting:

    def __init__(self, env_id=None, name=None, value=None) -> None:
        self._env_id = env_id
        self._name = name
        self._value = value

    @property
    def env_id(self) -> int:
        return self._env_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> str:
        return self._value;

    def __repr__(self) -> str:
        return "[env_id: %d, name: %s, value: %s]" % (self._env_id, self._name, self._value)


