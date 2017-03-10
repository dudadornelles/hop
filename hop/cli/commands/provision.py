from importlib import import_module
from hop.core import console



def execute(args, **kwargs):  # pylint: disable=unused-argument
    hop_config = kwargs['hop_config']
    try:
        provisioner = get_provisioner(hop_config['provider']['name'])
    except KeyError as exception:
        print("Error initializing provider. Make sure your configuration is correct")
        print(exception)
        exit(1)
    except ImportError as exception:
        print("Error initializing provider. Make sure your configuration is correct")
        print(exception)
        exit(1)

    console("Provisioning GoCD")
    provisioner.provision(hop_config)

def get_provisioner(provisioner_name):
    return import_module('hop.providers.{}'.format(provisioner_name))
