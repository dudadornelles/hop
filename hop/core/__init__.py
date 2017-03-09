import ruamel.yaml as yaml


def read_yaml(fpath):
    return yaml.load(open(fpath).read(), Loader=yaml.RoundTripLoader, preserve_quotes=True) or {}


def write_yaml(content, fpath):
    yaml.dump(content, open(fpath, 'w'), Dumper=yaml.RoundTripDumper)


def console(text):
    print("hop:: {}".format(text))
