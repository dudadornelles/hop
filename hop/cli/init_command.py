from pathlib import Path

class InitCommand(object):
    def __init__(self, args, ):
        self.args = args

    def execute(self):
        hop_dir = Path(self.args.dest_dir)
        hop_dir.mkdir(parents=True)
        hop_config = hop_dir / 'hop.yml'
        hop_config.touch()
