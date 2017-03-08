import logging as log

import docker


def _server_config(config, network):
    return {
        'name': config.get('provider.server.name', 'hop-server'),
        'detach': True,
        'ports': {
            8153: 18153,
            8154: 18154
        },
        'hostname': config.get('provider.server.hostname', 'hop-server'),
        'networks': [network]
    }


def _agent_config(server_name, agent_name, network):
    return {
        'environment': ['GO_SERVER_URL=https://{}:8154/go'.format(server_name)],
        'hostname': agent_name,
        'name': agent_name,
        'networks': [network],
        'detach': True
    }


def provision(hop_config):
    client = docker.from_env()

    network_name = hop_config.get('provider.network', 'hopnetwork')
    network = client.networks.create(network_name, driver="bridge")

    server_config = run_go_server(client, hop_config, network, network_name)
    run_go_agent(client, hop_config, network, network_name, server_config)

    print("hop:: gocd is up and running on https://localhost:8154/")


def run_go_agent(client, hop_config, network, network_name, server_config):
    server_hostname = server_config['hostname']
    go_agent_image = hop_config.get('provider.agents.image', 'gocd/gocd-agent')
    go_agent_name_prefix = hop_config.get('provider.agents.prefix', 'hop-agent')

    maybe_agents_containers = [c for c in client.containers.list() if c.name.startswith(go_agent_name_prefix)]
    for i in range(0, hop_config.get('provider.agents.instances', 1)):
        agent_name = "{0}-{1}".format(go_agent_name_prefix, i)
        if agent_name not in [a.name for a in maybe_agents_containers]:
            agent_config = _agent_config(server_hostname, agent_name, network_name)
            log.debug('creating AGENT with config %s', agent_config)
            agent = client.containers.run(go_agent_image, **agent_config)
            network.connect(agent)


def run_go_server(client, hop_config, network, network_name):
    server_config = _server_config(hop_config, network_name)
    go_server_image = hop_config.get('provider.server.image', 'gocd/gocd-server')
    maybe_server_containers = [c for c in client.containers.list() if c.name == server_config['name']]
    if len(maybe_server_containers) == 0:
        log.debug('creating SERVER with config %s', server_config)
        server = client.containers.run(go_server_image, **server_config)
        network.connect(server)

    return server_config
