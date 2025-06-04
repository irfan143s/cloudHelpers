# NIAS 2.0 - HISAMS
from helpers.utils import get_current_time

from helpers.resFormatter import ResFormatter
from helpers.ddbtools import DDBTools

from configuration import *
from resources.aws_lambda import *
from resources.constants import *
from resources.spiels import *
from resources.resourcemapping import *

class DataPrivacyNotice:

    __DPN_STATES = ['0', '1']

    def __init__(self, sender_id, page_id):
        self.__sender_id = sender_id
        self.__response_formatter = ResFormatter(page_id)
        self.__ddb_client_main = DDBTools(page_ddb_mapping_dict[page_id]['main'], REGION_OREGON)
        self.__init_main_data()


    def __init_main_data(self):
        data = self.__ddb_client_main.get_item("fbId", self.__sender_id)[0]
        
        if self.__is_dpn_attr_exists(data):
            self.__state = data['dpnState']
        else:
            self.__state = '0'

        if self.__is_last_accpted_attr_exists(data):
            self.__is_dpn_accepted = True
        else:
            self.__is_dpn_accepted = False


    def __is_dpn_attr_exists(self, data):
        if 'dpnState' in data and data['dpnState'].strip() and data['dpnState'].strip() in self.__DPN_STATES:
            return True
        return False


    def __is_last_accpted_attr_exists(self, data):
        if 'lastDpnAcceptedTimestamp' in data and data['lastDpnAcceptedTimestamp'].strip():
            return True
        return False

    
    def __update_state(self, state):
        item = { 
            'dpnState': state 
        }
        self.__ddb_client_main.update_item('fbId', self.__sender_id, item)


    def __reset_data(self):
        self.__ddb_client_main.delete_item_attribute('fbId', self.__sender_id, 'dpnState')
        

    # Use this method if you want to save the DPN details
    def __save_datails(self):
        item = { 
            'lastDpnAcceptedTimestamp': get_current_time() 
        }
        self.__ddb_client_main.update_item('fbId', self.__sender_id, item)



    # *******************************************************************************************************************************
    # ********************************************** Public methods *****************************************************************
    # *******************************************************************************************************************************

    def is_accepted(self):
        return self.__is_dpn_accepted


    def get_state(self):
        return self.__state

    
    def reset_session_data(self):
        self.__reset_data()

    
    def send_dpn(self, spiel=None):
        dpn_spiel = spiel if spiel else DPN_SPIEL

        self.__update_state('1')
        self.__response_formatter.send_quickresponse(self.__sender_id, dpn_spiel, YES_NO_MENU, MENU_FORM)

    
    def accept(self, spiel=None):
        dpn_yes_spiel = spiel if spiel else DPN_ACCEPTED_SPIEL

        if self.__state != '1':
            raise ValueError('You cannot accept a DPN with state not equals to 1')
        
        self.__response_formatter.send_message(self.__sender_id, dpn_yes_spiel)
        self.__state = '11'
        self.__save_datails()
        self.__reset_data()

    
    def reject(self, spiel=None):
        dpn_no_spiel = spiel if spiel else DPN_REJECTED_SPIEL

        if self.__state != '1':
            raise ValueError('You cannot reject a DPN with state not equals to 1')

        self.__response_formatter.send_message(self.__sender_id, dpn_no_spiel)
        self.__state = '00'
        self.__reset_data()