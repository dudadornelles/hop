class InitCommand(object):
    def __init__(self, args):
        self.args = args

    def execute(self):
        print("{} - Initializing hop in the current folder...".format(self.args.command))
