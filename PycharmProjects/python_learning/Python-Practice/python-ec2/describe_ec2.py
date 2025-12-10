import boto3
ec2 = boto3.client('ec2')
try:
    response = ec2.describe_instances(Filters=[{
        'Name': 'instance-state-name',
        'Values': [
            'stopped']
    }])
    found = False

    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            image = instance['ImageId']
            instance_type = instance['InstanceType']
            print(f"instance id : {instance_id}, state : {state}, image type : {image}, instance type : {instance_type}")
            found = True

    if not found:
        print("No instance are running")




except Exception as e:
    print(f"Error describing:str{e}")


