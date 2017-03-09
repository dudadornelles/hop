import unittest
import os

from hop.core import HopConfig
import docker
import hop.providers.local_docker as local_docker


def delete_hop_containers(client):
    for container in client.containers.list(all=True):
        print('found container {}'.format(container.name))
        if container.name.startswith('hoptest'):
            print('deleting {}'.format(container.name))
            if container.status == 'running':
                container.kill()
            container.remove()


class TestLocalDockerProvider(unittest.TestCase):

    def setUp(self):
        self.passwd_path = os.path.join(os.getcwd(), 'passwd')
        self.client = docker.from_env()

        open(self.passwd_path, 'w').close()
        delete_hop_containers(self.client)

    def tearDown(self):
        delete_hop_containers(self.client)
        os.remove(self.passwd_path)
        [n.remove() for n in self.client.networks.list() if n.name == 'hoptest-network']

    def test_provision_should_not_fail_if_you_run_it_twice(self):
        config = HopConfig({
            'provider': {
                'network': 'hoptest-network',
                'server': {
                    'name': 'hoptest-server',
                    'ports_map': {
                        8154: 3554,
                        8153: 3553,
                    }
                },
                'agents': {
                    'prefix': 'hoptest-agent',
                    'instances': 1
                }
            }
        })

        local_docker.provision(config)
        local_docker.provision(config)

        containers = self.client.containers.list(all=True)
        server = next(c for c in containers if c.name == 'hoptest-server')
        agent = next(c for c in containers if c.name == 'hoptest-agent-0')

        self.assertEquals(server.status, 'running')
        self.assertEquals(agent.status, 'running')


