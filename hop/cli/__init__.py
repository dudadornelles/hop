import argparse
import os

def new_dir(string):
    if os.path.exists(string):
        raise argparse.ArgumentTypeError("must specify a new directory for the hop project")
    return string


def create_parser():
    parser = argparse.ArgumentParser()
    sparser = parser.add_subparsers(dest='command')

    init_parser = sparser.add_parser('init', help='initializes hop')
    init_parser.add_argument('dest_dir', help='destination directory for hop')
    # init_parser.add_argument('--type', default='hop', help='the type of initialization, default is initialize hop')
    init_parser.add_argument('--skip-passwd', help='skip creating passwd file during init', dest='create_passwd',
                             action='store_false')
    init_parser.set_defaults(create_passwd=True)

    sparser.add_parser('provision', help='provisions GoCD')

    configure_parser = sparser.add_parser('configure', help='configures GoCD')
    configure_parser.add_argument('context', help='A folder with a set of yml files for app definitions')
    configure_parser.add_argument('-H', '--host', help='GoCD host. e.g: localhost:8153')
    configure_parser.add_argument('-u', '--user', help='User with admin role')
    configure_parser.add_argument('-p', '--password', help='Password for user')

    destroy_parser = sparser.add_parser('destroy', help='destroys GoCD')
    destroy_parser.add_argument('-f', '--force', help="Don't ask for confirmation before destroying GoCD",
                                action='store_true')
    destroy_parser.set_defaults(force=False)

    return parser
