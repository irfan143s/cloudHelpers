import logging
import time 

import configuration as config

import helpers.utilities.flow as flow_utils
import helpers.utilities.mybsscase as mybsscase_utils
import helpers.whitelistchecker as whitelist_checker

from helpers.autocase import AutoCase
from helpers.agenttools import AgentTools
from helpers.resFormatter import ResFormatter
from helpers.sessiontools import SessionTools

from resources.spiels import *
from resources import resourcemapping 
from resources.constants import *
import resources.api as endpoints

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class StuckOrder:

    def __init__(self, request= None, **kwargs):
        self.__is_stuck_order_flow_executed = False
        self.__is_valid_data_to_process = True
        
        if not self.__is_valid_data(**kwargs):
            self.__is_valid_data_to_process = False
            
        if not request:
            self.__is_valid_data_to_process = False
            logger.info(f"Request is required: {request}")
            
        self.__request = request
        self.__case_tools = AutoCase()
        self.__agent_tools = AgentTools(request['channel'])
        self.__page_id = request['channel']
        self.__sender_id = request['fbId']
        self.__intent = request['lastIntent']
        self.__lastSgBrand = request.get("lastSgBrand", "")
        
        self.__brand = kwargs.get("brand", "")
        self.__landline = kwargs.get("landline", "")
        self.__case_type = kwargs.get("case_type", "stuck-pending-order")
        self.__related_cases_type = kwargs.get("related_cases_type", "stuck-pending-order")
        self.__account_number= kwargs.get("account_number", "")
        
        
        self.__res_formatter = ResFormatter(self.__page_id)
    
    def __end_conversation(self):
        time.sleep(0.5)
        self.__session_tools.reset_state_and_session()
        self.__agent_tools.updateStatus(endpoints.SOCIO_UPDATE_API.format(config.SOCIO_ORG_ID), self.__page_id, self.__sender_id, resourcemapping.socio_profile_id_mapping_dict[self.__page_id], None, "CLOSE")
                   
    def __is_valid_data(self, **kwargs):
        landline = kwargs.get("landline", "")
        if not landline:
            logger.info(f"landline is required: {landline}")
            return False
        return True              
            
    def is_stuck_order_flow_executed(self):
        if self.__is_stuck_order_flow_executed:
            return True
        return False        
            
    def execute_stuck_order_flow(self):
        
        if not self.__is_valid_data_to_process:
            logger.info("Invalid data.. Cannot proceed to stuck order flow")
            return 
        
        self.__session_tools = SessionTools(self.__sender_id, self.__page_id)
        
        if whitelist_checker.is_pending_stuck_order_whitelisted(self.__landline) :
            self.__is_stuck_order_flow_executed = True
            logger.info("Customer have stuck/pending order")
            case_id = mybsscase_utils.get_latest_case_id("", self.__landline, self.__account_number)
            
            if case_id and mybsscase_utils.is_case_id_in_open_case_list(case_id, self.__related_cases_type, self.__brand):
                logger.info("Customer has related stuck order case") 
                self.__res_formatter.send_message(self.__sender_id,STUCK_PENDING_ORDER_EXISTING_CASE_SPIEL)
                self.__end_conversation()
            else:
                lognote = f"Service ID: {self.__landline}\nIntent: {self.__intent.title()}" 
                self.__res_formatter.send_message(self.__sender_id, STUCK_PENDING_ORDER_INTRO_SPIEL)
                create_case = self.__case_tools.auto_case(True, self.__session_tools,self.__case_type,  lognote,False)
                logger.info(f"create case status: {create_case}")
                if create_case: 
                ##change sms to true if prd
                    self.__end_conversation()
                else:
                    if self.__brand == POSTPAID_LOB_NAME:
                        lob = 'postpaid'
                    elif self.__brand in [PREPAID_LOB_NAME, TM_LOB_NAME]:
                        lob = 'prepaid'
                    elif self.__brand == BB_LOB_NAME:
                        lob = 'broadband'
                    elif self.__brand == BUSINESS_SG_LOB_NAME:
                        if self.__lastSgBrand:
                            if self.__lastSgBrand.upper() == "BROADBAND":
                                lob = "business_sg_broadband"
                            else:
                                lob = "business_sg_postpaid"
                        else:
                            lob = 'main'
                    else:
                        lob = 'main'                   
                    intent_id = config.socioBasket[self.__page_id][lob]
                    flow_utils.invoke_transfer_to_agent(self.__request, intent_id, {}, None)
        else:
            self.__is_stuck_order_flow_executed = False
            logger.info("Customer doesn't have stuck/pending order")          
       