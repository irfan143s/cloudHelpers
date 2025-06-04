from __future__ import annotations

import logging

from resources.common.enums.cx_channels import CxChannels

import resources.common.mapping.channelid_channelalias as channelid_channelalias_mapping
import resources.tableattributes as tableattributes

from helpers.ddbtools import DDBTools

import helpers.common.utils.str as str_utils
import helpers.utils as utils

import configuration as configs

logger = logging.getLogger()
logger.setLevel(logging.INFO)

TTL_EXPIRY_DAYS = 180

class SubscriberCrossChannelMatching:

    __ddb_xchannel_matching = None
    __clsname = "SubscriberCrossChannelMatching -"


    def __init__(self, cx_channel: CxChannels) -> None:
        self.__cx_channel = cx_channel

    
    def __init_instance_members(self):
        if self.__cx_channel == CxChannels.FACEBOOK:
            self.__cx_channel_alias = channelid_channelalias_mapping.FACEBOOK[self.__channel_id]
        elif self.__cx_channel == CxChannels.TWITTER:
            self.__cx_channel_alias = channelid_channelalias_mapping.TWITTER[self.__channel_id]
        else:
            self.__cx_channel_alias = "NONE"


    def update_matching(self, **kwargs) -> None:
        logger.info(f"{self.__clsname} kwargs provided: {kwargs}")

        if not self.__is_ivalid_input(**kwargs):
            logger.info(f"{self.__clsname} invalid input!")
            return

        self.__init_instance_members()

        if self.__account_no:
            matching_data = self.__get_rec_by_account_no()

            if matching_data:
                logger.info(f"{self.__clsname} account_no matching already exists!")
                self.__update_entry(matching_data[tableattributes.ID])
            else:
                logger.info(f"{self.__clsname} account_no matching does not exists!")
                self.__create_entry()

        elif self.__msisdn:
            matching_data = self.__get_rec_by_msisdn()
            if matching_data:
                logger.info(f"{self.__clsname} msisdn matching already exists!")
                self.__update_entry(matching_data[tableattributes.ID])
            else:
                logger.info(f"{self.__clsname} msisdn matching does not exists!")
                self.__create_entry()
                
            
    def __create_entry(self) -> None:
        self.__ddb_xchannel_matching = self.__get_ddb_xchannel_matching_instance()

        item = {
            tableattributes.ID: utils.generate_random_id(),
            tableattributes.USER_ID: self.__user_id,
            tableattributes.EXPIRY_TIMESTAMP: utils.modify_epoch_time("add", "days", TTL_EXPIRY_DAYS,  utils.get_current_epoch_time()),
            tableattributes.UPDATE_TIMESTAMP: utils.get_current_time(),
            tableattributes.UPDATE_DAY: utils.get_current_datetime().strftime("%Y%m%d")
        }   
        item[tableattributes.CHANNEL] = f"{self.__cx_channel.value} {self.__cx_channel_alias}"

        if self.__account_no:
            item[tableattributes.ACCOUNT_NO] = self.__account_no
        
        if self.__msisdn:
            item[tableattributes.MSISDN] = self.__msisdn

        if self.__cx_channel == CxChannels.FACEBOOK and self.__fb_identity_key:
            item[tableattributes.IDENTITY_KEY] = self.__fb_identity_key
        
        logger.info(f"{self.__clsname} Channel Subscriber Matching entry: {item}")
        self.__ddb_xchannel_matching.put_item(item)


    def __update_entry(self, id) -> None:
        self.__ddb_xchannel_matching = self.__get_ddb_xchannel_matching_instance()
        try:
            self.__ddb_xchannel_matching.update_item(tableattributes.ID, id, {
                    tableattributes.UPDATE_TIMESTAMP: utils.get_current_time(),
                    tableattributes.UPDATE_DAY: utils.get_current_datetime().strftime("%Y%m%d"),
                    tableattributes.EXPIRY_TIMESTAMP: utils.modify_epoch_time("add", "days", TTL_EXPIRY_DAYS,  utils.get_current_epoch_time()),
                })
        except Exception as error:
            logger.info(f"{self.__clsname} error updating entry: {utils.get_exception_str(error)}")


    def __is_ivalid_input(self, **kwargs) -> bool:
        self.__channel_id = str(kwargs.get("channel_id", ""))
        self.__user_id = str(kwargs.get("user_id", ""))
        self.__account_no = str(kwargs.get("account_no", ""))
        self.__msisdn = str(kwargs.get("msisdn", ""))

        if not isinstance(self.__cx_channel, CxChannels):
            logger.info(f"{self.__clsname} cx_channel provided is not a CxChannels type.")
            return False

        if self.__cx_channel == CxChannels.FACEBOOK:
            self.__fb_identity_key = str(kwargs.get("identity_key", ""))
            if not "identity_key" in kwargs:
                logger.info(f"{self.__clsname} identity_key is required.")
                return False

        if str_utils.is_none_or_empty_str(self.__channel_id):
            logger.info(f"{self.__clsname} channel_id is required.")
            return False

        if str_utils.is_none_or_empty_str(self.__user_id):
            logger.info(f"{self.__clsname} user_id is required.")
            return False

        if str_utils.is_none_or_empty_str(self.__account_no) and str_utils.is_none_or_empty_str(self.__msisdn):
            logger.info(f"{self.__clsname} Either of account_no or msisdn is required.")
            return False
            
        return True

    
    def __get_rec_by_account_no(self) -> dict:
        self.__ddb_xchannel_matching = self.__get_ddb_xchannel_matching_instance()
        filter_exp = {
            "attribute": tableattributes.USER_ID,
            "condition": "eq",
            "value": self.__user_id
        }

        xchannel_matching_res = self.__ddb_xchannel_matching.get_item_by_index(
                tableattributes.ACCOUNT_NO,
                self.__account_no,
                tableattributes.ACCOUNT_NO_INDEX,
                filter_expression=filter_exp)

        result_count = len(xchannel_matching_res)

        if result_count == 0:
            return {}

        for item in xchannel_matching_res:
            if self.__msisdn:
                if item.get(tableattributes.MSISDN, "").strip() == self.__msisdn:
                    return item
            else:
                if not item.get(tableattributes.MSISDN, "").strip():
                    return item
        
        return {}
                

    def __get_rec_by_msisdn(self) -> dict:
        self.__ddb_xchannel_matching = self.__get_ddb_xchannel_matching_instance()
        filter_exp = {
            "attribute": tableattributes.USER_ID,
            "condition": "eq",
            "value": self.__user_id
        }

        xchannel_matching_res = self.__ddb_xchannel_matching.get_item_by_index(
                tableattributes.MSISDN,
                self.__msisdn,
                tableattributes.MSISDN_INDEX,
                filter_expression=filter_exp)

        result_count = len(xchannel_matching_res)

        if result_count == 0:
            return {}

        for item in xchannel_matching_res:
            if self.__account_no:
                if item.get(tableattributes.ACCOUNT_NO, "").strip() == self.__account_no:
                    return item
            else:
                if not item.get(tableattributes.ACCOUNT_NO, "").strip():
                    return item
        
        return {}


    def __get_ddb_xchannel_matching_instance(self) -> DDBTools:
        if not self.__ddb_xchannel_matching:
            self.__ddb_xchannel_matching = DDBTools(configs.DDB_SUBSCRIBER_CROSS_CHANNEL_MATCHING, configs.REGION_OREGON)

        return self.__ddb_xchannel_matching