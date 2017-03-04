import ruamel.yaml as yaml
from os import path
from os import getcwd, makedirs

CONFIG_DIR = path.join(getcwd(), '.hop')
CONFIG_FILE = path.join(config_dir, 'hopconfig.yml')

def read_yaml(fpath):
    return yaml.load(open(fpath).read(), Loader=yaml.RoundTripLoader, preserve_quotes=True) or {}

def write_yaml(content, fpath):
    yaml.dump(content, open(fpath, 'w'), Dumper=yaml.RoundTripDumper)

def _read_config():
    if not path.exists(CONFIG_DIR):
        makedirs(CONFIG_DIR)
    if not path.exists(CONFIG_FILE):
        open(CONFIG_FILE).close()
    return read_yaml(config_file)


class ConfigException(Exception):
    pass


class HopConfig(object):

    def get(self, section, key, default=None):
        self.config = _read_config()
        section = self.config.get(section, None)
        if not section:
            raise ConfigException("section {} not found in .hop/hopconfig. This is likeyly a bug".format(section))
        return section.get(key, default)

    def put(self, section, key, value):
        self.config[section] = self.config[section] or {}
        self.config[section][key] = value
        write_yaml(self.config, CONFIG_FILE)


hopconfig = HopConfig()
