""" This is the body of the lambda function """

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

        # To-Do
        # Parse the payload to look for group list
        # Rebuild those groups in the group table

    return None
