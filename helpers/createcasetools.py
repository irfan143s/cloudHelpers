# NIAS 2.0 - HISAMS
import json
import boto3
import logging

from configuration import *

from resources.aws_lambda import PUBLISH_SMS_THROUGH_RAVEN_LAMBDA, CREATE_CASE_LAMBDA

from helpers.utils import get_13_digit_mobile_number, get_exception_str

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class CreateCaseTools:

    __CASE_REQUIRED_ATTRIBUTES = ['subscription', 'title', 'lvl1', 'lvl2', 'lvl3', 'lvl4', 'lvl5', 'queue', 'lob', 'reason','fbid','fbchannel']
    __SMS_REQUIRED_ATTRIBUTES = ['sla', 'receiver']
    __inputted_attributes = []

    def __init__(self):
        # initializing default values
        self.__account_no = "NA"
        self.__sms_message_id = CASE_CREATE_SMS_MESSAGE_ID
        self.__sms_ref_num = "$caseId$"
        self.__is_send_sms = False
        self.__is_created = False
        self._x_sms_parameters = {}
        self.__log_note = ""
        self.__phone_note = ""
        self.__issue_start_date = None


    def set_subscription(self, subscription):
        self.__subscription = get_13_digit_mobile_number(subscription)
        self.__inputted_attributes.append('subscription')

    def set_account_no(self, account_no):
        self.__account_no = account_no if account_no else "NA"
        self.__inputted_attributes.append('account_no')

    def set_title(self, title):
        self.__title = title
        self.__inputted_attributes.append('title')


    def set_lvl1(self, lvl1):
        self.__lvl1 = lvl1
        self.__inputted_attributes.append('lvl1')
        

    def set_lvl2(self, lvl2):
        self.__lvl2 = lvl2
        self.__inputted_attributes.append('lvl2')


    def set_lvl3(self, lvl3):
        self.__lvl3 = lvl3
        self.__inputted_attributes.append('lvl3')


    def set_lvl4(self, lvl4):
        self.__lvl4 = lvl4
        self.__inputted_attributes.append('lvl4')


    def set_lvl5(self, lvl5):
        self.__lvl5 = lvl5
        self.__inputted_attributes.append('lvl5')


    def set_queue(self, queue):
        self.__queue = queue
        self.__inputted_attributes.append('queue')


    def set_log_note(self, log_note, **kwargs):
        session_context_attributes = kwargs.get("sessionContextAttributes", {})
        req_log_notes = session_context_attributes.get("logNotes", "")

        self.__log_note = log_note + req_log_notes
        self.__inputted_attributes.append('lognote')
    

    def set_phone_note(self, phone_note, **kwargs):
        session_context_attributes = kwargs.get("sessionContextAttributes", {})
        req_phone_notes = session_context_attributes.get("logNotes", "")

        self.__phone_note = phone_note + req_phone_notes
        self.__inputted_attributes.append('phonenote')


    def set_lob(self, lob):
        self.__lob = lob
        self.__inputted_attributes.append('lob')


    def set_reason(self, reason):
        self.__reason = reason
        self.__inputted_attributes.append('reason')

    def set_fb_id(self, fb_id):
        self.__fb_id = fb_id
        self.__inputted_attributes.append('fbid')


    def set_fb_channel(self, fb_channel):
        self.__fb_channel = fb_channel
        self.__inputted_attributes.append('fbchannel')


    def set_is_send_sms(self, is_send_sms):
        self.__is_send_sms = is_send_sms
        self.__inputted_attributes.append('subscription')


    def set_sms_case_ref_num(self, ref_num):
        self.__sms_ref_num = ref_num


    def set_sms_message_id(self, message_id):
        self.__sms_message_id = message_id

    def set_x_sms_parameters(self, paramaters):
        self._x_sms_parameters = paramaters


    def set_sms_case_sla(self, case_sla):
        self.__sms_case_sla = case_sla
        self.__inputted_attributes.append('sla')


    def set_sms_receiver(self, sms_receiver):
        self.__sms_receiver = get_13_digit_mobile_number(sms_receiver)
        self.__inputted_attributes.append('receiver')

    def set_subscription_bb(self, subscription):
        self.__subscription = subscription
        self.__inputted_attributes.append('subscription')

    def set_subscription_lpr(self, subscription):
        self.__subscription = subscription
        self.__inputted_attributes.append('subscription')
    
    def set_issue_start_date(self, issue_start_date = None):        
        self.__issue_start_date = issue_start_date

    def is_created(self):
        return self.__is_created;

    
    def get_case_id(self):
        return self.__case_id


    def create(self):
        if not self.__is_case_input_valid():
            raise ValueError("Invalid input")
        
        self.__build_create_case_payload()
        self.__create_case()

    def is_ftc_case(self):
        case_id = self.__case_id
        is_ftc = False
        if case_id[:3] == "FTC":
            is_ftc = True
        return is_ftc

    def __is_case_input_valid(self):
        for attr in self.__CASE_REQUIRED_ATTRIBUTES:
            if attr not in self.__inputted_attributes:
                raise ValueError(f"{attr} is required")

        if not (any(key in self.__inputted_attributes) for key in ["lognote", "phonenote"]):
            raise ValueError(f"lognote or phonenote is required")

        if self.__is_send_sms:
            for sms_attr in self.__SMS_REQUIRED_ATTRIBUTES:
                if sms_attr not in self.__inputted_attributes:
                    raise ValueError(f"{sms_attr} is required for sending sms.")
        return True

    
    def __build_create_case_payload(self):
        self.__create_case_input = {
            'subscription': self.__subscription,
            'title': self.__title,
            'caseType1RefId': self.__lvl1,
            'caseType2RefId': self.__lvl2,
            'caseType3RefId': self.__lvl3,
            'caseType4RefId': self.__lvl4,
            'caseType5RefId': self.__lvl5,
            'logNote': self.__log_note,
            'phoneNote': self.__phone_note,
            'wfOperation': "1",
            'wfTarget': self.__queue,
            'channel': "LEX",
            'isSaveDetails': "true",
            'scd_LOB': self.__lob,
            'scd_Reason': self.__reason,
            'scd_FacebookId': self.__fb_id,
            'scd_FacebookChannel': self.__fb_channel,
            'scd_AccountNumber': self.__account_no,
            'isInvokeLambda': "true" if self.__is_send_sms else "false"
        }

        if self.__issue_start_date:
            self.__create_case_input["issueStartDate"] = self.__issue_start_date

        if self.__is_send_sms:
            self.__create_case_input['ivk_name'] = PUBLISH_SMS_THROUGH_RAVEN_LAMBDA


            if self._x_sms_parameters:
                self._x_sms_parameters["smsReceiver"] = self.__sms_receiver;
                
                self.__create_case_input['ivk_payload'] = {
                    "Details": {
                        "Parameters":self._x_sms_parameters
                    }
                }
            else:         
                self.__create_case_input['ivk_payload'] = {
                    "Details": {
                        "Parameters":{
                            "CASEREASON": self.__reason,
                            "CASEREFNUM": self.__sms_ref_num,
                            "SLA": self.__sms_case_sla,
                            "messageId": self.__sms_message_id,
                            "smsReceiver": self.__sms_receiver
                        }
                    }
                }
        
        self.__create_case_payload = {
            "Details": {
                "Parameters": {
                    "CreateCaseInput": json.dumps(self.__create_case_input)
                }
            }
        }

    
    def __create_case(self):
        lmbd_clnt_sg = boto3.client("lambda", region_name = REGION_SINGAPORE)

        try:
            logger.info(f"Create case payload: {self.__create_case_input}")
            create_case_response = lmbd_clnt_sg.invoke(FunctionName = CREATE_CASE_LAMBDA, InvocationType = "RequestResponse", Payload = json.dumps(self.__create_case_payload))
            create_case_response = json.loads(create_case_response['Payload'].read().decode())
            logger.info(f"Create case response: {create_case_response}")
        except Exception as err:
            logger.info(f"Error invoking createcase: {get_exception_str(err)}")
            self.__is_created = False
            return

        if create_case_response['statusCode'] == 200:
            self.__is_created = True
            self.__case_id = create_case_response['caseId']
            logger.info(f"Case created successfully: {self.__case_id }")
        else:
            self.__is_created = False
            logger.error("Case creation failed, statusCode was not 200.")