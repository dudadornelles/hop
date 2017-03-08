from hop.core import HopConfig
from .init_command import InitCommand
from .provision_command import ProvisionCommand


def create_from_args(args, hop_config):
    hop_config = HopConfig(config_dict=hop_config)
    if args.command == 'init':
        return InitCommand(args)
    if args.command == 'provision':
        return ProvisionCommand(args, hop_config)
