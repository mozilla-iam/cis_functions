""" This is the body of the lambda function """
import authzero
import boto3
import credstash
import logging
import os


from botocore.exceptions import ClientError
from cis.libs import utils


def find_user(user_id):
    table_name = os.getenv('CIS_DYNAMODB_TABLE', None)
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table(table_name)
    try:
        res = table.get_item(
            Key={
                'user_id': user_id
            }
        )
        profile = res.get('Item', None)

        # Fix null values workaround for DynamoDB limitation
        if profile and profile['groups'] == 'NULL':
            profile['groups'] = []

        return profile

    except ClientError:
        return None


def _denullify_empty_values(data):
    """
    Opposite of https://github.com/akatsoulas/cis/blob/8c8da24b2c215d02f5e14dec7a94da6b1792c8c9/cis/publisher.py#L80
    Remove `NULL` and replace it back by empty string
    """
    new = {}
    for k in data.keys():
        v = data[k]
        if isinstance(v, dict):
            v = _denullify_empty_values(v)
        if v == 'NULL':
            new[v] = ''
        else:
            new[v] = v
    return new


def handle(event, context):
    utils.StructuredLogger(
        name='cis-idvtoauth0',
        level=logging.INFO
    )

    logger = logging.getLogger('cis-idvtoauth0')
    logger.info("Stream Processor initialized.")

    environment = os.getenv('ENVIRONMENT', 'dev')

    if environment == 'production':
        environment = 'prod'
    else:
        logger.info('Development stage recognized.  Applying to credstash.')
        environment = 'dev'

    # New up the config object for CISAuthZero
    config = authzero.DotDict(dict())
    config.client_id = credstash.getSecret(
        name="cis.client_id",
        context={'app': 'cis', 'environment': environment},
        region="us-west-2"
    )

    config.client_secret = credstash.getSecret(
        name="cis.client_secret",
        context={'app': 'cis', 'environment': environment},
        region="us-west-2"
    )

    config.uri = credstash.getSecret(
        name="cis.uri",
        context={'app': 'cis', 'environment': environment},
        region="us-west-2"
    )

    client = authzero.CISAuthZero(config)
    client.get_access_token()

    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        logger.info("Record is loaded.")
        logger.info("Processing {record}".format(record=record))
        user_id = record['dynamodb']['Keys']['user_id']['S']

        logger.info("Initial payload decoded.")
        logger.info("Searching for dynamo record for {u}".format(u=user_id))
        profile = find_user(user_id)

        logger.info("Status of profile search is {s}".format(s=profile))

        if profile is not None:
            # Profile whitelisting. This allows to select which user profiles are
            # to be integrated using CIS, mainly for transitioning purposes.
            # See also: https://mozillians.org/en-US/group/cis_whitelist
            logger.info("The profile is {}".format(profile))

            if 'mozilliansorg_cis_whitelist' in profile.get('groups', []):
                # XXX Force-integrate LDAP groups as these are synchronized
                # from LDAP to Auth0 directly.
                # This is to be removed when LDAP feeds CIS.
                try:
                    upstream_user = client.get_user(user_id)

                    if 'groups' in upstream_user.keys():
                        for g in upstream_user['groups']:
                            if g not in profile['groups']:
                                profile['groups'].append(g)
                                logger.info("Forced re-integration of LDAP group {}".format(g))

                   # XXX Force-convert `NULL` back to empty string, to accomodate the DynamoDB work-around found at:
                   # https://github.com/akatsoulas/cis/blob/8c8da24b2c215d02f5e14dec7a94da6b1792c8c9/cis/publisher.py#L80
                   # So that RP gets the correct value returned (which is empty string)
                   # profile = _denullify_empty_values(profile)

                    res = client.update_user(user_id, profile)
                except Exception as e:
                    """Temporarily patch around raising inside loop until authzero.py can become part of CIS core."""
                    res = e
            else:
                res = "not processed"
                pass
            logger.info("Status of message processing is {s}".format(s=res))
        else:
            logger.critical(
                "User could not be matched in vault for userid : {user_id}".format(user_id=user_id)
            )

    logger.info(
        'Successfully processed {} records.'.format(len(event['Records']))
    )

    return 'Successfully processed {} records.'.format(len(event['Records']))
