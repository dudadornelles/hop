# hop

Hop is a CLI tool written in python you can use to manage GoCD installations using docker and pipeline-as-code.

## TL;DR:
Installing
```bash
$ pip install hop
```
Initializing:
```bash
$ mkdir myGocd && cd myGocd
$ hop init
```
Provisioning:
```bash
$ hop provision
hop:: Provisioning GoC
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
