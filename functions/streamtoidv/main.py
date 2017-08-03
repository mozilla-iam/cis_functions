import boto3
import base64
import json
import logging

from cis import processor
from cis.libs import utils

def handle(event, context):

    print(event)

    sl = utils.StructuredLogger(
        name='cis-streamtoidv',
        level=logging.INFO
    )

    logger = logging.getLogger('cis-streamtoidv')

    logger.info("Stream Processor initialized.")

    for record in event['Records']:

        print(record)
        # Kinesis data is base64 encoded so decode here
        logger.info("Record is loaded.")

        payload = json.loads(
            base64.b64decode(record['kinesis']['data']).decode('utf-8')
        )

        logger.info("Initial payload decoded.")

        p = processor.Operation(
            boto_session=boto3.Session(region_name='us-west-2'),
            publisher=record['kinesis']['partitionKey'],
            signature=None,
            encrypted_profile_data=payload
        )


        res = p.run()

        logger.info("Payload decrypted.  Attempting storage in the vault.")

        # Store the result of the event in the identity vault

        logger.info(
            "Vault storage status is {status}".format(
                status=res
            )
        )

    logger.info(
        'Successfully processed {} records.'.format(len(event['Records']))
    )

    return 'Successfully processed {} records.'.format(len(event['Records']))

def wrapper():
    sample = {
        'Records': [
            {
                'kinesis':
                     {
                         'kinesisSchemaVersion': '1.0',
                         'partitionKey': 'mozillians.org',
                         'sequenceNumber': '49575654460217106988212223920233322613632875453204135938',
                         'data': 'eyJjaXBoZXJ0ZXh0IjogInRWcWNNV2dUS0NrN2JNck12UEgyamovSmJYSDhNcHc4NzE1QS9USlZMQlRsVFdVSkJzc2dwb1Q4M2NSRnFKd3NRV1pFeHhnakR6YW5CWTlRYW5RVTRUaWZJbExQNWRybURydklFYy9zeVhabUJHYTFTc2hwSkl4aC9oUTU1MzdlNWZXRno0QnR3UEVpb2xyang1QlkzSW1iKzVPN1NvcVlaSEQ2RWtNRjhCSTliMEZvSVh0WU40WEtyRlpaK1pZTGkyNmNSa2pPYmxnNTJFRENlNDV2RnpJLy9uSVp3UmMyYmRxQ1lqeXlvQXRRd2ZueFpXRjkzTFdib1pXR0hJU04wOTMrRm1GL1pKb3NxQ2Q5VEJabGxPMVVhQWdyUXd6bEU2NFlFWmRZczV3K2ZXY3dTN0RMWURwUUY0L3hMNjhhMHRQSWZndWNnSDlzRHZiY081clp4Z05pRko4ZktsNksrSUgwS3NXNHpmMDNRcWE3YytvRXo2TGVRVFVuRzU1MXNLT1FOK25OVUtNNmVqcEZVSWFyVzZTc3YyY3dOdGFTa09RT284aHhDTnNTRkpBNTUxL2NPampMdVlCTVhHQzNZNXlmbmo4NjNueGN5bFVjU1RKOXNiK3hJc0xBQkd2WDdIVS9WY0tEUFlyOXRTNm5yelhmYmhtdkN6RFBSM2VlYjBKK0tvY05Sck90Ym1kRzFGSXdxY0V2TkN3R2hEb0tGemxHYWRJU3dLVWJYTERmTGtpR3A2OHVkQ3NDYSswbGpHVlFhRm9kQk1JSDNQcDBOeUhrM3ZsSHFWWGpOa0VVczRwVCtjTEs5UiswbTByY0oyUTZIYTgySDloNXdXQVNza3YzQzFaSDY3MmVKcDZoSnJOckdSUmtkOGZINW5SUVlEM29MbEY5cC9RN2NXUnJaZUhBSVdaV0F3b3dxY2w3Z0hZdVhObFo0bWxIZEFSZDVnaW9CSG9aQkd1cmNnYjVoZkR4WWdjSWFOcFhROW51K1BnQlFYRlEwUG9nOFBqMkpCNVIwMXNpM2J6OWFNdDFtUDBEemc4RS9tRTZUYiszNTNNcitrbHhveU9uNXdUNnh6dDdOVDZkMDgzRGxaS0JQNnpXUHdLOHdNZjA1TGlQS0J5SGtOVG41OHhNT0N1Sy9TOWdSMzhJeXZNakNlaVJRdjlveWozTjR0TmNmOEtJbmtoYkpnQ0Zhb095YVFIbndwOGR1RVZPcGc2ZnI4MDRjelEzZDF5Z2VJVzFyNnc5T0lVbVh4K2xickFyNGxxU0J4eUpUTkovL3VKbk5mYTFDOGVDQXk0ekZCQ3huRmd6Zi9vVkdianQzdnBDbUluOUZRR2t2Zi8vc0hCc1FHMFcrNDcvMEo3SG1vTTNCTFluSngydzhwMDJqd3hWOUVIUmR0OThyTHAwQUFMbzYyeGtQaTdtU1RxbkUzQlFnajJkMlUvcVpGWTlmNGFJTWRiK0VrTUpjTDFOUzJKdzE0NFIyTlhQYVZoNXVxL3VXSGM4djJZbnpJZ2xNS3lWaEsyeWFqVVNnNzVYUjRFSXJ2WlpzeWxsdTJ1SjZoN0dxTmRreVZ6amRMQUVqWnVKYmRNdmtZVGtpQ1doKzEyZUQwZ2VGNVlWVEthT0YzSCt6ak01aGpYbXZsemFPZjZPR29lV25kRzhlTmtnZm5FeGxQRGFHeTZScFRhTmIxVDZsaGlXYTV1cXRya3B2aG1ZSG9VV2FEUElyYzF2LzhqN09GZTBiUGFraW9XZURCcW8rTnNweEJ4OUZVUTN1VU9nR25jbmJpQVMwUVRDelVTMTZWUEdtbjE5SXUzMU5KZGdWRS84dmxYZUEvNDBqNjZJVWlDYkFWQ3Z1azcxV29laHRqb0grbGNXOG1VSWdreFBoMlZpaVB6eWNuS2xQeC9DU0xyYzlPeGlBVnJrV3krMVFmRWplWUdVMGRMa3VVYW4xT09yT25nc1J4SFFzSzZ3Nm51NldKQTA1b1I5RDZ6YkVvQUI3bC85RWhHZ2JUMHF5Zjdoa0dJeWNXSm5COUlKRGJlZFFSMThBMitiamVmU05mQVREQjI2L1ZNRjRmMWR1cGduMkd0QWVGM0g1bEhzVTZ1V1NXTis4MkZjcUVwUkJWT1Y4M3ozSkU1VXZYNEswczNxYWV5cVlHM0JWTkUxNFN5TzJ0bDdsekt1ZEZEODRsd1hHdlI3aHV5a2plNVBmOU9yY3FITTZXNm9vc3hYaVE5ODB0OXl0YUc2SVBzL1IwMGw4L2cyMit5RDRVaGhvQTdIcExGNUxydCtYUUo0YXR1TERoNXBIWXB4N3RqWHN4RFMzbG54QTBVaVZZWVUvZTcxQkQySFg5VlJyN1VicGN1R2JyQ3o4VVVPUmo1NVpuaEV2Um43bU9qSm5RakdtdkVibnhoL0Z2SDUzYmZQb01xN2MrSlFkSFMvWGZxMm9TeVNLYXJub0FaWDJHODZIdHg0U3h1c2wxK212R1FMWWg1VEZoZFgvTTBOSkxiSUpNWStzOXprdjJvdm9TRm1nU1EyTUpJTXhwQlJLOHNhb1l5b3JiaUdWYXpqZEdNZjk1Q0MxNVlFcGhDTWx4RUFzci9RTXYxa2puT2xJYXJiNXMxQW1VbkwzRTEvQmowblZoNXFBY1hRZTQvZEVkM25NU0h2M1lGcHZpVzkwK0lOL2FFdUppREUyMkJtTm1jdlljT1Q3TXRLTGZGWEtBQVRVVWxMOHQ3SXJ6Z1BkRjN6a0diQUVLSE9WamsxdGp4bHBQdGoxYXJpZTQySkhweTJsVG1WakJxMHB1bWQiLCAiY2lwaGVydGV4dF9rZXkiOiAiQVFJREFIaERRMDdaN2RZUnZEQlBVV0Zudk15YWFaejNkcStlL2FRVWkrbTIrbFY2MlFHSitNSGJVTXFQZXBPcE1WOFNOVWM0QUFBQWZqQjhCZ2txaGtpRzl3MEJCd2FnYnpCdEFnRUFNR2dHQ1NxR1NJYjNEUUVIQVRBZUJnbGdoa2dCWlFNRUFTNHdFUVFNdEJmTCtiSFlqNWNzbzZzeEFnRVFnRHM2aWc3VDRRMjR0S0pyZmtVVXllVkg5LzVpRU5vUURTUmZUWkM0aEZZcnUzV2VXbjc0VlpLS0RxMlUrbm9ra1luN3VpQ1hUbjlRMXpHR2NRPT0iLCAiaXYiOiAiMHRwWTZKTG90WmhTMWVIWCIsICJ0YWciOiAiSUhiS2FSUGpoY0JGQ2dVb2ZSZHA3dz09IiwgInNpZ25hdHVyZSI6IHt9fQ==',
                         'approximateArrivalTimestamp': 1501732692.012
                     },
                'eventSource': 'aws:kinesis',
                'eventVersion': '1.0',
                'eventID': 'shardId-000000000000:49575654460217106988212223920233322613632875453204135938',
                'eventName': 'aws:kinesis:record',
                'invokeIdentityArn': 'arn:aws:iam::656532927350:role/CISLambdaFunctionRoles-StreamToIDV-T5IH2261NJZM',
                'awsRegion': 'us-west-2',
                'eventSourceARN': 'arn:aws:kinesis:us-west-2:656532927350:stream/CISStreamandDB-CISInputStream-1FTGC3KE4NN9U'
            }
        ]
    }

    res = handle(sample, context={})
    print(res)
