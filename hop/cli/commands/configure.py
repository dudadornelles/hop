from importlib import import_module
import os

from gomatic import GoCdConfigurator
from hop.core.gomatic_ext import SecureHostRestClient
from hop.core import read_yaml


def execute(args, **kwargs):  # pylint: disable=unused-argument
    hop_config = kwargs['hop_config']
    configurator = GoCdConfigurator(SecureHostRestClient(host=args.host or hop_config.configure_url,
                                                         username=args.user or 'admin',
                                                         password=args.password or hop_config.admin_password,
                                                         ssl=True,
                                                         verify_ssl=False))


    configure(configurator, apps=_find_all_apps(args.context))


def configure(configurator, apps):
    for app_name, app_config in apps.items():
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


def get_plan(plan_name):
    return import_module('hop.plans.{}'.format(plan_name))
