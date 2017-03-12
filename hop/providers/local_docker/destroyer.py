import docker

from hop.core import console

def _is_hop_container(container, hop_config):
    return container.name == hop_config.server_name or container.name.startswith(hop_config.agents_prefix)

def destroy(args, hop_config): # pylint: disable=unused-argument
    console("Destroying GoCD")
    client = docker.from_env()
    hop_containers = [c for c in client.containers.list(all=True) if _is_hop_container(c, hop_config)]

    for container in hop_containers:
        try:
            container.kill()
            container.remove()
        except Exception as exception:
            print(exception)
