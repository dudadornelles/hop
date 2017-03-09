import os

from hop.core import HopConfig, read_yaml
from .init_command import InitCommand
from .provision_command import ProvisionCommand
from .configure_command import ConfigureCommand


def hop_config(args):
    hop_config_path = os.path.join(os.getcwd(), args.hop_config or 'hop.yml')
    return HopConfig(config_dict=read_yaml(hop_config_path))


def create_from_args(args):
    if args.command == 'init':
        return InitCommand(args)
    if args.command == 'provision':
        return ProvisionCommand(args, hop_config(args))
    if args.command == 'configure':
        return ConfigureCommand(args, hop_config(args))
