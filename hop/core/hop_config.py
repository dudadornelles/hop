from functools import reduce
import os

from hop.core import read_yaml


class BadHopConfiguration(Exception):
    pass


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
        saved_settings_file = os.path.expanduser('~/.hop{}'.format(self.get('name')))
        return read_yaml(saved_settings_file).get('password')

    @property
    def passwd_path(self):
        return os.path.join(os.getcwd(), self.get("provider.server.passwd_path", 'passwd'))

    @property
    def server_hostname(self):
        return self.get('provider.server.hostname', self.server_name)

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

    @property
    def provider_name(self):
        try:
            return self['provider']['name']
        except KeyError:
            raise BadHopConfiguration("Can't find provider.name in hop.yml, make sure your configuration is correct")

    @property
    def server_name(self):
        return self.get('provider.server.name', 'hop-server')

    @property
    def agents_prefix(self):
        return self.get('provider.agents.prefix', 'hop-agent')
