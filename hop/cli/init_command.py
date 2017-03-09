from pathlib import Path

#TODO extract this from being constant string when it gets more complicated
BASE_HOP_CONFIG = '''name: hop-gocd
provider:
    name: local_docker
    agents:
        instances: 2
'''

def generate_hop_config(hop_file):
    hop_file.touch()
    hop_file.write_text(BASE_HOP_CONFIG)

class InitCommand(object):
    def __init__(self, args, ):
        self.args = args

    def execute(self):
        hop_dir = Path(self.args.dest_dir)
        hop_dir.mkdir(parents=True)
        hop_config = hop_dir / 'hop.yml'
        generate_hop_config(hop_config)
