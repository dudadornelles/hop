import logging as log
import time
from xml.etree.ElementTree import tostring, fromstring

import docker
import os
import requests
import tarfile
from hop.core import console
from io import BytesIO


def create_tar_stream(file_content, file_name):
    # metadata for internal file
    tarinfo = tarfile.TarInfo(name=file_name)
    tarinfo.size = len(file_content)
    tarinfo.mtime = time.time()

    tarstream = BytesIO()
    tar = tarfile.TarFile(fileobj=tarstream, mode='w')
    tar.addfile(tarinfo, BytesIO(file_content))
    tar.close()
    tarstream.seek(0)
    return tarstream


def copy_to_container(src, dest, owner, group, container):
    log.info('copying to container: %s', locals())
    dest_file = os.path.basename(dest)
    dest_dir = os.path.dirname(dest)
    file_data = open(src).read().encode('utf-8')

    tar_stream = create_tar_stream(file_content=file_data, file_name=dest_file)
    container.put_archive(path=dest_dir, data=tar_stream)
    container.exec_run('chown {0}:{1} -R {2}'.format(owner, group, dest))


def init_security(server_container, url, hop_config):
    # copy passwd
    console("Updating passwd")
    copy_to_container(src=hop_config.passwd_path,
                      dest='/etc/go/passwd',
                      container=server_container,
                      owner='go',
                      group='go')

    # add security to cruise-config.xml
    response = requests.get('{}/go/admin/restful/configuration/file/GET/xml'.format(url))
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
    })


def wait_for_go_server(url):
    tries = 0
    while tries < 5:
        try:
            requests.get('{}/go/auth/login'.format(url))
            console("GoCD is up and running".format(url))
            return
        except Exception as exception:
            log.info("while waiting for gocd to be up, got %s", exception)
            tries += 1
            console("GoCD not yet initialized at {}. Will try again in 15 secs".format(url))
            time.sleep(15)
    print("ERROR: there was a problem initializing gocd. Check the server logs")
    exit(1)


def _server_config(config, network):
    server_name = config.get('provider.server.name', 'hop-server')
    return {
        'name': server_name,
        'detach': True,
        'ports': config.ports_map,
        'hostname': config.get('provider.server.hostname', server_name),
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
    console("Using local_docker provider")

    client = docker.from_env()
    ensure_images_available(client, hop_config)
    network_name = hop_config.get('provider.network', 'hopnetwork')
    server_config = _server_config(hop_config, network_name)
    url = 'http://localhost:{}'.format(server_config['ports'][8153])

    # create network
    maybe_network = [n for n in client.networks.list() if n.name == network_name]
    if len(maybe_network) == 0:
        network = client.networks.create(network_name, driver="bridge")
    else:
        network = maybe_network[0]

    # run go server
    server_container = run_go_server(client, server_config, network, hop_config)

    wait_for_go_server(url)
    init_security(server_container, url, hop_config)

    run_go_agent(client, hop_config, network, network_name, server_config)

    wait_for_go_server(url)
    console("GoCD is up and running on {}".format(url))

def ensure_images_available(client, hop_config):
    console("Verifying presense of images")
    agent_image = hop_config.get('provider.agents.image', 'gocd/gocd-agent')
    server_image = hop_config.get('provider.server.image', 'gocd/gocd-server')
    for image in [agent_image, server_image]:
        try:
            client.images.get(image)
        except docker.errors.ImageNotFound:
            console("Image {} not found. Attempting to pull.".format(image))
            client.images.pull(image)

def run_go_agent(client, hop_config, network, network_name, server_config):
    number_of_agents = hop_config.get('provider.agents.instances', 1)
    server_hostname = server_config['hostname']
    go_agent_image = hop_config.get('provider.agents.image', 'gocd/gocd-agent')
    go_agent_name_prefix = hop_config.get('provider.agents.prefix', 'hop-agent')

    maybe_agents_containers = [c for c in client.containers.list() if c.name.startswith(go_agent_name_prefix)]
    for i in range(0, number_of_agents):
        agent_name = "{0}-{1}".format(go_agent_name_prefix, i)
        if agent_name not in [a.name for a in maybe_agents_containers]:
            console("Starting {0} from {1}".format(agent_name, go_agent_image))
            agent_config = _agent_config(server_hostname, agent_name, network_name)
            log.debug('creating AGENT with config %s', agent_config)
            agent = client.containers.run(go_agent_image, **agent_config)
            network.connect(agent)


def run_go_server(client, server_config, network, hop_config):
    go_server_image = hop_config.get('provider.server.image', 'gocd/gocd-server')
    maybe_server_containers = [c for c in client.containers.list() if c.name == server_config['name']]

    if len(maybe_server_containers) == 0:
        console("Starting GoCD server from {0}".format(go_server_image))
        log.debug('creating SERVER with config %s', server_config)
        server = client.containers.run(go_server_image, **server_config)
        network.connect(server)
        return server
    else:
        return maybe_server_containers[0]
