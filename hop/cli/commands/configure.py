from importlib import import_module
import json
import os
import requests

from gomatic import GoCdConfigurator
from hop.core import read_yaml


def execute(args, **kwargs):  # pylint: disable=unused-argument
    hop_config = kwargs['hop_config']
    configurator = GoCdConfigurator(SecureHostRestClient(host=args.host or hop_config.host,
                                                         username=args.user or 'admin',
                                                         password=args.password or hop_config.admin_password,
                                                         ssl=False))


    for app_name, app_config in _find_all_apps(args.context).items():
        try:
            plan = get_plan(app_config['plan'])
            plan.execute(configurator, app_name, app_config)
        except KeyError:
            print("WARN: app '{}' does not define a plan".format(app_name))
        except ImportError as exception:
            print(exception)
            print("WARN: couldnt find plan with name '{0}' for app '{1}'".format(app_config['plan'], app_name))
    configurator.save_updated_config()


def _find_all_apps(yaml_files_folder):
    all_apps_ = {}
    for root, _, files in os.walk(yaml_files_folder):
        for fname in files:
            if fname.endswith(".yml") or fname.endswith(".yaml"):
                apps = read_yaml(os.path.join(root, fname))
                all_apps_.update(apps)
    return all_apps_


class SecureHostRestClient(object):
    def __init__(self, host, username=None, password=None, ssl=False, verify_ssl=True):
        self.__host = host
        self.__username = username
        self.__password = password
        self.__ssl = ssl
        self.__verify_ssl = verify_ssl

    def __repr__(self):
        return 'HostRestClient("{0}", ssl={1})'.format(self.__host, self.__ssl)

    def __path(self, path):
        http_prefix = 'https://' if self.__ssl else 'http://'
        return '{0}{1}{2}'.format(http_prefix, self.__host, path)

    def __auth(self):
        return (self.__username, self.__password) if self.__username or self.__password else None

    def get(self, path):
        return requests.get(self.__path(path), auth=self.__auth(), verify=self.__verify_ssl)

    def post(self, path, data):
        url = self.__path(path)
        result = requests.post(url, data, auth=self.__auth(), verify=self.__verify_ssl)
        if result.status_code != 200:
            try:
                result_json = json.loads(result.text.replace("\\'", "'"))
                message = result_json.get('result', result.text)
                raise RuntimeError("Could not post config to Go server (%s) [status code=%s]:\n%s" % (
                    url, result.status_code, message))
            except ValueError:
                raise RuntimeError(
                    "Could not post config to Go server (%s) [status code=%s] (and result was not json):\n%s" % (
                        url, result.status_code, result))


def get_plan(plan_name):
    return import_module('hop.plans.{}'.format(plan_name))
