# NIAS 2.0 - HISAMS
import logging

from helpers.ddbtools import DDBTools
from helpers.facebooktools import FacebookTools
from helpers.utils import *

from configuration import *

from resources.resourcemapping import page_ddb_mapping_dict, page_name_mapping_dict, single_identity_db_mapping_dict
from resources.constants import session_status_list, SESSION_STATUS_ACTIVE, SESSION_STATUS_TICKET_CLOSURE
from resources.states import MAIN_MENU_STATE

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SessionTools:

    def __init__(self, sender_id, page_id):
        self.__sender_id = sender_id
        self.__page_id = page_id
        self.__ddb_identity = DDBTools(DDB_FACEBOOK_USER_IDENTITY, REGION_OREGON)
        self.__ddb_session = DDBTools(page_ddb_mapping_dict[page_id]['session'], REGION_OREGON)
        self.__ddb_main = DDBTools(page_ddb_mapping_dict[page_id]['main'], REGION_OREGON)
        self.__ddb_history = DDBTools(page_ddb_mapping_dict[page_id]['history'], REGION_OREGON)

        self.__main_data = {}
        self.__new_data = {}
        self.__session_id = ''
        self.__session_status = ''

        self.__get_session_data()
        self.__get_session_state_info()


    def update_status(self, status=SESSION_STATUS_ACTIVE, **kwargs):
        status = status.strip().upper()
        item = {}
        session_id = kwargs.get('session_id', '')

        if status not in session_status_list:
            raise ValueError("Invalid session status provided")

        if  not self.get_session_id():
            if not session_id:
                self.__session_id = generate_random_id()
                item['sessionId'] =  self.__session_id
            else:
                self.__session_id = session_id

        item['fbId'] = self.__sender_id
        item['pageId'] = self.__page_id
        item['status'] = status
        item['expiryTimestamp'] = modify_epoch_time("add", "minutes", TIME_SESSION_END,  get_current_epoch_time())
        item['updateTimestamp'] = get_current_time()
        item['sessionId'] = self.__session_id

        return self.__ddb_session.put_item(item)


    def __copy_main_data_to_history(self):
        main_data_result = self.__ddb_main.get_item("fbId", self.__sender_id)
        main_table_data = main_data_result[0]
        # main_table_data['histId'] = generate_random_id()
        main_table_data['histId'] = self.get_session_id()
        main_table_data['qryIdx'] = "QI"
        main_table_data['createTimestamp'] = get_current_time()
        main_table_data['sessionId'] = self.get_session_id()

        # save last session id
        self.__ddb_main.update_item('fbId',  self.__sender_id, {'lastSessionId': self.get_session_id()})
        return self.__ddb_history.put_item(main_table_data)


    def __delete_session(self):
        key = {}
        key['fbId'] = self.__sender_id

        return self.__ddb_session.delete_item(key)


    def create_session_data(self, sender_id, page_id):
        try:
            fb_tools = FacebookTools()
            fb_name = fb_tools.get_name(page_id, sender_id)['first_name']
        except Exception as error:
            fb_name = " "
        self.__new_data['newUserDate'] = str(get_current_datetime_without_marker())
        self.__new_data = {}
        self.__new_data['fbId'] = sender_id
        self.__new_data['fbName'] = fb_name
        self.__new_data['channel'] = page_id
        self.__new_data['sessionState'] = MAIN_MENU_STATE
        self.__new_data['advisoryPriority'] = "0"
        self.__new_data['subState'] = "0"
        self.__new_data['retry'] = "0"
        self.__new_data['unrecognizedRetry'] = "0"
        self.__new_data['userInput'] = {}
        self.__new_data['lastAccountNumber'] = "String"
        self.__new_data['lastLandline'] = "String"
        self.__new_data['lastFirstName'] = "String"
        self.__new_data['lastSubsBrand'] = "String"
        self.__new_data['lastLobNumber'] = "String"
        self.__new_data['lastSgBrand'] = "String"
        self.__new_data['lastBrand'] = "String"
        self.__new_data['lastNumber'] = "String"
        self.__new_data['lastIntent'] = "String"
        self.__new_data['lastIntentDate'] = "String"
        self.__new_data['lastMenuId'] = "String"
        self.__new_data['lobName'] = "String"
        self.__new_data['isGreeted'] = "false"
        self.__new_data['lastBssContactId'] = "String"
        self.__new_data['lastTenure'] = "String"
        self.__new_data['lastActivationDate'] = "String"
        self.__new_data['lastMsisdn'] = "String"
        self.__new_data['lastCustomerType'] = "String"
        self.__new_data['advisories'] = "String"
        self.__new_data['lockedFlow'] = ""
        self.__new_data['caseType'] = "String"
        self.__new_data['caseCreationStatus'] = "String"
        self.__new_data['isPrivateReplyActive'] = "false"
        self.__new_data['globalRetryCount'] = "0"
        self.__new_data['sessionContextAttributes'] = {}
        self.__new_data['brandType'] = "String"
        
        try:
            self.__ddb_main.put_item(self.__new_data)
            self.__main_data = self.__new_data
            return self.__new_data
        except Exception as error:
            logger.info(f"Error creating session data: {get_exception_str(error)}")


    def reset_state(self, **kwargs):
        item = {}
        reset_except = kwargs.get('reset_except', [])
        if 'globalRetryCount' not in reset_except:
            item['globalRetryCount'] = "0"

        item['sessionState'] = MAIN_MENU_STATE
        item['subState'] = "0"
        item['advisoryPriority'] = "0"
        item['retry'] = "0"
        item['unrecognizedRetry'] = "0"
        item['userInput'] = {}
        item['lastAccountNumber'] = "String"
        item['lastLandline'] = "String"
        item['lastFirstName'] = "String"
        item['lastSubsBrand'] = "String"
        item['lastLobNumber'] = "String"
        item['lastBrand'] = "String"
        item['lastNumber'] = "String"
        item['lastSgBrand'] = "String"
        item['lastIntent'] = "String"
        item['lastMenuId'] = "String"
        item['lobName'] = "String"
        item['dpnState'] = "0"
        item['lastBssContactId'] = "String"
        item['lastTenure'] = "String"
        item['lastActivationDate'] = "String"
        item['lastMsisdn'] = "String"
        item['advisories'] = "String"
        item['transactionStartDate'] = "String"
        item['lockedFlow'] = ""
        item['caseType'] = "String"
        item['caseCreationStatus'] = "String"
        item['isSenior'] = "false"
        item['sessionContext'] = ""
        item['sessionContextAttributes'] = {}
        item['brandType'] = "String"
        item['lastCustomerType'] = "String"

        try:
            return self.__ddb_main.update_item("fbId", self.__sender_id, item)
        except Exception as error:
            logger.info(f"Error resetting state: {get_exception_str(error)}")


    def reset_session(self):
        try:
            self.__ddb_session.delete_item_attribute("fbId", self.__sender_id, "expiryTimestamp")
            self.__delete_session()
        except Exception as error:
            logger.info(f"Error resetting session: {get_exception_str(error)}")
           
            
    def reset_private_reply(self):
        try:
            if 'identityKey' in self.__main_data:
                identity_key = self.__main_data['identityKey']
                response_identity = self.__ddb_identity.get_item('identityKey', identity_key)
                
                if len(response_identity)  > 0:        
                    for k, sender_id_identity in response_identity[0].items():
                        if k in single_identity_db_mapping_dict:

                            table_name_identity = page_ddb_mapping_dict[single_identity_db_mapping_dict[k]]['main']
                            if table_name_identity != DDB_THEA_MAIN:
                                logger.info(f"Private Reply Reset: table_name_identity: {table_name_identity}, fbId: {sender_id_identity}")
                                ddb_identity = DDBTools(table_name_identity, REGION_OREGON)
                                ddb_identity.update_item_if_primary_key_exist("fbId", sender_id_identity, {'isPrivateReplyActive': "false"})
                else:
                    logger.info("Private Reply Reset: no identity key detected in identity table")
            else:
                logger.info("Private Reply Reset: no identity key detected in main data")  
                                          
        except Exception as error:
            logger.info(f"Error resetting private reply on all pages: {get_exception_str(error)}")


    def reset_state_and_session(self, is_full_reset=True):
        try:
            self.__reset_is_greeted()
            self.__copy_main_data_to_history()
            self.reset_state()
            self.reset_private_reply()
            self.reset_session_context_attributes()
            if is_full_reset:
                self.reset_session()

        except Exception as error:
            logger.info(f"Error resetting state and session: {get_exception_str(error)}")


    # this should be used incase multiple attributes update to lessen the write request
    def update_attributes(self, items):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, items)

            for k, v in items.items():
                self.__main_data[k] = v

        except Exception as error:
            logger.info(f"Error updating attributes: {get_exception_str(error)}")


    def update_state(self, state):
        try:
            if state == self.__main_data.get("sessionState", ""):
                return
            
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'sessionState': state})
            self.__main_data['sessionState'] = state
        except Exception as error:
            logger.info(f"Error updating sessionState: {get_exception_str(error)}")


    def update_sub_state(self, sub_state):
        try:
            if sub_state == self.__main_data.get("subState", ""):
                return
            
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'subState': sub_state})
            self.__main_data['subState'] = sub_state
        except Exception as error:
            logger.info(f"Error updating subState: {get_exception_str(error)}")


    def update_session_context(self, session_context):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'sessionContext': session_context})
            self.__main_data['sessionContext'] = session_context
        except Exception as error:
            logger.info(f"Error updating sessionContext: {get_exception_str(error)}")

    
    def update_last_number(self, number):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'lastNumber': number})
            self.__main_data['lastNumber'] = number
        except Exception as error:
            logger.info(f"Error updating lastNumber: {get_exception_str(error)}")


    def update_last_sg_brand(self, lob):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'lastSgBrand': lob})
            self.__main_data['lastSgBrand'] = lob
        except Exception as error:
            logger.info(f"Error updating lastSgBrand: {get_exception_str(error)}")


    def update_last_brand(self, lob):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'lastBrand': lob})
            self.__main_data['lastBrand'] = lob
        except Exception as error:
            logger.info(f"Error updating lastBrand: {get_exception_str(error)}")


    def update_case_type(self, case_type):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'caseType': case_type})
            self.__main_data['caseType'] = case_type
        except Exception as error:
            logger.info(f"Error updating caseType: {get_exception_str(error)}")


    def update_last_activation_date(self, activationdate):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'lastActivationDate': activationdate})
            self.__main_data['lastActivationDate'] = activationdate
        except Exception as error:
            logger.info(f"Error updating lastActivationDate: {get_exception_str(error)}")


    def reset_retry(self):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'retry': '0'})
            self.__main_data['retry'] = '0'
        except Exception as error:
            logger.info(f"Error resetting retry: {get_exception_str(error)}")


    def update_retry(self, value):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'retry': str(value)})
            self.__main_data['retry'] = str(value)
        except Exception as error:
            logger.info(f"Error updating retry: {get_exception_str(error)}")

    def update_unrecognized_retry(self, value):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'unrecognizedRetry': str(value)})
            self.__main_data['unrecognizedRetry'] = str(value)
        except Exception as error:
            logger.info(f"Error updating unrecognizedRetry: {get_exception_str(error)}")

    def update_is_greeted(self, value):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'isGreeted': str(value).lower()})
            self.__main_data['isGreeted'] = str(value).lower()
        except Exception as error:
            logger.info(f"Error updating retry: {get_exception_str(error)}")


    def update_last_intent(self, intent):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'lastIntent': intent})
            self.__main_data['lastIntent'] = intent
        except Exception as error:
            logger.info(f"Error updating lastIntent: {get_exception_str(error)}")


    def update_is_persistent_menu_enabled(self, is_persistent_menu_enabled):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'isPersistentMenuEnabled': is_persistent_menu_enabled})
            self.__main_data['isPersistentMenuEnabled'] = is_persistent_menu_enabled
        except Exception as error:
            logger.info(f"Error updating isPersistentMenuEnabled: {get_exception_str(error)}")


    def update_user_input(self, items):
        try:
            self.__ddb_main.update_map('fbId', self.__sender_id, 'userInput', items)

            for k, v in items.items():
                self.__main_data['userInput'][k] = v

        except Exception as error:
            logger.info(f"Error updating userInput: {get_exception_str(error)}")


    def update_session_context_attributes(self, items):
        try:
            if not "sessionContextAttributes" in self.__main_data:
                self.__main_data["sessionContextAttributes"] = {}
                self.__ddb_main.update_item('fbId', self.__sender_id, {'sessionContextAttributes': {}})
            
            self.__ddb_main.update_map('fbId', self.__sender_id, 'sessionContextAttributes', items)

            for k, v in items.items():
                self.__main_data['sessionContextAttributes'][k] = v

        except Exception as error:
            logger.info(f"Error updating sessionContextAttributes: {get_exception_str(error)}")


    def update_locked_flow(self, value):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'lockedFlow':  str(value).lower()})
            self.__main_data['lockedFlow'] =  str(value).lower()
        except Exception as error:
            logger.info(f"Error updating lockedFlow: {get_exception_str(error)}")


    def update_is_senior(self, value):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'isSenior':  str(value).lower()})
            self.__main_data['isSenior'] =  str(value).lower()
        except Exception as error:
            logger.info(f"Error updating isSenior: {get_exception_str(error)}")


    def __reset_is_greeted(self):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'isGreeted': "false"})
            self.__main_data['isGreeted'] = "false"
        except Exception as error:
            logger.info(f"Error updating isGreeted: {get_exception_str(error)}")


    def update_global_retry_count(self, value):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'globalRetryCount':  str(value).lower()})
            self.__main_data['globalRetryCount'] =  str(value).lower()
        except Exception as error:
            logger.info(f"Error updating globalRetryCount: {get_exception_str(error)}")


    def reset_user_input(self):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'userInput': {}})
            self.__main_data['userInput'] = {}
        except Exception as error:
            logger.info(f"Error resetting userInput: {get_exception_str(error)}")


    def reset_session_context_attributes(self):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'sessionContextAttributes': {}})
            self.__main_data['sessionContextAttributes'] = {}
        except Exception as error:
            logger.info(f"Error resetting sessionContextAttributes: {get_exception_str(error)}")

    def reset_unrecognized_retry(self):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'unrecognizedRetry': '0'})
            self.__main_data['unrecognizedRetry'] = '0'
        except Exception as error:
            logger.info(f"Error resetting unrecognizedRetry: {get_exception_str(error)}")

    def __get_session_data(self):
        try:
            response = self.__ddb_main.get_item('fbId', self.__sender_id)
            if len(response) > 0:
                self.__is_user_exists = True
                self.__main_data = response[0]
                if not self.__main_data.get('newUserDate'):
                    self.__main_data['newUserDate'] = str(get_current_datetime_without_marker())
                    self.__ddb_main.update_item('fbId',  self.__sender_id, {"newUserDate":self.__main_data['newUserDate']})
            else:
                self.__is_user_exists = False

            logger.info(f"__get_session_data: __main_data: {self.__main_data}")
            return self.__main_data
        except Exception as error:
            logger.info(f"Error getting session data: {get_exception_str(error)}")


    def __get_session_state_info(self):
        try:
            tmp_session_state_info = self.__ddb_session.get_item('fbId', self.__sender_id)
            if len(tmp_session_state_info) > 0:
                if 'sessionId' in tmp_session_state_info[0].keys() and tmp_session_state_info[0]['sessionId']:
                    self.__session_id = tmp_session_state_info[0]['sessionId']
                    self.__session_status = tmp_session_state_info[0]['status']
        except Exception as error:
            logger.info(f"Error getting current session info: {get_exception_str(error)}")
    

    # This will return the fresh data from DB
    def get_session_data(self):
        return self.__get_session_data()

    """
        Setting "is_raw" to "True" will get the "sessionId" from DB and not from the current object and update the current state's sessionId.
    """
    def is_new_session(self, is_raw=False):
        if is_raw:
            self.__get_session_state_info()

        if self.get_session_id() and not self.__session_status == SESSION_STATUS_TICKET_CLOSURE:
            return False
        return True


    # ******************************************************************************************************************
    # **************************************** Public SET methods ******************************************************
    # ******************************************************************************************************************
    """ Issue:  When session data is deleted by TTL, session_id of the current state will be empty string "" from get_session_id() since it is querying
                the session table with data that has already been deleted.
                When reset_session_and_state() is invoked, "sessionId" attribute will be an empty string on history table.
        Fix:    Added this method to explicitly add the sessionId from the data stream old_data after TTL is triggered.
    """
    def set_session_id(self, session_id=""):
        self.__session_id = session_id


    def reset_locked_flow(self):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'lockedFlow':  'String'})
            self.__main_data['lockedFlow'] =  'String'
        except Exception as error:
            logger.info(f"Error resetting lockedFlow: {get_exception_str(error)}")


    def reset_session_context(self):
        try:
            self.__ddb_main.update_item('fbId',  self.__sender_id, {'sessionContext':  ''})
            self.__main_data['sessionContext'] =  ''
        except Exception as error:
            logger.info(f"Error resetting sessionContext: {get_exception_str(error)}")


    def reset_is_greeted(self):
        self.__reset_is_greeted()


    # ******************************************************************************************************************
    # **************************************** Public GET methods ******************************************************
    # ******************************************************************************************************************

    def get_last_brand(self):
        return self.__main_data['lastBrand']

    def get_last_sg_brand(self):
        return self.__main_data['lastSgBrand'] if 'lastSgBrand' in self.__main_data else ""

    def get_last_number(self):
        return self.__main_data['lastNumber']

    def get_case_type(self):
        return self.__main_data['caseType']
    
    def get_fb_id(self):
        return self.__sender_id
    
    def get_page_id(self):
        return self.__page_id

    def get_fb_name(self):
        return self.__main_data['fbName']

    def get_state(self):
        return self.__main_data['sessionState']

    def get_sub_state(self):
        return self.__main_data['subState']

    def get_retry(self):
        return self.__main_data.get("retry", "0")
    
    def get_unrecognized_retry(self):
        return self.__main_data['unrecognizedRetry']

    def get_session_context_attributes(self):
        return self.__main_data['sessionContextAttributes'] if 'sessionContextAttributes' in self.__main_data else {}
    
    def get_user_input(self):
        return self.__main_data['userInput']

    def is_greeted(self):
        return self.__main_data['isGreeted']

    def is_user_exists(self):
        return self.__is_user_exists

    def get_last_bss_contact_id(self):
        return self.__main_data.get("lastBssContactId", "")

    def get_last_tenure(self):
        return self.__main_data['lastTenure']

    def get_last_landline(self):
        return self.__main_data['lastLandline']

    def get_last_account_no(self):
        return self.__main_data['lastAccountNumber']

    def get_last_activation_date(self):
        return self.__main_data['lastActivationDate']

    def get_last_msisdn(self):
        return self.__main_data['lastMsisdn']

    def get_advisories(self):
        return self.__main_data['advisories']

    def get_advisory_priority(self):
        return self.__main_data['advisoryPriority']

    def get_new_user_date(self):
        return self.__main_data['newUserDate']

    def get_session_id(self):
        return self.__session_id if self.__session_id.strip() else ""

    def get_identity_key(self):
        return self.__main_data.get("identityKey", "")

    def get_locked_flow(self):
        return self.__main_data.get("lockedFlow", "")

    def get_case_creation_status(self):
        return self.__main_data.get("caseCreationStatus", "")

    def is_senior(self):
        return self.__main_data.get("isSenior", "false")

    def is_private_reply_active(self):
        return self.__main_data.get("isPrivateReplyActive", "false")

    def get_session_context(self):
        return self.__main_data.get("sessionContext", "")
    
    def get_last_intent(self):
        return self.__main_data.get("lastIntent", "")

    def get_last_session_id(self):
        return self.__main_data.get("lastSessionId", "")
    
    def get_otp_referrer(self):
        return self.__main_data.get("otpReferrer", "")
    
    def get_last_first_name(self):
        return self.__main_data.get("lastFirstName", "")
    
    def get_free_thea_registered_number(self):
        return self.__main_data.get("freeTheaRegisteredNumber", "")

    def get_thea_registered_number(self):
        return self.__main_data.get("registeredNumber", "")
    
    def get_global_retry_count(self):
        return int(self.__main_data.get("globalRetryCount", "0"))
    
    def get_brand_type(self):
        return self.__main_data.get("brandType", "")

    def get_session_state(self):
        return self.__main_data.get("sessionState", "")

    def get_last_customer_type(self):
        return self.__main_data.get("lastCustomerType", "").upper()