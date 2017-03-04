import argparse
from hop.cli import command_factory

def run():
    parser = create_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        exit(0)
    command_factory.create_from_args(args).execute()

def create_parser():
    parser = argparse.ArgumentParser()
    sparser = parser.add_subparsers(dest='command')

    init_parser = sparser.add_parser('init', help='initializes hop (by defaul in the current folder)')
    init_parser = sparser.add_parser('provision', help='provisions gocd')

    return parser
