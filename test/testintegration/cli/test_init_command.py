import unittest
from pathlib import Path
from hop.cli.init_command import InitCommand
from hop import create_parser

TEST_DIR_PATH = '/tmp/testinitcommand'
EXPECTED_CONTENTS = '''name: hop-gocd
provider:
    name: local_docker
    agents:
        instances: 2
'''

class TestInitCommand(unittest.TestCase):
    def setUp(self):
        self.parser = create_parser()

    def tearDown(self):
        test_dir = Path(TEST_DIR_PATH)
        (test_dir / 'hop.yml').unlink() #you can't delete nonempty dirs in python
        test_dir.rmdir()

    def test_should_create_hop_config_in_specified_folder(self):

        InitCommand(self.parser.parse_args(['init', TEST_DIR_PATH])).execute()

        config = Path(TEST_DIR_PATH + '/hop.yml')
        self.assertTrue(config.is_file(), 'file appears not to exist')

        config_contents = config.read_text()
        self.assertEqual(config_contents, EXPECTED_CONTENTS, "hop.yml contents did not match expected contents")
