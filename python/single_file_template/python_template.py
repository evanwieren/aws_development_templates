from __future__ import print_function
import os
import sys
import logging
import traceback
import boto3
from botocore.exceptions import ClientError

##########
# Location for Global Variables
# Add to these as you desire.
##########

AWS_REGION = ''

##########
# Fixed functions for logging. 
# No need to edit.
##########
LOG_LEVELS = {'CRITICAL': 50, 'ERROR': 40, 'WARNING': 30, 'INFO': 20, 'DEBUG': 10}


def init_logging():
    # Setup loggin because debugging with print can get ugly.
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger('botocore').setLevel(logging.WARNING)
    logging.getLogger('nose').setLevel(logging.WARNING)

    return logger


def setup_local_logging(logger, log_level = 'INFO'):
    # Set the Logger so if running locally, it will print out to the main screen.
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if log_level in LOG_LEVELS:
        logger.setLevel(LOG_LEVELS[log_level])
    else:
        logger.setLevel(LOG_LEVELS['INFO'])

    return logger


def set_log_level(logger, log_level = 'INFO'):
    # There is some stuff that needs to go here.
    if log_level in LOG_LEVELS:
        logger.setLevel(LOG_LEVELS[log_level])
    else:
        logger.setLevel(LOG_LEVELS['INFO'])

    return logger

#########
# Add your code below.
#########


# This is a function that can be used to process global variables from the environment.
def process_global_vars():
    logger.info("Processing variables from environment.")
    try:
        global AWS_REGION
        AWS_REGION = os.environ.get('AWS_REGION', AWS_REGION)
        if AWS_REGION is '':
            logger.error("AWS_REGION must be set.")
            sys.exit(1)
        logger.debug("Completed execution of process_global_vars")
    except SystemExit:
        sys.exit(1)
    except:
        logger.error("Unexpected error!\n Stack Trace:", traceback.format_exc())


def lambda_handler(event, context):
    try:
        global logger
        logger = init_logging()
        logger = set_log_level(logger, os.environ.get('log_level', 'INFO'))

        logger.debug("Running function lambda_handler")
        process_global_vars()

    except SystemExit:
        logger.error("Exiting")
        sys.exit(1)
    except ClientError as e:
        if e.response['Error']['Code'] == 'SomeAWSErrorMessage':
            logger.error('Put Message Here')
        else:
            logger.error( "Unexpected AWS error: %s" % e )
    except ValueError:
        exit(1)
    except:
        print ("Unexpected error!\n Stack Trace:", traceback.format_exc())
    exit(0)


if __name__ == "__main__":
    logger = init_logging()
    os.environ['log_level'] = os.environ.get('log_level', "INFO")

    logger = setup_local_logging(logger, os.environ['log_level'])

    event = {'log_level': 'INFO'}
    os.environ['AWS_REGION'] = os.environ.get('AWS_REGION', "us-east-2")


    # Add default level of debug for local execution
    lambda_handler(event, 0)
