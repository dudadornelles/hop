import argparse

import os
from hop.cli import command_factory, create_parser
from hop.core import read_yaml


def run():
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        exit(0)

    command_factory.create_from_args(args).execute()
