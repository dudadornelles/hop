import argparse
import os

def new_dir(string):
    if os.path.exists(string):
        raise argparse.ArgumentTypeError("must specify a new directory for the hop project")
    return string

def create_parser():
    config_parser = argparse.ArgumentParser(add_help=False)
    config_parser.add_argument('--hop-config', help='path to hop.yml file (defaults to ./hop.yml)')
    parser = argparse.ArgumentParser()
    sparser = parser.add_subparsers(dest='command')

    init_parser = sparser.add_parser('init', help='initializes hop', parents=[config_parser])
    init_parser.add_argument('dest_dir', help='destination directory for hop', nargs='?', default='.')

    sparser.add_parser('provision', help='provisions gocd', parents=[config_parser])

    configure_parser = sparser.add_parser('configure', help='provisions gocd', parents=[config_parser])
    configure_parser.add_argument('context', help='A folder with a set of yml files for app definitions')
    configure_parser.add_argument('host', help='The host for gocd (use the http url, not the https one')
    configure_parser.add_argument('user', help='A user with admin rights', default='admin')
    configure_parser.add_argument('password', help='The GoCD admin password')

    return parser
