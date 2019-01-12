from core import ClientModel


class ImageClientModel(ClientModel):
    ATTR_CONTAINERS = 'Container'
    ATTR_CREATED = 'Created'
    ATTR_LABELS = 'Labels'
    ATTR_PARENT_ID = 'ParentId'
    ATTR_REPO_DIGESTS = 'RepoDigests'
    ATTR_REPO_TAGS = 'RepoTags'
    ATTR_SHARED_SIZE = 'SharedSize'
    ATTR_SIZE = 'Size'
    ATTR_VIRTUAL_SIZE = 'VirtualSize'

    def __init__(self, details: dict = None):
        super().__init__(details)

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
        Image labels in form of a dict
        :return: Labels in form of a dict
        """
        labels = self.details.get(self.ATTR_LABELS)
        if labels is None:
            labels = {}
        return labels

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
        return ' - '.join(self.repo_tags)
