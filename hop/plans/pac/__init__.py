from xml.etree.ElementTree import fromstring

from gomatic.xml_operations import Ensurance
from hop.core import console


def ensure_config_repo(configurator, git_url, plugin):
    config_groups = Ensurance(configurator._GoCdConfigurator__xml_root).ensure_child("config-repos") # pylint: disable=protected-access
    gits = config_groups.element.find('config-repo//git')
    if not gits or not any([c for c in gits if c.url == git_url]):
        Ensurance(config_groups.element).append(
            fromstring('<config-repo plugin="{0}"><git url="{1}" /></config-repo>'.format(plugin, git_url)))


def execute(configurator, app_name, app_config):
    console("executing 'pac' plan for {0}".format(app_name))

    ensure_config_repo(configurator, git_url=app_config['git_url'], plugin='yaml.config.plugin')
