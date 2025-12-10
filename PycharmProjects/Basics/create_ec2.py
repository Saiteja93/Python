import boto3
from boto3 import client

ec2 = boto3.client('ec2')
response = ec2.run_instances( ImageId='ami-09c813fb71547fc4f',  # Replace with a valid AMI ID
        InstanceType='t2.micro',          # Replace with your desired instance type
        MinCount=1,
        MaxCount=1,)

for instance in response['Instances']:
    print(f"Instance ID: {instance['InstanceId']}")