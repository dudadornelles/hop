class ProvisionCommand(object):
    def __init__(self, args):
        self.args = args

    def execute(self):
        print("Provisioning gocd")
