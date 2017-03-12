import logging

from importlib import import_module


class ProviderNotFound(Exception):
    pass

def get_provider(hop_config):
    try:
        return import_module('hop.providers.{}'.format(hop_config.provider_name))
    except ImportError:
        raise ProviderNotFound("Error initializing provider. Make sure your configuration is correct")
