""" Mozilla Change Integration Service Validator.

This lambda function is invoked by a change integration service producer like
mozillians.org.

Call:  synchronously using boto3('lambda') client.
Takes: an event containing a user profile
Does:  validate the user profile against the json schema for Mozilla users.

If the profile passes store it in kinesis for processing.

"""
import boto3
import logging
import os

# Import the Mozilla CIS library to facilitate core logic interaction.
from cis import processor
from cis.libs import utils

def handle(event, context):
    """This is the main handler called during function invocation."""

    sl = utils.StructuredLogger(
        name='cis-validator',
        level=logging.INFO
    )

    logger = logging.getLogger('cis-validator')

    p = processor.Operation(
        boto_session=boto3.Session(region_name='us-west-2'),
        publisher=event.get('publisher'),
        signature=event.get('signature'),
        encrypted_profile_data=event.get('profile')
    )

    result = p.run()

    logger.info('The result of the change operation was {r}'.format(r=result))

def wrapper():
    """Helper for easily calling this from a command line locally.
    Example: `python -c 'import main; main.wrapper()' | jq '.'`
    Only present to facilitate local testing without uploading to
    lambda.  Remove wrapper for production release.  Wrapper() concept
    courtesy of Graham Jones from ThreatResponse.
    """

    event_file = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'event.json'
    )

    with open(event_file, 'r') as event_data:
        profile_data = (event_data.read().encode('utf-8'))


    from cis.libs import encryption

    encryptor = encryption.Operation(boto_session=boto3.Session(region_name='us-west-2'))

    event = {
        'publisher': {'id': 'mozillians.org'},
        'signature': {},
        'profile': encryptor.encrypt(profile_data)
    }

    print(event)

    res = handle(event, None)