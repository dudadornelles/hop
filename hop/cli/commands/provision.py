from hop.cli.commands import get_provider
from hop.core import console


def execute(args, **kwargs):  # pylint: disable=unused-argument
    console("Provisioning GoCD")

    hop_config = kwargs['hop_config']
    get_provider(hop_config).provision(hop_config)
