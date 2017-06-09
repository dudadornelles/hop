from unittest import TestCase
from unittest.mock import patch, Mock
from argparse import Namespace
import os
import subprocess

import docker
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from hop.core.hop_config import HopConfig
import hop.providers.local_docker as local_docker

import hop

urllib3.disable_warnings(InsecureRequestWarning)


def get_host_name():
    host = subprocess.check_output(['bash', '-c', "/sbin/ip route|awk '/default/ { print $3 }'"]).decode('utf-8').strip()
    return 'localhost' if host == '' else host


def delete_hop_containers(client):
    for container in client.containers.list(all=True):
        print('found container {}'.format(container.name))
        if container.name.startswith('hoptest'):
            print('deleting {}'.format(container.name))
            if container.status == 'running':
                container.kill()
            container.remove()


class TestLocalDockerProvider(TestCase):

    def setUp(self):
        self.passwd_path = os.path.join(os.getcwd(), 'passwd')
        self.client = docker.from_env()

        open(self.passwd_path, 'w').close()
        delete_hop_containers(self.client)

    def tearDown(self):
        delete_hop_containers(self.client)
        os.remove(self.passwd_path)
        [n.remove() for n in self.client.networks.list() if n.name == 'hoptest-network']

    def assertServerAndAgents(self, num_of_agents):
        containers = self.client.containers.list(all=True)

        server = next(c for c in containers if c.name == 'hoptest-server')
        self.assertEquals(server.status, 'running')
        
        agents = [c for c in containers if c.name.startswith('hoptest-agent-')]
        self.assertEquals(len(agents), num_of_agents)
        for agent in agents:
            self.assertEquals(agent.status, 'running')



    @patch.object(hop.providers.local_docker.provisioner.LocalDockerConfig, 'https_url')
    def test_provision_should_scale_up_and_down(self, https_url_mock):
        hop_config = HopConfig({
            'name': 'testhop',
            'provider': {
                'network': 'hoptest-network',
                'server': {
                    'name': 'hoptest-server',
                    'http_port': 3553,
                    'https_port': 3554
                },
                'agents': {
                    'prefix': 'hoptest-agent',
                    'instances': 3
                }
            }
        })
        https_url_mock.__get__ = Mock(return_value='https://{}:3554'.format(get_host_name()))

        local_docker.provision(hop_config)
        self.assertServerAndAgents(num_of_agents=3)

        # scaling down
        hop_config['provider']['agents']['instances'] = 1
        local_docker.provision(hop_config)
        self.assertServerAndAgents(num_of_agents=1)

        # scaling up again
        hop_config['provider']['agents']['instances'] = 2
        local_docker.provision(hop_config)
        self.assertServerAndAgents(num_of_agents=2)

    @patch.object(hop.providers.local_docker.provisioner.LocalDockerConfig, 'https_url')
    def test_destroy(self, https_url_mock):
        config = HopConfig({
            'name': 'testhop',
            'provider': {
                'network': 'hoptest-network',
                'server': {
                    'name': 'hoptest-server',
                    'http_port': 3553,
                    'https_port': 3554
                },
                'agents': {
                    'prefix': 'hoptest-agent',
                    'instances': 1
                }
            }
        })
        https_url_mock.__get__ = Mock(return_value='https://{}:3554'.format(get_host_name()))
        local_docker.provision(config)

        # when
        local_docker.destroy(Namespace(), config)

        # then
        containers = self.client.containers.list(all=True)
        maybe_server = [c for c in containers if c.name == 'hoptest-server']
        maybe_agents = [c for c in containers if c.name == 'hoptest-agent-0']

        self.assertTrue(len(maybe_server) == 0)
        self.assertTrue(len(maybe_agents) == 0)


