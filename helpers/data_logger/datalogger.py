# NIAS2.0 - HISAMS - 20220-02-23
import logging

from helpers.utils import (
    get_current_epoch_time,
    modify_epoch_time,
    get_current_time,
    generate_random_id)
from helpers.data_logger.conf import (
    LOGS_TTL_DAYS,
    LOG_TYPES_REQUIRED_FIELDS
)
 
from helpers.ddbtools import DDBTools

from configuration import (
    REGION_OREGON,
    DDB_LOGS
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

"""
    If you'll be modifying this class, please observe code pattern.
    -HISAM
"""
class DataLogger:

    def __init__(self):
        self.__ddb_logs = DDBTools(DDB_LOGS, REGION_OREGON)

    
    def __get_required_table_attributes(self):
        return {
            "logId": generate_random_id(),
            "qryIdx": "QI",
            "expiryTimestamp": modify_epoch_time("ADD", "DAYS", LOGS_TTL_DAYS,  get_current_epoch_time()),
            "createTimestamp": get_current_time(),
        }


    def __is_kwargs_valid(self, **kwargs):
        REQUIRED_KWARGS = ["log_type", "data"]
        
        for arg in REQUIRED_KWARGS:
            if arg not in kwargs.keys():
                logger.info(f"Failed to log data. \"{arg}\" is required.")
                return False

            if not kwargs[arg]:
                logger.info(f"Failed to log data. \"{arg}\" requires value.")
                return False
        
        if kwargs["log_type"] not in LOG_TYPES_REQUIRED_FIELDS.keys():
            logger.info(f'Failed to log data. log_type: \"{kwargs["log_type"]}\" is not supported.')
            return False
        
        if not isinstance(kwargs["data"], dict):
            logger.info(f"Failed to log data. data must be a Dict.")
            return False
        
        for field in LOG_TYPES_REQUIRED_FIELDS[kwargs["log_type"]]:
            if field not in kwargs["data"].keys() or not kwargs["data"][field]:
                logger.info(f"Failed to log data. Required field: \"{field}\" does not exists from argument.")
                return False
        return True
        

    def log_data(self, **kwargs):
        if not self.__is_kwargs_valid(**kwargs):
            return
    
        log_data = self.__get_required_table_attributes()
        data = {}
        log_type = kwargs["log_type"]

        for attribute in  LOG_TYPES_REQUIRED_FIELDS[log_type]:
            data[attribute] = kwargs["data"][attribute]

        log_data.update({
            "logType": log_type.lower(),
            "data": data
        })

        logger.info(log_data)
        self.__ddb_logs.put_item(log_data)