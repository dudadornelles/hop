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
  plan: pac # pac is the pipeline-as-code plan; this will look for a .gocd.yaml file in the repository 
  git_url: https://github.com/dudadornelles/hop.git
EOF
$ hop configure apps/
hop:: created pipeline 'myapp'
```

### Developing hop
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

