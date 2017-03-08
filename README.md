# hop

Hop is a CLI tool written in python you can use to manage GoCD installations using docker and pipeline-as-code.

## TL;DR:

OBS: this is not currently implemented, is more of an idea of what the end state should look like

Installing
```bash
$ pip install hop
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
hop:: Starting a GoCD server from hopgocd/hop-server
hop:: Starting 2 GoCD agents from hopgocd/hop-server
hop:: GoCD running at https://localhost:8154/go
```
Configuring:
```
$ echo <EOF
myapp:
  plan: custom_pipeline_plan
  git_url: https://github.com/dudadornelles/hop.git
  stages:
    - unit-test:
      command: make develop test
EOF > apps/myapp.yml
$ hop configure
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

