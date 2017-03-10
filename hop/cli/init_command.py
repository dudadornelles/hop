from getpass import getpass
from pathlib import Path
import os

from sh import htpasswd  # pylint: disable=no-name-in-module
from hop.core import write_yaml, read_yaml
from hop.core.hop_config import HopConfig



BASE_HOP_CONFIG = '''name: {0}
provider:
    name: local_docker
    server:
        passwd_path: ./passwd
        http_port: 18153
        https_port: 18154
        image: gocdhop/hop-server
        name: {0}-server
    agents:
        image: gocdhop/hop-agent
        prefix: {0}-agent
        instances: 2
'''

def get_admin_password(hop_dir, hop_config):
    password = getpass('admin password:')
    repeat_password = getpass('repeat admin password:')
    if password != repeat_password:
        print("ERROR: passwords must match")
        exit(1)

    htpasswd('-sbc', os.path.join(hop_dir.as_posix(), hop_config.get('provider.server.passwd_path')), 'admin', password)
    write_yaml({'password': password}, os.path.expanduser('~/.hop{}'.format(hop_config.name)))


def generate_hop_config(hop_file, installation_name):
    hop_file.touch()
    hop_file.write_text(BASE_HOP_CONFIG.format(installation_name))
    return read_yaml(hop_file.as_posix())


class InitCommand(object):
    def __init__(self, args):
        self.args = args

    def execute(self):
        hop_dir = Path(self.args.dest_dir)
        hop_dir.mkdir(parents=True)
        hop_config = hop_dir / 'hop.yml'
        config = generate_hop_config(hop_config, installation_name=hop_dir.name)
        hop_config = HopConfig(config)
        get_admin_password(hop_dir, hop_config)
