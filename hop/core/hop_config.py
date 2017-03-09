from functools import reduce
import os

from hop.core import read_yaml


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
    def admin_password(self):
        return read_yaml(os.path.expanduser('~/.hop{}'.format(self.get('name')))).get('password')

    @property
    def passwd_path(self):
        return os.path.join(os.getcwd(), self.get("provider.server.passwd_path", 'passwd'))

    @property
    def host(self):
        return 'localhost:{}'.format(self.http_port)

    @property
    def ports_map(self): # TODO: move to LocalDockerProviderConfig(HopConfig)
        return {
            8154: self.https_port,
            8153: self.http_port
        }

    @property
    def https_port(self):
        return self.get('provider.server.https_port')

    @property
    def http_port(self):
        return self.get('provider.server.http_port')

    @property
    def name(self):
        return self.get('name')
