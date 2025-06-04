import logging
import time 
import boto3
import copy
import json

import configuration as configs

from helpers.resFormatter import ResFormatter
from helpers.whitelistchecker import *
import resources.spiels as spiels
import resources.constants as constants

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class Optin:

    def __init__(self, sender_id, page_id):
        self.__page_id = page_id
        self.__sender_id = sender_id

        self.__res_formatter = ResFormatter(self.__page_id) 
            
    def execute_optin_flow(self, title, frequency):
        logger.info(f"initiating recurring notifiacations...")
        rec_notif_data = is_recurring_notif_opted(self.__sender_id, self.__page_id)
        if rec_notif_data == False:
            logger.info(f"User {self.__sender_id} is eligible for opt-in.")
            self.__res_formatter.send_notif_message_optin(self.__sender_id, title, "", frequency)