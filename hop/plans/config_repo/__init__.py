from xml.etree.ElementTree import fromstring

from gomatic.xml_operations import Ensurance
from hop.core import console


def config_repo_not_yet_present(git_url, config_groups):
    git_urls = [g.get('url') for g in config_groups.element.findall('config-repo//git')]
    return not git_url in git_urls


def ensure_config_repo(configurator, git_url, plugin):
    config_groups = Ensurance(configurator._GoCdConfigurator__xml_root).ensure_child("config-repos")  # pylint: disable=protected-access
    if config_repo_not_yet_present(git_url, config_groups):
        Ensurance(config_groups.element).append(
            fromstring('<config-repo plugin="{0}"><git url="{1}" /></config-repo>'.format(plugin, git_url)))


def execute(configurator, app_name, app_config):
    console("executing 'config_repo' plan for {0}".format(app_name))

    ensure_config_repo(configurator, git_url=app_config['git_url'], plugin='yaml.config.plugin')
