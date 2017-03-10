import unittest

import getpass
from base64 import b64encode
from hashlib import sha1
from shutil import rmtree

from unittest.mock import patch
from pathlib import Path
from hop.cli.init_command import InitCommand
from hop import create_parser

TEST_DIR_PATH = '/tmp/testinitcommand'
EXPECTED_CONTENTS = '''name: testinitcommand
provider:
    name: local_docker
    server:
        passwd_path: ./passwd
        http_port: 18153
        https_port: 18154
        image: gocdhop/hop-server
        name: testinitcommand-server
    agents:
        image: gocdhop/hop-agent
        prefix: testinitcommand-agent
        instances: 2
'''



class TestInitCommand(unittest.TestCase):
    def setUp(self):
        self.parser = create_parser()

    def tearDown(self):
        rmtree(TEST_DIR_PATH, ignore_errors = True)

    @patch('getpass.getpass')
    def test_should_create_hop_config_in_specified_folder(self, getpw):
        input_password = 'foo'
        getpw.return_value = input_password
        password_hash = b64encode(sha1(input_password.encode('ascii')).digest())
        expected_passwd_content = 'admin:{SHA}' + password_hash.decode('ascii') + '\n'

        InitCommand(self.parser.parse_args(['init', TEST_DIR_PATH])).execute()

        config = Path(TEST_DIR_PATH + '/hop.yml')
        self.assertTrue(config.is_file(), 'file appears not to exist')

        config_contents = config.read_text()
        self.assertEqual(config_contents, EXPECTED_CONTENTS, "hop.yml contents did not match expected")

        passwd = Path(TEST_DIR_PATH + '/passwd')
        self.assertTrue(passwd.is_file(), 'file appears not to exist')
        passwd_contents = passwd.read_text()
        self.assertEqual(passwd_contents, expected_passwd_content)
