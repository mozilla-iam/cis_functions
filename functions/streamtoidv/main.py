import base64
import boto3
import json

from cis import processor

from cis.libs import utils
from cis.settings import get_config

config = get_config()


def handle(event, context):
    config = get_config()
    custom_logger = utils.CISLogger(
        name=__name__,
        level=config('logging_level', namespace='cis', default='INFO'),
        cis_logging_output=config('logging_output', namespace='cis', default='stream'),
        cis_cloudwatch_log_group=config('cloudwatch_log_group', namespace='cis', default='')
    ).logger()

    logger = custom_logger.get_logger()

    logger.info("Stream Processor initialized for stage: streamtoidv.")

    for record in event['Records']:
        payload = json.loads(
            base64.b64decode(record['kinesis']['data']).decode('utf-8')
        )

        logger.info("Initial payload decoded for user: {}.".format(record.get('user_id')))
        try:
            p = processor.StreamtoVaultOperation(
                boto_session=boto3.Session(region_name='us-west-2'),
                publisher=record['kinesis']['partitionKey'],
                signature=None,
                encrypted_profile_data=payload
            )

            res = p.run()
        except Exception as e:
            logger.error('Error user: {} writing to dynamo due to: {}'.format(record.get('user_id'), e))
            res = False

        logger.info(
            "Payload decrypted for user {}.  Attempting storage in the vault.".format(
                record.get('user_id')
            )
        )

        # Store the result of the event in the identity vault

        logger.info(
            "Vault storage status is {status} for user {user}.".format(
                status=res, user=record.get('user_id')
            )
        )

    logger.info(
        'Successfully processed {} records.'.format(len(event['Records']))
    )

    return 'Successfully processed {} records.'.format(len(event['Records']))
