"""This script uses the master account credentials and fetches the AWS CLI Access Key and Secret Access Key
for a "member" account and sets it in the CLI environment.
"""
import boto3
import time
from getpass import getuser
from argparse import ArgumentParser


def sts_assume_role(accountid, rolename):
    """Returns a set of temporary security credentials (consisting
    of an access key ID, a secret access key, and a security token) 
    that you can use to access AWS resources.
    
    Args:
        accountid: String
        rolename: String
    Returns:
        Dictionary consisting of the Access Key, Secret Access Key,
        Session Token and the Expiration date/time for the given key.
    """
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

print("unset AWS_ACCESS_KEY_ID")
print("unset AWS_SECRET_ACCESS_KEY")
print("unset AWS_SESSION_TOKEN")
print("export AWS_ACCESS_KEY_ID=" + temporary_access_key['AccessKeyId'])
print("export AWS_SECRET_ACCESS_KEY=" + temporary_access_key['SecretAccessKey'])
print("export AWS_SESSION_TOKEN=" + temporary_access_key['SessionToken'])

# print key expiration date
utc_epoch = temporary_access_key['Expiration'].timestamp()
expiration_local_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(utc_epoch))
print("\nKeys will expire on: " + expiration_local_time + "\n")
