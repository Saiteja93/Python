import boto3

try:
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(Filters=[{
        'Name': 'instance-state-name',
        'Values': ['stopped']
    }])


    instance_ids = []
    for reservation in response['Reservations']:
        for  instances in reservation['Instances']:
            instance_ids.append(instances['InstanceId'])

    if instance_ids:
        print("Terminating instances in a stoped stage: ", instance_ids)
        terminated_instances = ec2.terminate_instances(InstanceIds = instance_ids)
        for instance in terminated_instances['Terminating']:
            print(f"Instance {instance['InstanceId']} is now {instance['CurrentState']['Name']}")
        else:
            print("No instances are found running")

except Exception as e:
    print("An Error occured", str(e))



