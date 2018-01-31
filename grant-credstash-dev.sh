#!/bin/bash

region="us-west-2"
credstash_key_id="`aws --region $region kms list-aliases --query "Aliases[?AliasName=='alias/credstash'].TargetKeyId | [0]" --output text`"
role_arn="`aws iam get-role --role-name CISLambdaFunctionRoles-IDVtoIDMDriver-22W44UZPPRSX --query Role.Arn --output text`"
constraints="EncryptionContextEquals={app=cis,environment=dev}"

# Grant the ability to decrypt credstash secrets
aws kms create-grant --key-id $credstash_key_id --grantee-principal $role_arn --operations "Decrypt" --constraints $constraints --name cis-dev

region="us-west-2"
pykmssig_key_id="`aws --region $region kms list-aliases --query "Aliases[?AliasName=='alias/pykmssig'].TargetKeyId | [0]" --output text`"
role_arn="`aws iam get-role --role-name CIS-Staging-Roles-StreamValidator-1003AY11YNZN2 --query Role.Arn --output text`"

# Grant the validator the ability to decrypt signatures.
aws kms create-grant --key-id $pykmssig_key_id --grantee-principal $role_arn --operations "Decrypt" --name validator-can-validate-sigs
