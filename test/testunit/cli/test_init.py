import unittest
import sh
from mock import patch
from hop.cli.commands.init import htpasswd_fn


class TestHtpasswdWrapper(unittest.TestCase):

    @patch("hop.cli.commands.init._sh_htpasswd")
    @patch("hop.cli.commands.init.logging")
    @patch("hop.cli.commands.init.sys")
    def test_importing_htpasswd_should_show_error_message_if_cant_find_it(self, mock_sys, mock_logging, mock_sh_htpasswd):
        mock_sh_htpasswd.side_effect = sh.CommandNotFound()

        htpasswd_fn()

        mock_logging.error.assert_called_with("'htpasswd' not found in the path. Install 'htpasswd' and try again")
        mock_sys.exit.assert_called_with(1)



