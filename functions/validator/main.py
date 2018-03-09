""" Mozilla Change Integration Service Validator.

This lambda function is invoked by a change integration service producer like
mozillians.org.

Call:  synchronously using boto3('lambda') client.
Takes: an event containing a user profile
Does:  validate the user profile against the json schema for Mozilla users.

If the profile passes store it in kinesis for processing.

"""
import base64
import boto3
import json

# Import the Mozilla CIS library to facilitate core logic interaction.
from cis import processor

from cis.libs import utils
from cis.settings import get_config

config = get_config()


def handle(event, context):
    """This is the main handler called during function invocation."""

    config = get_config()
    custom_logger = utils.CISLogger(
        name=__name__,
        level=config('logging_level', namespace='cis', default='INFO'),
        cis_logging_output=config('logging_output', namespace='cis', default='stream'),
        cis_cloudwatch_log_group=config('cloudwatch_log_group', namespace='cis', default='')
    ).logger()

    logger = custom_logger.get_logger()

    # Encrypted profile packet contains ciphertext, iv, etc.
    encrypted_profile_packet = json.loads(base64.b64decode(event.get('profile').encode()))
    signature = event.get('signature', None)
    publisher = event.get('publisher', None)

    logger.debug('Attempting to push an event for publisher: {}'.format(publisher))

    if signature is not None or signature != {}:
        p = processor.ValidatorOperation(
            boto_session=boto3.Session(region_name='us-west-2'),
            publisher=publisher,
            signature=signature,
            encrypted_profile_data=encrypted_profile_packet
        )

        result = p.run()
        logger.info('The result of the change operation was {r}'.format(r=result))
    else:
        logger.error('No sigature was present. This operation was untrusted.')
        result = False

    logger.info('VALIDATOR: Processed 1 record.')
    return result
