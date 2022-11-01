AWS Cross Account Roles
===

UPDATE: You can now use [IAM Identity Center](https://aws.amazon.com/iam/identity-center/) (previously AWS SSO) to achieve account switching
from a central location if your AWS accounts are members of an AWS Organization. For alternative methods, use may use this method.

This project helps you to manage multiple AWS accounts by having to maintain login credentials in just a single (Master) account.

This is achieved by granting the **Master** account access to resources in the **Member** account. When you setup the cross account roles in the Member account, you only need to paste the URL of the role in order to 'jump' into that account.

### Setting Up Cross Account Login:
1. Login to the Member account and run the CloudFormation templates in the us-east-1 region. Enter the Account ID of the Master account and other parameters as per your choice.
2. Once the roles have been setup, copy the URL of the roles from CFN Outputs and share it with the people you would like to give access to.
3. At this point you can safely delete all users / keys from the Member account.
4. You will also need to setup the Master account by running the CFN template of the Master account.
5. You can then setup users / groups in the Master account by attaching the policy created from the Master CFN template.
6. Once the users login to the Master account, they need to paste the link of the role of the Member account they wish to log in to. You will see a 'Switch Role' page from AWS to confirm the details.
7. Once you click on Switch Role, you are now in the Member account and you'll have access as per the role you have selected.

Thats all!
