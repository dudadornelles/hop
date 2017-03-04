import boto3
from hop.core import hopconfig


class ECSGoServer(object):
    def __init__(self, ecs_client):
        self.client = ecs_client
    pass


class EC2ContainerInstance(object):
    AMI_ID = 'ami-dd104dbd'  # ecs optimized us-west-1

    def __init__(self, ec2_client):
        self.instance_id = hopconfig.get('provider', 'instance_id', None)
        self.client = ec2_client

    def provision(self):
        if self.instance_id:
            ecs_instance = self.client.create_instances(ImageId=EC2ContainerInstance.AMI_ID, MinCount=1, MaxCount=1)[0]
            self.instance_id = ecs_instance.id
            hopconfig.set('provider', 'instance_id', self.instance_id)


def provision():
    ec2_client = boto3.resource('ec2')
    ecs_client = boto3.client('ecs')

    container_instance = EC2ContainerInstance(ec2_client)
    container_instance.provision()

    server = ECSGoServer(ecs_client)
