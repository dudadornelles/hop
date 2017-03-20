## hop-builds-hop

This example uses the `local_docker` provider to start hop. It should work with native docker and with `docker-machine`. Using `docker-machine` will allow you to run this example in a cloud provider by chosing the appropriate `--driver` for docker machine.

To run the example, from this folder run:
```
hop provision
hop configure apps/ --password admin
```

### Running it in ec2 with `docker-machine`

First, create a `docker-machine`:
```
AWS_INSTANCE_TYPE=t2.large docker-machine create --driver amazonec2 aws-sandbox
```

Notice that you can select a different instance type by changing the envirnment name.

Load the `docker-machine` environment by doing
```
eval $(docker-machine env aws-sandbox)
```

Then follow the instructions in the "hop-builds-hop" section of this readme to run it.

Make sure to change the admin password if you plan on using this tutorial to setup a more serious installation of hop.

