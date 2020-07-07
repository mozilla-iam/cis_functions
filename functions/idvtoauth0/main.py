"""
This is the body of the lambda function for the Auth0 Identity driver of CIS
This function retrieves user profiles from the CIS ID Vault and sends the appropriate data to the Auth0 API
which is in turn used to create the id_token JWT and fill the user info endpoint ('profile' scope)
"""
import os

from cis.libs import utils
from cis.settings import get_config


config = get_config()


def handle(event, context):
    config = get_config()
    custom_logger = utils.CISLogger(
        name=__name__,
        level=config("logging_level", namespace="cis", default="INFO"),
        cis_logging_output=config("logging_output", namespace="cis", default="stream"),
        cis_cloudwatch_log_group=config("cloudwatch_log_group", namespace="cis", default=""),
    ).logger()

    logger = custom_logger.get_logger()
    logger.info("Stream Processor initialized for stage: idvtoauth0.")

    environment = os.getenv("ENVIRONMENT", "dev")

    if environment != "production":
        logger.info("Development stage recognized.  Applying to credstash.")

    logger.info("IDVTOAUTH0: Skipped all {} records.".format(len(event["Records"])))

    return "IDVTOAUTH0: Skipped all {} records.".format(len(event["Records"]))
