# NIAS 2.0 - HISAMS - 2022-03-01
import boto3
import logging

import helpers.utils as utils
                                                                                                                                                                                        
logger = logging.getLogger()
logger.setLevel(logging.INFO)

""" *****************************************************************************************************
    *****************************************************************************************************
    *****************************************************************************************************
    If you'll be modifying this class, please observe code pattern.
    Consider others who will modify or read this.
    Add ddb nethods here which is not bound to a specific table.
    -HISAM
    *****************************************************************************************************
    *****************************************************************************************************
    *****************************************************************************************************
"""

class DDBUtils:
    
    def __init__(self):
        """ This holds the dynamodb resource instances per region """
        self.__ddb_resources = {}
        

    def batch_get_item(self, region: str, batch_keys: dict) -> dict:
        if not region in self.__ddb_resources.keys():
            self.__ddb_resources[region] = boto3.resource("dynamodb", region_name=region)

        try:
            response = self.__ddb_resources[region].batch_get_item(RequestItems=batch_keys)
            return response["Responses"]
        except Exception as error:
            logger.error(f"Error getting batch item: {utils.get_exception_str(error)}")
            return {}
