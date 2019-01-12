import enum


class ContainerStatus(enum.Enum):

    CREATED = 'created'
    RESTARTING = 'restarting'
    RUNNING = 'running'
    PAUSED = 'paused'
    EXITED = 'exited'
    DEAD = 'dead'


class Operation(enum.Enum):

    STOP_CONTAINER = 'op_stop_container'

