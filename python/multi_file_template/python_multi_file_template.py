# This will connnect to an AWS account and provide a report of resources that
# are not in compliance. 

from __future__ import print_function
import os
import sys
import traceback
import boto3
from botocore.exceptions import ClientError
import helpers

##########
# Location for Global Variables
# Add to these as you desire.
##########

AWS_REGION = ''


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
        logger = helpers.logger.init_logging()
        logger = helpers.logger.set_log_level(logger, os.environ.get('log_level', 'INFO'))

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
    logger = helpers.logger.init_logging()
    os.environ['log_level'] = os.environ.get('log_level', "INFO")

    logger = helpers.logger.setup_local_logging(logger, os.environ['log_level'])

    event = {'log_level': 'INFO'}
    os.environ['AWS_REGION'] = os.environ.get('AWS_REGION', "us-east-2")


    # Add default level of debug for local execution
    lambda_handler(event, 0)
