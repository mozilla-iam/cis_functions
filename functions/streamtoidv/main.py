import base64
import json
import logging

from cis import encryption
from cis import validation
from cis import utils


def handle(event, context):
    sl = utils.StructuredLogger(
        name='cis-streamtoidv',
        level=logging.INFO
    )

    logger = logging.getLogger('cis-streamtoidv')

    logger.info("Stream Processor initialized.")

    for record in event['Records']:
        # Kinesis data is base64 encoded so decode here
        logger.info("Record is loaded.")

        payload = json.loads(
            base64.b64decode(record['kinesis']['data']).decode('utf-8')
        )

        logger.info("Initial payload decoded.")

        # Decrypt using the CIS library.  Each field is b64encoded as well.
        decrypted_payload = (
            json.loads(
                encryption.decrypt_payload(
                    ciphertext=base64.b64decode(payload['ciphertext']),
                    ciphertext_key=base64.b64decode(payload['ciphertext_key']),
                    iv=base64.b64decode(payload['iv']),
                    tag=base64.b64decode(payload['tag'])
                )
            )
        )

        logger.info("Payload decrypted.  Attempting storage in the vault.")

        # Store the result of the event in the identity vault
        res = validation.store_to_vault(decrypted_payload)

        logger.info(
            "Vault storage status is {status}".format(
                status=res
            )
        )

    logger.info(
        'Successfully processed {} records.'.format(len(event['Records']))
    )

    return 'Successfully processed {} records.'.format(len(event['Records']))
