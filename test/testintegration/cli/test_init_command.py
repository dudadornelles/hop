import unittest
from pathlib import Path
from hop.cli.init_command import InitCommand
from hop import create_parser

test_dir_path = '/tmp/testinitcommand'

class TestInitCommand(unittest.TestCase):
    def setUp(self):
        self.parser = create_parser()

    def tearDown(self):
        test_dir = Path(test_dir_path)
        (test_dir / 'hop.yml').unlink() #you can't delete nonempty dirs in python
        test_dir.rmdir()

    def test_should_create_hop_config_in_specified_folder(self):
        InitCommand(self.parser.parse_args(['init', test_dir_path])).execute()
        config = Path(test_dir_path + '/hop.yml')
        self.assertTrue(config.is_file(), 'file appears not to exist')
        #do something here to make sure the file looks right
