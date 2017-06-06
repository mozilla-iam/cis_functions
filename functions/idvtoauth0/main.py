""" This is the body of the lambda function """
import authzero
import boto3
import credstash
import json
import logging
import utils

def find_user(user_id):
    client = boto3.client('dyanmodb')


def handle(event, context):

    # Initialize Stream Logger
    # Log level can be environment driven later in development.
    log_level = logging.INFO
    utils.set_stream_logger(level=log_level)
    logger = logging.getLogger('cis-idvtoauth0')
    logger.info("Stream Processor initialized.")

    # New up the config object for CISAuthZero
    config = authzero.DotDict(dict())
    config.client_id = credstash.getSecret(
        name="cis.client_id",
        context={'app': 'cis', 'environment': 'dev'},
        region="us-east-1"
    )

    config.client_secret = credstash.getSecret(
        name="cis.client_secret",
        context={'app': 'cis', 'environment': 'dev'},
        region="us-east-1"
    )

    config.uri = credstash.getSecret(
        name="cis.uri",
        context={'app': 'cis', 'environment': 'dev'},
        region="us-east-1"
    )

    client = authzero.CISAuthZero(config)
    access_token = client.get_access_token()

    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        logger.info("Record is loaded.")
        logger.info("Processing {record}".format(record=record))
        user_id = record['dynamodb']['Keys']['user_id']['S']

        logger.info("Initial payload decoded.")
        logger.info("Searching for dynamo record for {u}".format(u=user_id))
        profile = {}

        # Push profile to webtask for processing

        # res = client.update_user(user_id, profile)
        # logger.info("Status of message processing is {s}".format(s=res))

    logger.info(
        'Successfully processed {} records.'.format(len(event['Records']))
    )

    return 'Successfully processed {} records.'.format(len(event['Records']))
