# NIAS 2.0 - HISAMS
import logging              

import resources.cj as cj
import helpers.utils as utils

from helpers.ddbtools import DDBTools
from helpers.sessiontools import SessionTools

from configuration import REGION_OREGON, DDB_CUSTOMER_JOURNEY

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class CustomerJourney:
    
    def __init__(self, sender_id, page_id):
        self.__sender_id = sender_id
        self.__page_id = page_id
        self.__ddb_cj = DDBTools(DDB_CUSTOMER_JOURNEY, REGION_OREGON)
        self.__session_tools = SessionTools(sender_id, page_id)
        self.__session_id = self.__session_tools.get_session_id()
        self.__cj_data = {}
        self.__is_cj_session_exists = False
        self.__init_cj_data()

    
    def __init_cj_data(self):
        tmp_items = self.__ddb_cj.get_item('sessionId', self.__session_id)
        tmp_items = tmp_items if tmp_items else []
        
        if len(tmp_items) > 0:
            self.__is_cj_session_exists = True
            self.__cj_data = tmp_items[0]
        else:
            self.__is_cj_session_exists = False
        
        logger.info(f"__init_cj_data(): {tmp_items}")


    def __create_new_cj_session(self, journey_id):
        self.__cj_data['journeySequence'] = journey_id
        self.__cj_data['concernedNumber'] = None
        tmp_new_cj_session_data = {
            'sessionId': self.__session_id,
            'fbId': self.__sender_id,
            'channel': self.__page_id,
            'qryIdx': 'QI',
            'createTimeStamp': utils.get_current_time(),
            'updateTimestamp': utils.get_current_time(),
            'journeySequence': str(journey_id),
            'concernedNumber': " "
        }

        logger.info(f"Creating CJ entry: {tmp_new_cj_session_data}")

        try:
            self.__ddb_cj.put_item(tmp_new_cj_session_data)
        except Exception as error:
            logger.info(f"Error creating new customer journey data: {utils.get_exception_str(error)}")


    def __get_appended_journey(self, journey_id=""):
        self.__cj_data['journeySequence'] = self.__cj_data['journeySequence'] + ';' + journey_id
        return self.__cj_data['journeySequence']

    def __get_appended_concerned_number(self, number=""):
        if self.__cj_data['concernedNumber'] != " ":
            self.__cj_data['concernedNumber'] = self.__cj_data['concernedNumber'] + ';' + number
        else:
            self.__cj_data['concernedNumber'] = number
        return self.__cj_data['concernedNumber']

    def append_journey(self, journey_id):
        if self.__is_cj_session_exists and self.__session_id:
            tmp_update_item = {
                'journeySequence': self.__get_appended_journey(journey_id),
                'updateTimestamp': utils.get_current_time()
            }

            if self.__cj_concerned_number:
                tmp_update_item['concernedNumber'] = self.__get_appended_concerned_number(self.__cj_concerned_number)
            
            try:
                self.__ddb_cj.update_item('sessionId', self.__session_id, tmp_update_item)
            except Exception as error:
                logger.info(f"Error updating customer journey data: {utils.get_exception_str(error)}")                
        else:
            self.__create_new_cj_session(journey_id)


    def get_journey_id(self, **kwargs):
        logger.info(f"get_journey_id() <- {kwargs}")

        flow = kwargs.get('flow', cj.CJ_NO_FLOW)
        brand = kwargs.get('brand', cj.CJ_NO_BRAND)
        self.__cj_concerned_number = kwargs.get('concerned_number', None)


        # if not flow or flow not in cj.customer_journey_flow_codes:
        #     flow = cj.CJ_NO_FLOW
        #     logger.info(f"flow: {flow} does not exists in cj configurations.")
        
        if not brand or brand not in cj.customer_journey_brand_codes:
            brand = cj.CJ_NO_BRAND
            logger.info(f"brand: {brand} does not exists in cj configurations.")
            
        page_code = cj.customer_journey_page_codes[self.__page_id]
        brand_code = cj.customer_journey_brand_codes[brand]
        
        if flow in cj.customer_journey_flow_codes:
            flow_code = cj.customer_journey_flow_codes[flow]
            return brand_code + "_" + flow_code
        return brand_code + "_" + flow