from __future__ import annotations

import logging

from datetime import datetime, timedelta

from helpers.ddbtools import DDBTools

import configuration as configs

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CaseCreatedDdb:

    def __init__(self):
       self.__ddb_case_created = DDBTools(configs.DDB_CASE_CREATED, configs.REGION_SINGAPORE)


    def __get_data_by_index(self, **kwargs) -> list:
        key_name = kwargs.get("key_name", "")
        index_name = kwargs.get("index_name", "")
        index_value = kwargs.get("index_value", "")
        filter_expression = kwargs.get("filter_expression", "")

        case_created_res = self.__ddb_case_created.get_item_by_index(key_name, index_value, index_name, filter_expression=filter_expression)
        result_count = len(case_created_res)    
        
        if result_count > 0:
            return case_created_res
        else:
            return []
        
    
    def get_data_within_hours_by_subscriber_no(self, **kwargs) -> list:
        hours = kwargs.get("hours", 7)
        subscriber_no = kwargs.get("subscriber_no", "")

        hours_ago = (datetime.now() - timedelta(hours=hours)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        filter_expression = {
            "attribute": "DateOfRequest",
            "condition": "gt",
            "value": hours_ago
        }

        return self.__get_data_by_index(
                key_name="SubscriberNumber",
                index_name="SubscriberNumber-index",
                index_value=subscriber_no,
                filter_expression=filter_expression)


    def get_data_within_hours_by_account_no(self, **kwargs) -> list:
        hours = kwargs.get("hours", 7)
        account_no = kwargs.get("account_no", "")

        hours_ago = (datetime.now() - timedelta(hours=hours)).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        filter_expression = {
            "attribute": "DateOfRequest",
            "condition": "gt",
            "value": hours_ago
        }

        return self.__get_data_by_index(
                key_name="AccountNumber",
                index_name="AccountNumber-index",
                index_value=account_no,
                filter_expression=filter_expression)      
        