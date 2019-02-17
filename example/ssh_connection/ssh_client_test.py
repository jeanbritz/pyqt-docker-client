import six

from paramiko import SSHClient
from paramiko.util import log_to_file

log_to_file("paramiko-ssh_client_test.log", level="DEBUG")


base_url = 'ssh://darkhorse@10.0.0.17:2375'
ssh_client = None
try:
    ssh_client = SSHClient()
    ssh_client.load_system_host_keys()
    parsed = six.moves.urllib_parse.urlparse(base_url)
    ssh_client.connect(parsed.hostname, parsed.port, parsed.username)

    stdin, stdout, stderr = ssh_client.exec_command('docker version')
    print(stdout.read())
finally:
    if ssh_client:
        ssh_client.close()
