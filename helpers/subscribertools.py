# NIAS 2.0 - HISAMS
import json
import boto3
import logging

from configuration import REGION_SYDNEY
from helpers.utils import get_exception_str
from resources.aws_lambda import MAIN_CONNECT_LAMBDA
from resources.constants import PLATINUM_BB_LOB_NAME, BB_LOB_NAME,SHP_LOB_NAME, IN_HOUSE_LOB_NAME, PREPAID_LOB_NAME

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class SubscriberTools:

    def __init__(self, subs_context, subs_context_id, additional_attributes = None):

        if not self.__is_valid_input(subs_context, subs_context_id, additional_attributes):
            raise ValueError(self.__error)

        self.__subs_context = subs_context.upper()
        self.__subs_context_id = subs_context_id
        self.__additional_attributes = additional_attributes
        self.__get_data_from_connect()


    def __is_valid_input(self, context, value, additional_attribute):
        if context is None or not context.strip() or context.upper() not in ["MSISDN", "ACCOUNTNUMBER"]:
            self.__error = "Invalid search type"
            return False
        elif value is None or not value.strip():
            self.__error = "Invalid search value"
            return False
        if additional_attribute != None:
            if not type(additional_attribute) is dict and len(additional_attribute.keys()) == 0:
                self.__error =  "Invalid attributes"
                return False
        return True

    
    def __build_connect_payload(self):
        payload = {
            "Details": {
                "ContactData": {
                    "Attributes": {},
                    "CustomerEndpoint": {
                        "Address": "+63XXXXXXXXXX"
                    }
                },
                "Parameters": {}
            }
        }

        if self.__additional_attributes != None:
            payload['Details']['ContactData']['Attributes'] = self.__additional_attributes
        if self.__subs_context == "MSISDN":
            payload['Details']['ContactData']['Attributes']['concernedNumber'] = self.__subs_context_id
        else:
            payload['Details']['ContactData']['Attributes']['concernedAccountNumber'] = self.__subs_context_id
        
        return payload
        
                
    def __get_data_from_connect(self):
        connect_req_payload = self.__build_connect_payload()
        lmbd_clnt_sydney = boto3.client("lambda", region_name = REGION_SYDNEY)

        try:
            connect_response = lmbd_clnt_sydney.invoke(FunctionName = MAIN_CONNECT_LAMBDA, InvocationType = "RequestResponse", Payload = json.dumps(connect_req_payload))
            connect_response = json.loads(connect_response['Payload'].read().decode())
        except Exception as error:
            logger.info(f"Error calling {MAIN_CONNECT_LAMBDA}: {get_exception_str(error)}")
            connect_response = None

        logger.info(f"ConnectMain paylod: {connect_req_payload}")
        logger.info(f"ConenctMain response: {connect_response}")

        if connect_response is None:
            self.__is_subscriber_exists = False
            self.__set_non_existing_attrs()
            return
        
        self.__is_subscriber_exists = True
        self.__lob_name = connect_response['lobName'] if 'lobName' in connect_response and connect_response['lobName'].strip() else ""
        self.__msisdn = connect_response['mSISDN'] if 'mSISDN' in connect_response and connect_response['mSISDN'].strip() else ""
        self.__account_no = connect_response['accountNumber'] if 'accountNumber' in connect_response and connect_response['accountNumber'].strip() else ""
        self.__first_name = connect_response['firstName'].strip() if 'firstName' in connect_response and connect_response['firstName'].strip() else ""
        self.__birth_date = connect_response['dateOfBirth'] if 'dateOfBirth' in connect_response and connect_response['dateOfBirth'].strip() else ""
        self.__bss_contact_id = connect_response['bssContactId'] if 'bssContactId' in connect_response and connect_response['bssContactId'].strip() else ""
        self.__landline = connect_response['landline'] if 'landline' in connect_response and connect_response['landline'].strip() else ""
        self.__brand = connect_response['brand'] if 'brand' in connect_response and connect_response['brand'].strip() else ""
        self.__lob_number = connect_response['lob'] if 'lob' in connect_response and connect_response['lob'].strip() else ""
        self.__amax_user_status = connect_response['amaxUserStatus'] if 'amaxUserStatus' in connect_response and connect_response['amaxUserStatus'].strip() else ""
        self.__sg_lob = connect_response['sgLob'] if 'sgLob' in connect_response and connect_response['sgLob'].strip() else ""
        self.__tenure = connect_response['isTenure'] if 'isTenure' in connect_response and connect_response['isTenure'].strip() else ""
        self.__activation_date = connect_response['activationDate'] if 'activationDate' in connect_response and connect_response['activationDate'] else 0
        self.__bill_cycle = connect_response['billCycle'] if 'billCycle' in connect_response and connect_response['billCycle'].strip() else "0"
        self.__is_senior = connect_response['isSenior'] if 'isSenior' in connect_response and connect_response['isSenior'] else "false"
        self.__delete_indicator = connect_response['deleteInd'] if 'deleteInd' in connect_response and connect_response['deleteInd'] else "0"
        self.__is_new_cust = connect_response['isNewCustomer'] if 'isNewCustomer' in connect_response and connect_response['isNewCustomer'] else ""
        self.__days_tenured = connect_response['daysTenured'] if 'daysTenured' in connect_response and connect_response['daysTenured'] else ""
        self.__customer_type = connect_response['customerType'] if 'customerType' in connect_response and connect_response['customerType'].strip() else "" #customertype

    def __set_non_existing_attrs(self):
        self.__lob_name = None
        self.__msisdn = None
        self.__account_no = None
        self.__first_name = None
        self.__birth_date = None
        self.__landline = None
        self.__bss_contact_id = None
        self.__brand = None
        self.__lob_number = None
        self.__amax_user_status = None
        self.__sg_lob = None
        self.__tenure =None
        self.__activation_date = None
        self.__bill_cycle = None
        self.__is_senior = None
        self.__delete_indicator = None
        self.__is_new_cust = None
        self.__days_tenured = None
        self.__customer_type = None


    def get_lob_name(self):
        if self.__lob_name == PLATINUM_BB_LOB_NAME:
            logger.info("Platinum Brodband Detected, treating as Regular Broadband")
            self.__lob_name = BB_LOB_NAME
        elif self.__lob_name == SHP_LOB_NAME:
            logger.info("SHP Detected, treating as Regular Broadband")
            self.__lob_name = BB_LOB_NAME
        elif self.__lob_name == IN_HOUSE_LOB_NAME:
            logger.info("InHouse Detected, treating as Prepaid")
            self.__lob_name = PREPAID_LOB_NAME
        return self.__lob_name
    
    def get_lob_number(self):
        return self.__lob_number

    def get_msisdn(self):
        return self.__msisdn


    def get_account_no(self):
        return self.__account_no


    def get_first_name(self):
        return self.__first_name


    def get_birth_date(self):
        return self.__birth_date

    
    def is_subscriber_exists(self):
        return self.__is_subscriber_exists

    def get_bss_contact_id(self):
        return self.__bss_contact_id
    
    def get_landline(self):
        return self.__landline
    
    def get_brand(self):
        return self.__brand

    def get_amax_user_status(self):
        return self.__amax_user_status

    def get_sg_lob(self):
        return self.__sg_lob

    def get_tenure(self):
        return self.__tenure

    def get_activation_date(self):
        return str(self.__activation_date)

    def get_bill_cycle(self):
        return self.__bill_cycle

    def is_senior(self):
        return self.__is_senior.lower() if self.__is_senior else self.__is_senior

    def get_delete_indicator(self):
        return self.__delete_indicator.lower() if self.__delete_indicator else self.__delete_indicator

    def is_new_cust(self):
        return self.__is_new_cust.lower() if self.__is_new_cust else self.__is_new_cust
    
    def get_days_tenured(self):
		    return self.__days_tenured
    
    def get_customer_type(self):
		    return self.__customer_type