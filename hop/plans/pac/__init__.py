from gomatic.xml_operations import Ensurance
from hop.core import console


def ensure_config_repo(configurator, git_url, plugin):
    config_groups = Ensurance(configurator._GoCdConfigurator__xml_root).ensure_child("config-repose")
    config_repo = Ensurance(config_groups.element).ensure_child_with_attribute('config-repo', 'plugin', plugin)
    Ensurance(config_repo.element).ensure_child_with_attribute('git', 'url', git_url)


def execute(configurator, app_name, app_config):
    print(configurator)
    console("executing 'pac' plan for {0} with config {1}".format(app_name, app_config))

    ensure_config_repo(configurator, git_url=app_config['git_url'], plugin='yaml.config.plugin')
