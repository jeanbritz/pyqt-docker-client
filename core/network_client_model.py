from core import ClientModel


class NetworkClientModel(ClientModel):

    ATTR_ATTACHABLE = 'Attachable'
    ATTR_CONFIG_FROM = 'ConfigFrom'
    ATTR_CONFIG_ONLY = 'ConfigOnly'
    ATTR_CONTAINERS = 'Containers'
    ATTR_CREATED = 'Created'
    ATTR_DRIVER = 'Driver'
    ATTR_ENABLEDIPV6 = 'EnableIPv6'
    ATTR_IPAM = 'IPAM'
    ATTR_INGRESS = 'Ingress'
    ATTR_INTERNAL = 'Internal'
    ATTR_LABELS = 'Labels'
    ATTR_NAME = 'Name'
    ATTR_OPTIONS = 'Options'
    ATTR_SCOPE = 'Scope'

    def __init__(self, details: dict = None):
        super().__init__(details)

    @property
    def attachable(self):
        return self.details.get(self.ATTR_ATTACHABLE)

    @property
    def config_from(self):
        return self.details.get(self.ATTR_CONFIG_FROM)

    @property
    def config_only(self):
        return self.details.get(self.ATTR_CONFIG_ONLY)

    @property
    def containers(self):
        return self.details.get(self.ATTR_CONTAINERS)

    @property
    def created(self):
        return self.details.get(self.ATTR_CREATED)

    @property
    def driver(self):
        return self.details.get(self.ATTR_DRIVER)

    @property
    def enableIPV6(self):
        return self.details.get(self.ATTR_ENABLEDIPV6)

    @property
    def ipam(self):
        return self.details.get(self.ATTR_IPAM)

    @property
    def ingress(self):
        return self.details.get(self.ATTR_INGRESS)

    @property
    def internal(self):
        return self.details.get(self.ATTR_INTERNAL)

    @property
    def labels(self):
        return self.details.get(self.ATTR_LABELS)

    @property
    def name(self):
        return self.details.get(self.ATTR_NAME)

    @property
    def options(self):
        return self.details.get(self.ATTR_OPTIONS)

    @property
    def scope(self):
        return self.details.get(self.ATTR_SCOPE)

    def __repr__(self):
        return self.name

