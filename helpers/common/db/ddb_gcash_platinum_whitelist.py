from __future__ import annotations

import logging

from helpers.ddbtools import DDBTools

import configuration as configs

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class GCashPlatinumWhitelistDdb:

    def __init__(self):
        self.__ddb_gcash_platinum_whitelist = DDBTools(configs.DDB_GCASH_PLATINUM_WHITELIST, configs.REGION_OREGON)

    def get_all_data(self, limit, last_evaluated_key) -> list:
        return self.__ddb_gcash_platinum_whitelist.get_all(limit, last_evaluated_key)
        