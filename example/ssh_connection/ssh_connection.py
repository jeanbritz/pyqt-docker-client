import os
import logging

from docker.client import DockerClient
from docker.errors import DockerException
from paramiko.agent import Agent
from paramiko.util import log_to_file

log_to_file("paramiko.log", level="DEBUG")

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

print("Test only applicable if GUI application runs on Windows 10")
print("---- TEST: ssh-agent env variables ----")
# SSH_AUTH_SOCK variable needs to be available for SSH Adapter to work
try:
    print("SSH_AUTH_SOCK: %s " % os.environ['SSH_AUTH_SOCK'])
except KeyError as e:
    print("SSH_AUTH_SOCK needs to be set. Usually it would be SSH_AUTH_SOCK: /tmp/.ssh-pagent-%USERPROFILE%")

print("---- TEST: Pagent is running? ----")
agent = Agent()
keys = agent.get_keys()
if keys:
    print("Pagent is running and has %d private key(s) loaded" % len(keys))
else:
    print("Pagent is not running.")


print("----- TEST: Using DockerClient to Get Version of Docker Daemon -----")
env = {'DOCKER_HOST': 'ssh://darkhorse@10.0.0.17'}
kwargs = {'timeout': 60, 'version': 'auto', 'environment': env}
try:
    client = DockerClient.from_env(**kwargs)
    version = client.api.version()
    print("Version: %s" % version)
    print('Loaded environment')
except DockerException as e:
    print(e)
