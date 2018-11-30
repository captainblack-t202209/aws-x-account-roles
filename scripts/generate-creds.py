import boto3
import time
from getpass import getuser
from argparse import ArgumentParser


def sts_assume_role(accountid, rolename):
    session_name = getuser() + "-" + str(time.time())
    
    response = client.assume_role(
        RoleArn='arn:aws:iam::' + accountid + ':role/' + rolename,
        RoleSessionName=session_name
    )

    access_key = {
        "AccessKeyId": response['Credentials']['AccessKeyId'],
        "SecretAccessKey": response['Credentials']['SecretAccessKey'],
        "SessionToken": response['Credentials']['SessionToken'],
        "Expiration": response['Credentials']['Expiration']
    }

    return access_key


# check command line arguments
parser = ArgumentParser()
parser.add_argument("--auto", choices=['y', 'n'], default='n',
                    help="Automatically set the environment variables received from STS")
parser.add_argument("--account",
                    help="12 digit AWS account number of the member stack", required=True)
parser.add_argument("--role",
                    help="IAM role to assume in the member stack", required=True)


args = parser.parse_args()

# check if account id and role were passed to the cli
if args.account or args.role is not None:
    if len(args.account) is not 12:
        print('''\nAWS account numbers must be of 12 digits. '''
        '''Please enter a valid AWS account number and try again.\n''')
        exit()

print("\nGenerating AWS CLI credentials...\n")

# Establish STS connection and get credentials
client = boto3.client('sts')
temporary_access_key = sts_assume_role(args.account, args.role)

print("set AWS_ACCESS_KEY_ID=" + temporary_access_key['AccessKeyId'])
print("set AWS_SECRET_ACCESS_KEY=" + temporary_access_key['SecretAccessKey'])
print("set AWS_SESSION_TOKEN=" + temporary_access_key['SessionToken'])

# print key expiration date
utc_epoch = temporary_access_key['Expiration'].timestamp()
expiration_local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(utc_epoch))
print("\nKeys will expire on: " + expiration_local_time + "\n")


# def set_system_variables(access_key):
#     os = platform.system()
    
#     if os is 'Linux' or 'Darwin':
#         print('Yes ' + os)
#     elif os is 'Windows':
#         print('not set.')

# check if credentials is to be automatically set
# if args.auto is 'y':
#     print('Setting AWS credentials...')
#     subprocess.call(["export AWS_REGION=ap-southeast-2"], shell=True)