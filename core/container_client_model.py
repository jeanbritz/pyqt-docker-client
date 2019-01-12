from core import ClientModel


class ContainerClientModel(ClientModel):
    ATTR_NAMES = 'Names'
    ATTR_IMAGE = 'Image'
    ATTR_IMAGE_ID = 'ImageID'
    ATTR_COMMAND = 'Command'
    ATTR_CREATED = 'Created'
    ATTR_PORTS = 'PORTS'
    ATTR_LABELS = 'Labels'
    ATTR_STATE = 'State'
    ATTR_STATUS = 'Status'
    ATTR_HOST_CONFIG = 'HostConfig'
    ATTR_NETWORK_SETTINGS = 'NetworkSettings'
    ATTR_MOUNTS = 'Mounts'

    def __init__(self, details: dict = None):
        super().__init__(details)

    @property
    def names(self):
        """
        Container Names
        :return:
        """
        return self.details.get(self.ATTR_NAMES)

    @property
    def image(self):
        """
        Image name associated with this container
        :return:
        """
        return self.details.get(self.ATTR_IMAGE)

    @property
    def image_id(self):
        """
        Image ID associated with this container
        :return:
        """
        return self.details.get(self.ATTR_IMAGE_ID)

    @property
    def command(self):
        """
        Container startup command
        :return:
        """
        return self.details.get(self.ATTR_COMMAND)

    @property
    def created(self):
        """
        Created date of image
        :return: Epoch timestamp of created date
        """
        return self.details.get(self.ATTR_CREATED)

    @property
    def labels(self):
        """"
        Container labels in form of a dict
        :return: Labels in form of a dict
        """
        labels = self.details.get(self.ATTR_LABELS)
        if labels is None:
            labels = {}
        return labels

    @property
    def state(self):
        """
        Container state
        :return:
        """
        return self.details.get(self.ATTR_STATE)

    @property
    def status(self):
        """
        Container status message
        :return:
        """
        return self.details.get(self.ATTR_STATUS)

    @property
    def host_config(self):
        """
        Contaner host config
        :return:
        """
        return self.details.get(self.ATTR_HOST_CONFIG)

    @property
    def network_settings(self):
        """
        Container Network Settings
        :return:
        """
        return self.details.get(self.ATTR_NETWORK_SETTINGS)

    @property
    def mounts(self):
        """
        Container mounts info
        :return:
        """
        return self.details.get(self.ATTR_MOUNTS)

    @property
    def parent_id(self):
        """
        Parent Id of this image
        :return:
        """
        return self.details.get(self.ATTR_PARENT_ID)

    @property
    def repo_digests(self):
        """
        Repo digests of this image
        :return:
        """
        return self.details.get(self.ATTR_REPO_DIGESTS)

    @property
    def repo_tags(self):
        """
        Repo tags of this image
        :return:
        """
        tags = self.details.get(self.ATTR_REPO_TAGS)
        if tags is None:
            tags = []
        return tags

    @property
    def shared_size(self):
        """
        Shared Size
        """
        return self.details.get(self.ATTR_SHARED_SIZE)

    @property
    def size(self):
        """
        Image Size
        :return:
        """
        return self.details.get(self.ATTR_SIZE)

    @property
    def virtual_size(self):
        """
        Virtual Size of image
        :return:
        """
        return self.details.get(self.ATTR_VIRTUAL_SIZE)

    def __repr__(self):
        return '%s | %s' % (' - '.join(self.names), self.status)
