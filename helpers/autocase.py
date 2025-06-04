import logging
import boto3
import json

from configuration import *

from resources.casetags import case_tags
from resources.casespiels import case_spiels
from resources.constants import BB_LOB_NAME
from resources.aws_lambda import CHAT_TO_CALL_LAMBDA

from helpers.createcasetools import CreateCaseTools
from helpers.utils import get_exception_str, invoke_chat_to_call
from helpers.resFormatter import ResFormatter


logger = logging.getLogger()
logger.setLevel(logging.INFO)

class AutoCase:

    def __init__(self):
        # initializing default values
        logger.info("Auto case initialization")
        self.__case = CreateCaseTools()
        self.__case_tag = {}

    def __set_session_data(self, sessionTools):
        self.__session_data = sessionTools.get_session_data()

    def __set_log_note(self, caseType, logNotes):
        if logNotes:
            self.__log_note = logNotes
        else:
            self.__log_note = self.create_log_note(caseType)

    def create_log_note(self, caseType):
        # create generic log note here
        custNum = ''
        if self.__lob_name == BB_LOB_NAME:
            custNum = self.__session_data['lastLandline'] if self.__session_data['lastLandline'] not in ['String', ''] else self.__session_data['lastAccountNumber']
        else:
            custNum = self.__session_data['lastMsisdn'] if self.__session_data['lastMsisdn'] not in ['String', ''] else self.__session_data['lastNumber']
            custNum = custNum.replace(" ","").strip()[-10:]

        return (
            f" Customer number: {custNum}\n"
            f" Case type: {caseType}\n"
        )

    def __set_case_tags(self, caseType):
        self.__case_tag = case_tags[caseType]

    def __set_lob(self, lobName):
        self.__lob_name = lobName

    def __set_session_context_attributes(self, sessionTools):
        self.__session_context_attributes = sessionTools.get_session_context_attributes()

    def auto_case(self, caseSwitch, sessionTools, caseType, logNote = None, sendSMS = True, chat2call = False, payload = None):
        if caseSwitch:
            self.__set_session_data(sessionTools)
            self.__set_session_context_attributes(sessionTools)
            self.__set_case_tags(caseType)
            self.__set_lob(self.__session_data['lastBrand'])
            self.__set_log_note(caseType, logNote)
            self.__case.set_fb_channel(self.__session_data['channel'])
            self.__case.set_fb_id(self.__session_data['fbId'])
            self.__case.set_title(self.__case_tag['title'])
            self.__case.set_lvl1(self.__case_tag['lvl1'])
            self.__case.set_lvl2(self.__case_tag['lvl2'])
            self.__case.set_lvl3(self.__case_tag['lvl3'])
            self.__case.set_lvl4(self.__case_tag['lvl4'])
            self.__case.set_lvl5(self.__case_tag['lvl5'])
            self.__case.set_lob(self.__lob_name)
            self.__case.set_log_note(self.__log_note, sessionContextAttributes=self.__session_context_attributes)
            self.__case.set_queue(self.__case_tag['queue'])
            self.__case.set_reason(self.__case_tag['reason'])

            res = ResFormatter(self.__session_data['channel'])
            senderId = self.__session_data['fbId']

            if self.__lob_name == BB_LOB_NAME:
                subscription = self.__session_data['lastLandline'] if self.__session_data['lastLandline'] not in ['String', ''] else self.__session_data['lastAccountNumber']
                self.__case.set_subscription_bb(subscription)
                self.__case.set_is_send_sms(False)
            else:
                subscription = self.__session_data['lastMsisdn'] if self.__session_data['lastMsisdn'] not in ['String', ''] else self.__session_data['lastNumber']
                self.__case.set_subscription(subscription)
                self.__case.set_is_send_sms(sendSMS)
                self.__case.set_sms_case_sla(self.__case_tag['sla'])
                self.__case.set_sms_receiver(self.__session_data['lastNumber'])

            try:
                self.__case.create()
            except Exception as e:
                logger.error(f"create case error: {get_exception_str(e)}")

            if self.__case.is_created():
                logger.info(f"Auto Case creation success")
                res.send_message(senderId, case_spiels[caseType].format(self.__case.get_case_id()))
            else:
                logger.info(f"Auto Case creation failed")

            logger.info(f"chat2call {chat2call}")
            logger.info(f"payload {payload}")

            if chat2call:
                # invoke chat to call lamdba
                invoke_chat_to_call(payload)
            else:
                sessionTools.reset_user_input()
            return self.__case.is_created()
        else:
            return False
