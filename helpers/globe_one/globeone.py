import logging
import time 
import boto3
import copy
import json

import configuration as configs

from helpers.resFormatter import ResFormatter
from helpers.sessiontools import SessionTools
from helpers.subscribertools import SubscriberTools
from helpers.ddbtools import DDBTools
from helpers.opt_in.optin import Optin 

import helpers.utils as utils
import resources.aws_lambda as lmb_functions
import resources.spiels as spiels
import resources.constants as constants

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class GlobeOne:

    def __init__(self, request=None, **kwargs):
        self.__is_globe_one_flow_executed = False
        self.__is_valid_data_to_process = True
            
        if not request:
            self.__is_valid_data_to_process = False
            logger.info(f"globe_one -> Request is required: {request}")
            
        self.__request = request
        self.__page_id = request['channel']
        self.__sender_id = request['fbId']
        self.__last_intent = request['lastIntent']
        self.__msisdn = kwargs.get("lastNumber", "")

        self.__res_formatter = ResFormatter(self.__page_id)
        self.__globe_one_db = DDBTools(configs.DDB_GLOBE_ONE_DETAILS, configs.REGION_OREGON)
        self.__lambda_sg = boto3.client("lambda", region_name = configs.REGION_SINGAPORE)
        self.opt_in = Optin(self.__sender_id, self.__page_id)
        
    def __is_valid_data(self, **kwargs):
        msisdn = kwargs.get("lastNumber", "")
        if not msisdn or msisdn.strip().lower() in ["string",""]:
            logger.info(f"msisdn is required: {msisdn}")
            return False
        return True  

    def globe_one_details_from_db(self, msisdn):
        globe_one_details = {
            "is_present" : False,
            "is_globe_one_user" : False,
            "is_active_last_30_days" : False
        }
        globe_one_db = DDBTools(configs.DDB_GLOBE_ONE_DETAILS, configs.REGION_OREGON)
        result = globe_one_db.get_item('msisdn', msisdn.strip())

        if result:
            logger.info(f"is_globe_one_details_present -> true : {result}")
            globe_one_details["is_present"] = True
            if result[0]["superapp_user_indicator"] == "true":
                globe_one_details["is_globe_one_user"] = True
                if result[0]["superapp_mau_indicator"] == "true":
                    globe_one_details["is_active_last_30_days"] = True
        
        return globe_one_details
    
    def globe_one_details_from_api(self, msisdn):

        globe_one_details = {
            "is_globe_one_user" : False,
            "is_active_last_30_days" : False
        }

        globe_one_db_params = {
            "msisdn" : self.__msisdn,
            "superapp_user_indicator" : "false",
            "superapp_mau_indicator" : "false",
            "expiry_timestamp" : utils.modify_epoch_time("ADD", "DAYS", 15,  utils.get_current_epoch_time())
        }

        get_details_by_attributes_req = copy.deepcopy(constants.CONNECT_LMB_REQUEST)
        get_details_by_attributes_req["Details"]["ContactData"]["Attributes"].update({
                    "concernedNumber": self.__msisdn
                })
        get_details_by_attributes_req["Details"]["Parameters"].update({
                    "G1Flag": "true",
                    "Attributes": ["msisdn","suind","smind"]
                })

        try:
            logger.info(f" Request[{lmb_functions.GET_DETAILS_BY_ATTRIBUTES_LAMBDA}]: {get_details_by_attributes_req}")
            get_details_by_attributes_res = self.__lambda_sg.invoke(FunctionName = lmb_functions.GET_DETAILS_BY_ATTRIBUTES_LAMBDA, InvocationType = "RequestResponse", Payload = json.dumps(get_details_by_attributes_req))
            get_details_by_attributes_res = json.loads(get_details_by_attributes_res['Payload'].read().decode())
            logger.info(f" Response[{lmb_functions.GET_DETAILS_BY_ATTRIBUTES_LAMBDA}]: {get_details_by_attributes_res}")
        except Exception as err:
            logger.info(f"Error invoking {lmb_functions.GET_DETAILS_BY_ATTRIBUTES_LAMBDA}: {utils.get_exception_str(err)}")
            self.__is_globe_one_flow_executed = False
            logger.info("Customer not enrolled in GlobeOne")

        if "suind" in get_details_by_attributes_res and get_details_by_attributes_res["suind"] == "true":
            globe_one_db_params["superapp_user_indicator"] = "true"
            globe_one_details["is_globe_one_user"] = True

            if get_details_by_attributes_res["smind"] == "true":
                globe_one_db_params["superapp_mau_indicator"] = "true"
                globe_one_details["is_active_last_30_days"] = True
            
        try:
            logger.info(f"globe_one_details-> entry : {globe_one_db_params}")
            self.__globe_one_db.put_item(globe_one_db_params)
        except Exception as error:
            logger.info(f"Error inserting globe_one_details: {utils.get_exception_str(error)}")

        return globe_one_details
                
    def is_globe_one_flow_executed(self):
        if self.__is_globe_one_flow_executed:
            return True
        return False        
            
    def execute_globe_one_flow(self):
        
        if not self.__is_valid_data_to_process:
            logger.info("globe_one -> invalid data.. unable to execute globe one flow")
            return 
        
        if self.__last_intent not in [constants.LOAD_PROMOS_AND_REWARDS_INTENT, constants.BUY_LOAD_OR_PROMO_INTENT, constants.CHECK_APPLICATION_INTENT, constants.FOLLOWUP_CONCERN_INTENT]:
            globe_one_details = self.globe_one_details_from_db(self.__msisdn)

            if globe_one_details["is_present"]:
                if globe_one_details["is_globe_one_user"]:
                    if globe_one_details["is_active_last_30_days"]:
                        # self.__res_formatter.send_message(self.__sender_id, spiels.G1_ENROLLED_WITHIN_30DAYS_SPIEL)
                        if self.__page_id == configs.GT_PAGE_ID:
                            self.opt_in.execute_optin_flow(spiels.G1_ENROLLED_OPTIN_SPIEL, "WEEKLY")
                    else:
                        # self.__res_formatter.send_message(self.__sender_id, spiels.G1_ENROLLED_BEYOND_30DAYS_SPIEL)
                        if self.__page_id == configs.GT_PAGE_ID:
                            self.opt_in.execute_optin_flow(spiels.G1_ENROLLED_OPTIN_SPIEL, "WEEKLY")
                else:
                    # self.__res_formatter.send_message(self.__sender_id, spiels.G1_NOT_ENROLLED_SPIEL)
                    if self.__page_id == configs.GT_PAGE_ID:
                            self.opt_in.execute_optin_flow(spiels.G1_NOT_ENROLLED_OPTIN_SPIEL, "WEEKLY")
                
                logger.info(f"globe_one_details->: {globe_one_details}")
                self.__is_globe_one_flow_executed = True
                return
            else:
                logger.info(f"globe_one_details_db-> msisdn({self.__msisdn}): false")
                if self.__msisdn.strip().lower() not in ["string",""]:
                    globe_one_details = self.globe_one_details_from_api(self.__msisdn)

                    if globe_one_details["is_globe_one_user"]:
                        if globe_one_details["is_active_last_30_days"]:
                            # self.__res_formatter.send_message(self.__sender_id, spiels.G1_ENROLLED_WITHIN_30DAYS_SPIEL)
                            if self.__page_id == configs.GT_PAGE_ID:
                                self.opt_in.execute_optin_flow(spiels.G1_ENROLLED_OPTIN_SPIEL, "WEEKLY")
                        else:
                            # self.__res_formatter.send_message(self.__sender_id, spiels.G1_ENROLLED_BEYOND_30DAYS_SPIEL)
                            if self.__page_id == configs.GT_PAGE_ID:
                                self.opt_in.execute_optin_flow(spiels.G1_ENROLLED_OPTIN_SPIEL, "WEEKLY")
                    else:
                        # self.__res_formatter.send_message(self.__sender_id, spiels.G1_NOT_ENROLLED_SPIEL)
                        if self.__page_id == configs.GT_PAGE_ID:
                            self.opt_in.execute_optin_flow(spiels.G1_NOT_ENROLLED_OPTIN_SPIEL, "WEEKLY")
                    
                    logger.info(f"globe_one_details->: {globe_one_details}")
                    self.__is_globe_one_flow_executed = True
                    return

                else:
                    # self.__res_formatter.send_message(self.__sender_id, spiels.G1_NOT_ENROLLED_SPIEL)
                    self.__is_globe_one_flow_executed = True
                    return
        else:
            self.__is_globe_one_flow_executed = False
            logger.info(f"globe_one-> |{self.__last_intent}| is not eligible for GlobeOne")
            return          
       