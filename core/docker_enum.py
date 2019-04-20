import enum


class ContainerStatus(enum.Enum):

    CREATED = 'created'
    RESTARTING = 'restarting'
    RUNNING = 'running'
    PAUSED = 'paused'
    EXITED = 'exited'
    DEAD = 'dead'

    @staticmethod
    def from_str(status):
        if status == 'created':
            return ContainerStatus.CREATED
        if status == 'restarting':
            return ContainerStatus.RESTARTING
        if status == 'running':
            return ContainerStatus.RUNNING
        if status == 'paused':
            return ContainerStatus.PAUSED
        if status == 'exited':
            return ContainerStatus.EXITED
        if status == 'dead':
            return ContainerStatus.DEAD

class Operation(enum.Enum):

    START_CONTAINER = 'op_start_container'
    STOP_CONTAINER = 'op_stop_container'


class DockerEntity(enum.Enum):

    IMAGE = 'image'
    CONTAINER = 'container'
    NETWORK = 'network'
