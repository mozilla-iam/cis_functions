""" Mozilla Change Integration Service Validator.

This lambda function is invoked by a change integration service producer like
mozillians.org.

Call:  synchronously using boto3('lambda') client.
Takes: an event containing a user profile
Does:  validate the user profile against the json schema for Mozilla users.

If the profile passes store it in kinesis for processing.

"""
import base64
import logging
import os
# Import the Mozilla CIS library to facilitate core logic interaction.
from cis import encryption
from cis import streams
from cis import validation
from cis import utils

def handle(event, context):
    """This is the main handler called during function invocation."""

    sl = utils.StructuredLogger(
        name='cis-validator',
        level=logging.INFO
    )

    logger = logging.getLogger('cis-validator')

    payload = {}
    payload['ciphertext'] = event['ciphertext']
    payload['tag'] = event['tag']
    payload['ciphertext_key'] = event['ciphertext_key']
    payload['iv'] = event['iv']

    # Require publisher to add partition key in event
    publisher = "mozillians.org"
    #publisher = str(base64.b64decode(event.get('publisher').decode('utf-8')))


    # Initialize Stream Logger
    # Log level can be environment driven later in development.

    logger.info("Validator successfully initialized.")

    payload_status = validation.validate(publisher, **payload)

    if payload_status is True:
        logger.info("Payload is valid sending to kinesis.")

        decrypted_profile = encryption.decrypt_payload(**payload)

        res = streams.publish_to_cis(
            data=decrypted_profile,
            partition_key=publisher
        )

        return True
    else:
        logger.info("Payload is invalid rejecting payload.")
        return False

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
        event = (event_data.read().encode('utf-8'))

    event = encryption.encrypt_payload(event)
    res = handle(event, None)