import os

from docker.client import DockerClient, APIClient
from docker.errors import DockerException
from docker.transport.sshconn import SSHAdapter
from paramiko.agent import Agent
from paramiko.util import log_to_file

log_to_file("paramiko.log", level="DEBUG")

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

adapter = None
print("----- TEST: Establish SSH Adapter -----")
try:
    base_url = 'ssh://darkhorse@10.0.0.17:22'
    adapter = SSHAdapter(base_url, timeout=60, pool_connections=1)
except NameError:
    raise Exception(
        'Install paramiko package to enable ssh:// support'
    )
finally:
    if adapter:
        print("SSH Adapter successfully initialized")
        adapter.close()


print("----- TEST: Using DockerClient to Get Version of Docker Daemon -----")
env = {'DOCKER_HOST': 'ssh://darkhorse@10.0.0.17'}
kwargs = {'timeout': 60, 'version': 'auto', 'environment': env}
client = None
try:
    client = DockerClient.from_env(**kwargs)
    version = client.api.version()
    print('Version: %s' % version)
except DockerException as e:
    print(e)
finally:
    if client:
        client.close()

print("----- TEST: Using APIClient to Get Version of Docker Daemon -----")
client = None
try:
    client = APIClient(base_url='ssh://darkhorse@10.0.0.17')
    version = client.version()
    print('Version: %s' % version)
except DockerException as e:
    print(e)
finally:
    if client:
        client.close()
