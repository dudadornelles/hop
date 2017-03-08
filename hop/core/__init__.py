from os import path
from os import getcwd, makedirs
import ruamel.yaml as yaml

from .hop_config import HopConfig
CONFIG_DIR = path.join(getcwd(), '.hop')


def read_yaml(fpath):
    return yaml.load(open(fpath).read(), Loader=yaml.RoundTripLoader, preserve_quotes=True) or {}


def write_yaml(content, fpath):
    yaml.dump(content, open(fpath, 'w'), Dumper=yaml.RoundTripDumper)



class ConfigException(Exception):
    pass


class HopStateConfig(object):

    def __init__(self, config_dir=CONFIG_DIR):
        self.config_dir = config_dir
        self.config_file = path.join(self.config_dir, 'hopconfig.yml')
        self.config = self._read_config()
        write_yaml(self.config, self.config_file)

    def get(self, section, key, default=None):
        self.config = self._read_config()
        if not self.config.get(section, None):
            self.config[section] = {}
        return self.config.get(section).get(key, default)

    def set(self, section, key, value):
        self.config[section] = self.config[section] or {}
        self.config[section][key] = value
        write_yaml(self.config, self.config_file)

    def _read_config(self):
        if not path.exists(self.config_dir):
            makedirs(self.config_dir)
        if not path.exists(self.config_file):
            open(self.config_file, 'w').close()
        return read_yaml(self.config_file)



HOP_STATE_CONFIG = HopStateConfig()
