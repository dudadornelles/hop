from .init_command import InitCommand
from .provision_command import ProvisionCommand

def create_from_args(args):
    if args.command == 'init':
        return InitCommand(args)
    if args.command == 'provision':
        return ProvisionCommand(args)

