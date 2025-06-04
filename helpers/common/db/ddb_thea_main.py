from __future__ import annotations

import logging

from helpers.ddbtools import DDBTools

import configuration as configs

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class TheaMainDdb:

    def __init__(self):
       self.__ddb_thea_main = DDBTools(configs.DDB_THEA_MAIN, configs.REGION_OREGON)

    def get_data_by_msisdn(self, key_name, index_name, index_value) -> list:
        thea_main_res = self.__ddb_thea_main.get_item_by_index(key_name, index_value, index_name, filter_expression="")
        result_count = len(thea_main_res)     
        if result_count > 0:
            return thea_main_res
        else:
            return []
