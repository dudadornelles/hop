import logging as log
import time

from xml.etree.ElementTree import tostring, fromstring
import docker
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from hop.core import console
from hop.core.hop_config import HopConfig

from .docker_utils import copy_to_container, ensure_images_available

class LocalDockerConfig(HopConfig):
    def __init__(self, config):
        HopConfig.__init__(self, config)

    @property
    def network_name(self):
        return self.get('provider.network', 'hopnetwork')

    @property
    def server_config(self):
        return {
            'name': self.server_name,
            'detach': True,
            'ports': self.ports_map,
            'hostname': self.server_hostname,
            'volumes': self.server_volumes,
            'networks': [self.network_name]
        }

    def agent_config(self, agent_name):
        return {
            'environment': ['GO_SERVER_URL=https://{}:8154/go'.format(self.server_name)],
            'hostname': agent_name,
            'name': agent_name,
            'networks': [self.network_name],
            'detach': True,
            'volumes': self.agent_volumes
        }

    @property
    def agent_instance_count(self):
        return self.get('provider.agents.instances', 1)

    @property
    def agent_volumes(self):
        return self.get('provider.agents.volumes', {})

    @property
    def server_volumes(self):
        return self.get('provider.server.volumes', {})

    @property
    def server_image(self):
        return self.get('provider.server.image', 'gocd/gocd-server')

    @property
    def agent_image(self):
        return self.get('provider.agents.image', 'gocd/gocd-agent')

    @property
    def https_url(self):
        return 'https://localhost:{}'.format(self.https_port)


def provision(hop_config):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    console("Using local_docker provider")
    client = docker.from_env()
    hop_config = LocalDockerConfig(hop_config)

    ensure_images_available(client, hop_config)
    network = _create_network(client, hop_config.network_name)
    server_container = _run_go_server(client, hop_config, network)
    _wait_for_go_server(hop_config.https_url)
    _init_security(server_container, hop_config)
    _run_go_agent(client, hop_config, network)
    _wait_for_go_server(hop_config.https_url)

    console("GoCD is up and running on {}".format(hop_config.https_url))


def _create_network(client, network_name):
    maybe_network = [n for n in client.networks.list() if n.name == network_name]
    if len(maybe_network) == 0:
        return client.networks.create(network_name, driver="bridge")
    else:
        return maybe_network[0]


def _init_security(server_container, hop_config):
    # copy passwd
    url = hop_config.https_url
    console("Updating passwd")
    copy_to_container(src=hop_config.passwd_path,
                      dest='/etc/go/passwd',
                      container=server_container,
                      owner='go',
                      group='go')

    # add security to cruise-config.xml
    response = requests.get('{}/go/admin/restful/configuration/file/GET/xml'.format(url), verify=False)
    xml, md5 = response.content, response.headers.get('x-cruise-config-md5', None)
    if not md5:
        return

    console("Adding security config to cruise-config.xml")
    security = '<security><passwordFile path="/etc/go/passwd"/><admins><user>admin</user></admins></security>'
    cruise_config = fromstring(xml)
    cruise_config.find('server').insert(0, fromstring(security))
    requests.post('{}/go/admin/restful/configuration/file/POST/xml'.format(url), data={
        'xmlFile': tostring(cruise_config),
        'md5': md5
    }, verify=False)


def _wait_for_go_server(url):
    tries = 0
    while tries < 5:
        try:
            requests.get('{}/go/auth/login'.format(url), verify=False)
            console("GoCD is up and running".format(url))
            return
        except Exception as exception:
            log.info("while waiting for gocd to be up, got %s", exception)
            tries += 1
            console("GoCD not yet initialized at {}. Will try again in 15 secs".format(url))
            time.sleep(15)
    print("ERROR: there was a problem initializing gocd. Check the server logs")
    exit(1)


def _run_go_agent(client, hop_config, network):
    new_instance_count = hop_config.agent_instance_count

    # scale down
    agent_containers = sorted([c for c in client.containers.list(all=True) if
                               c.name.startswith(hop_config.agents_prefix)], key=lambda c: c.name)

    for agent in agent_containers[new_instance_count:]:
        console("Stopping and destroying {}".format(agent.name))
        agent.kill()
        agent.remove()

    # scale up
    container_names = sorted([a.name for a in client.containers.list(all=True)])
    for i in range(0, new_instance_count):
        agent_name = "{0}-{1}".format(hop_config.agents_prefix, i)

        if not agent_name in container_names:
            console("Starting {0} from {1}".format(agent_name, hop_config.agent_image))
            log.debug('creating AGENT with config %s', hop_config.agent_config(agent_name))
            agent = client.containers.run(hop_config.agent_image, **hop_config.agent_config(agent_name))
            network.connect(agent)


def _run_go_server(client, hop_config, network):
    go_server_image = hop_config.server_image
    maybe_server_containers = [c for c in client.containers.list() if c.name == hop_config.server_name]

    if len(maybe_server_containers) == 0:
        console("Starting GoCD server from {0}".format(go_server_image))
        log.debug('creating SERVER with config %s', hop_config.server_config)
        server = client.containers.run(go_server_image, **hop_config.server_config)
        network.connect(server)
        return server
    else:
        return maybe_server_containers[0]
