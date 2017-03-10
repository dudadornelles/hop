# hop

Hop is a CLI tool written in python you can use to manage GoCD installations using docker and pipeline-as-code.

## TL;DR:
The fastest way to try `hop` is to use the `hop-builds-hop` example. To try it, clone this very repository, install hop and provision the example.

Hop has the following dependencies:
```
python3.5
pip3
htpasswd
docker
```
Install hop with:
```
$ pip3 install git+https://github.com/dudadornelles/hop.git
```
Then `cd hop/examples/hop-builds-hop/` and run:
```
$ hop provision
$ hop configure apps/
```

Open your browser on `https://localhost:18154` and login as `admin:admin`. In no time you'll see the `hop` pipeline running.


## Table of Contents

* [Introduction](#intro)
* [Getting Started](#getting_started)
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


## <a name="getting_started"></a> Getting Started

#### Dependencies
```
python3.5
pip3
htpasswd
docker
```

#### Installing 
Install with hop and python3 and pip3:
```
$ pip3 install git+https://github.com/dudadornelles/hop.git
```

#### Initializing:
Initialize `hop` in a destination directory:
```
$ hop init myGoCD
```
Running `hop init` will place ask your for a password. Remember this passwrod as it is the GoCD admin password. When `hop init` is done,
cd into your `hop` root and you will find two files:

* hop.yml: the main configuration file for hop. 
* passwd: the [htpasswd](http://www.htaccesstools.com/articles/htpasswd/) password file. 


#### Provisioning:
Run `hop provision` from the root folder to invoke the provider and start the GoCD server and agents.
```
$ cd myGoCD
$ hop provision
hop:: Provisioning GoCD
hop:: Using local_docker provider
hop:: Verifying presense of images
hop:: Starting GoCD server from gocdhop/myGoCD-server
hop:: GoCD not yet initialized at https://localhost:18154. Will try again in 15 secs
hop:: GoCD not yet initialized at https://localhost:18154. Will try again in 15 secs
hop:: GoCD is up and running
hop:: Updating passwd
hop:: Adding security config to cruise-config.xml
hop:: Starting myGoCD-agent-0 from gocdhop/hop-agent
hop:: Starting myGoCD-agent-1 from gocdhop/hop-agent
hop:: GoCD is up and running
hop:: GoCD is up and running on https://localhost:18154
```

#### Configuring:

To configure hop, create a folder for your apps (we call this a 'context'):
```
$ mkdir apps
```
Add a app definition in a yaml file inside that context.

```
# apps/hop.yml
hop:
  plan: config_repo
  git_url: https://github.com/dudadornelles/hop.git
```

Run `hop configure <context>`
```
$ hop configure apps/
hop:: executing 'config_repo' plan for hop
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

### configure
Looks for apps in `context` and executes them using the declared `plan`. Example:
```yaml
# apps/hop.yaml
hop:
  plan: config_repo
  git_url: https://github.com/dudadornelles/hop
```
Then running `hop configure apps/` will add the `git_url` as a yaml config repo in GoCD.
```
$ hop configure -h
usage: hop configure [-h] [--hop-config HOP_CONFIG] [--host HOST]
                     [--user USER] [--password PASSWORD]
                     context

positional arguments:
  context               A folder with a set of yml files for app definitions

optional arguments:
  -h, --help            show this help message and exit
  --hop-config HOP_CONFIG
                        path to hop.yml file (defaults to ./hop.yml)
  --host HOST           GoCD host. e.g: localhost:8153
  --user USER           User with admin role
  --password PASSWORD   Password for user
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

