import argparse

import os
from hop.cli import command_factory
from hop.core import read_yaml


def run():
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        exit(0)
    hop_config_path = os.path.join(os.getcwd(), args.hop_config or 'hop.yml')
    hop_config = read_yaml(hop_config_path)

    command_factory.create_from_args(args, hop_config).execute()


def create_parser():
    config_parser = argparse.ArgumentParser(add_help=False)
    config_parser.add_argument('--hop-config', help='path to hop.yml file (defaults to ./hop.yml)')
    parser = argparse.ArgumentParser()
    sparser = parser.add_subparsers(dest='command')

    sparser.add_parser('init', help='initializes hop (by defaul in the current folder)', parents=[config_parser])
    sparser.add_parser('provision', help='provisions gocd', parents=[config_parser])

    return parser
