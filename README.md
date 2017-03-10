# hop

Hop is a CLI tool written in python you can use to manage GoCD installations using docker and pipeline-as-code.

## TL;DR:
Dependencies
```
python3.5
pip3
htpasswd
docker
```

Installing
```bash
$ pip3 install git+https://github.com/dudadornelles/hop.git
```
Initializing:
```bash
$ hop init myGoCD
```
Provisioning:
```bash
$ cd myGoCD
$ hop provision
hop:: Provisioning GoCD
hop:: Using local_docker provider
hop:: Starting GoCD server from hopgocd/hop-server
hop:: GoCD not yet initialized at http://localhost:18153. Will try again in 15 secs
hop:: GoCD not yet initialized at http://localhost:18153. Will try again in 15 secs
hop:: GoCD is up and running
hop:: Updating passwd
hop:: Adding security config to cruise-config.xml
hop:: Starting myGoCD-agent-0 from gocd/gocd-agent
hop:: Starting myGoCD-agent-1 from gocd/gocd-agent
hop:: GoCD is up and running
hop:: GoCD is up and running on http://localhost:18153
```
Configuring:
```
$ mkdir apps
$ cat <<EOF > apps/hop.yml
hop:
  plan: config_repo
  git_url: https://github.com/dudadornelles/hop.git
EOF
$ hop configure apps/
hop:: created pipeline 'myapp'
```

## Table of Contents

* [Introduction](#intro)
* [Reference](#reference)
* [Developing hop](#dev_hop)

## <a name="intro"></a>Introduction

Welcome to hop. Hop was created to speed up the process of provisioning, managing and configuring [GoCD](https://go.cd) through code.

Hop has three main concepts:

* Providers: a provider manages the lifecycle of the GoCD server and agents. It is a plugin system, so you can decide what to use as 
the underlying infrastructure by chosing/implementing a provider. Currently `hop` ships with a `local_docker` provider, that uses a
local docker socket to spin up the server and agents in your local docker daemon.  
* Plans: plans are an abstraction one-level higher then GoCD's pipelines. A plan is a collection of 1 or more pipelines. Plans are also 
a plugin system and are written in python using the [gomatic](https://github.com/SpringerSBM/gomatic) library. 
* Apps: apps or 'app definitions' are data structures with a 'plan', that get processed and transformed into pipelines. 

Hop is specially valuable for platforms where there are 'categories' of applications (that get built/deployed in similar ways), for now
you can define a 'plan' to represent a 'category' and thus streamline the process of creating and (most important) deploying new applications.

Install hop with python3 and pip3:
```
$ pip3 install git+https://github.com/dudadornelles/hop.git
```

## <a name="reference"></a>Reference

You'll find the available commands by running 
```
$ hop -h
usage: hop [-h] {init,provision,configure} ...

positional arguments:
  {init,provision,configure}
    init                initializes hop
    provision           provisions gocd
    configure           configures gocd

optional arguments:
  -h, --help            show this help message and exit
```

### init: 
Initializes hop in `dest_dir`. 
```
$ hop init -h
usage: hop init [-h] dest_dir

positional arguments:
  dest_dir              destination directory for hop

optional arguments:
  -h, --help            show this help message and exit
```

### provision:
Runs the `provision` method of the `provider`. The provider is specified in the `hop.yml` file. Eg:
```yaml
# hop.yml
provider:
  name: local_docker
```
```
$ hop provision -h
usage: hop provision [-h] [--hop-config HOP_CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  --hop-config HOP_CONFIG
                        path to hop.yml file (defaults to ./hop.yml)
```

### <a name="dev_hop"></a>Developing hop
Make sure you have docker running.

Hop is written in python 3.5, and we recommend you use virtualenv to develop hop. After cloning this repository, cd into `hop` and run:

```bash
virtualenv -p python3.5 .venv && source .venv/bin/activate
make init
```

The current integration test suite runs against a local Docker provider. This means you need to have Docker installed and running.
To run the tests:
```bash
make develop
make unit # unit tests
make integration # integration tests
make test # pylint, unit and integration tests
```

Take a look at the `Makefile` to see what else is available.

