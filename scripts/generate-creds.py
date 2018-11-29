import boto3
import time
import datetime
import platform
import subprocess
from getpass import getuser


def set_system_variables(access_key):
    os = platform.system()
    
    if os is 'Linux' or 'Darwin':
        print('Yes ' + os)
    elif os is 'Windows':
        print('not set.')


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


print("Generating AWS CLI credentials...\n")

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--auto", choices=['y', 'n'],
                    help="Automatically set the environment variables", default='n')
parser.add_argument("--account",
                    help="AWS account number of the member stack", required=True)
parser.add_argument("--role",
                    help="IAM role to assume in the member stack", required=True)

args = parser.parse_args()
print(args)
print(args.account)
print(args.role)
exit()

client = boto3.client('sts')
temporary_access_key = sts_assume_role(None, None)

print("Copy and paste this in a terminal or allow the script to set it for you...\n")
print("set AWS_ACCESS_KEY_ID=" + temporary_access_key['AccessKeyId'])
print("set AWS_SECRET_ACCESS_KEY=" + temporary_access_key['SecretAccessKey'])
print("set AWS_SESSION_TOKEN=" + temporary_access_key['SessionToken'])

# key_expriration_date_local = temporary_access_key['Expiration'].astimezome()
# print("\nKeys will expire on: " + key_expriration_date_local.strftime("%Y-%m-%d %H:%M:%S"))
print("\n")



# subprocess.call(["echo", "Generating AWS CLI credentials..."])