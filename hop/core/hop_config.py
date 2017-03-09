from functools import reduce
import os


class HopConfig(dict):
    def __init__(self, config_dict):
        dict.__init__(self, config_dict)

    def get(self, key, default=None):
        if "." in key:
            try:
                return reduce(lambda config, key: config[key], key.split("."), self)
            except KeyError:
                return default

        return super(HopConfig, self).get(key, default)

    @property
    def passwd_path(self):
        return os.path.join(os.getcwd(), self.get("provider.server.passwd_path", 'passwd'))
