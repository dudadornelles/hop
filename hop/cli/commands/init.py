from getpass import getpass
from pathlib import Path
import os
import sys
import logging

from cookiecutter.main import cookiecutter
from hop.core import write_yaml, read_yaml
from hop.core.hop_config import HopConfig

import sh

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


def execute(args, **kwargs):  # pylint: disable=unused-argument
    hop_dir = Path(args.dest_dir)
    hop_config = hop_dir / 'hop.yml'
    config = generate_hop_config(hop_config, installation_name=hop_dir.name, dest_dir=hop_dir)
    hop_config = HopConfig(config)
    if args.create_passwd:
        get_admin_password(hop_dir, hop_config)


def _sh_htpasswd():
    return sh.htpasswd  # pylint: disable=no-member


def htpasswd_fn():
    try:
        return _sh_htpasswd()
    except sh.CommandNotFound:
        logging.error("'htpasswd' not found in the path. Install 'htpasswd' and try again")
        sys.exit(1)


def get_admin_password(hop_dir, hop_config):
    password = getpass('admin password:')
    repeat_password = getpass('repeat admin password:')
    if password != repeat_password:
        print("ERROR: passwords must match")
        exit(1)

    passwd_path = os.path.join(hop_dir.as_posix(), hop_config.get('provider.server.passwd_path'))
    htpasswd_fn()('-sbc', passwd_path, 'admin', password)
    write_yaml({'password': password}, os.path.expanduser('~/.hop{}'.format(hop_config.name)))


def generate_hop_config(hop_file, installation_name, dest_dir):
    cookiecutter('https://github.com/crohacz/cookiecutter-hop-template.git', no_input=True,
                 extra_context={'installation_name': installation_name, 'dest_dir': dest_dir})
    return read_yaml(hop_file.as_posix())
