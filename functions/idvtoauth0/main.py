""" This is the body of the lambda function """

import base64
import json
import logging
import utils

def handle(event, context):

    # Initialize Stream Logger
    # Log level can be environment driven later in development.
    log_level = logging.INFO
    utils.set_stream_logger(level=log_level)
    logger = logging.getLogger('cis-idvtoauth0')
    logger.info("Stream Processor initialized.")

    print(event)

    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        logger.info("Record is loaded.")

        payload = json.loads(
            (record['dynamodb']['NewImage']).decode('utf-8')
        )

        logger.info(payload)

        logger.info("Initial payload decoded.")

        # To do Push the event out to the auth0 webtask for processing

        # Kang puts request code here!
        # This will call a bit of nodejs then get result
        # If success log success
        # If fail dead letter the event ( POST OKR )

    logger.info(
        'Successfully processed {} records.'.format(len(event['Records']))
    )

    return 'Successfully processed {} records.'.format(len(event['Records']))
