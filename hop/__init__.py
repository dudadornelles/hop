import argparse
import importlib
import os


from hop.cli import create_parser
from hop.core import read_yaml
from hop.core.hop_config import HopConfig


def get_command(command_name):
    try:
        return importlib.import_module("hop.cli.commands.{}".format(command_name))
    except ImportError:
        print("ERROR: command '{}' has no implementation under hop.cli.commands".format(command_name))
        exit(1)

def run():
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        exit(0)

    get_command(args.command).execute(args, hop_config=hop_config(args))

def hop_config(args):
    if args.command == 'init':
        return
    hop_config_path = os.path.join(os.getcwd(), args.hop_config or 'hop.yml')
    return HopConfig(config_dict=read_yaml(hop_config_path))
