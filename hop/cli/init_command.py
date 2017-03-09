from pathlib import Path

BASE_HOP_CONFIG = '''name: {0}
provider:
    name: local_docker
    server:
        passwd_path: ./passwd
        http_port: 18153
        image: hopgocd/hop-server
        name: {0}-server
        ports_map:
            8153: 18153
            8154: 18154
    agents:
        image: gocd/gocd-agent
        prefix: {0}-agent
        instances: 2
'''


def generate_hop_config(hop_file, installation_name):
    hop_file.touch()
    hop_file.write_text(BASE_HOP_CONFIG.format(installation_name))


class InitCommand(object):
    def __init__(self, args):
        self.args = args

    def execute(self):
        hop_dir = Path(self.args.dest_dir)
        hop_dir.mkdir(parents=True)
        hop_config = hop_dir / 'hop.yml'
        generate_hop_config(hop_config, installation_name=self.args.dest_dir)
