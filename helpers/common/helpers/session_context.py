import logging

from typing import Any

from helpers.cms_tools import CMSTools
from helpers.resFormatter import ResFormatter
from helpers.sessiontools import SessionTools
from helpers.dpntools import DataPrivacyNotice
from helpers.customerjourneytools import CustomerJourney

import resources.tableattributes as tableattributes

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class SessionContext:
    def __init__(self, request: dict):
        self.__request = request
        self.__psid = request.get(tableattributes.FB_ID, "")
        self.__page_id = request.get(tableattributes.CHANNEL, "")
        self.__session_state = request.get(tableattributes.SESSION_STATE, "")
        self.__sub_state = request.get(tableattributes.SUB_STATE, "")
        self.__is_flow_end = False
        self.__message = request.get("message", "").strip()

        self.__session_tools = SessionTools(self.__psid, self.__page_id)
        self.__res_formatter = ResFormatter(self.__page_id)
        self.__cms_tools = CMSTools()
        self.__dpn = DataPrivacyNotice(self.__psid, self.__page_id)
        self.__cj = CustomerJourney(self.__psid, self.__page_id)

    @property
    def request(self) -> dict:
        return self.__request
    
    @property
    def psid(self):
        return self.__psid

    @property
    def page_id(self):
        return self.__page_id

    @property
    def session_state(self):
        return self.__session_state

    @property
    def sub_state(self):
        return self.__sub_state
    
    @property
    def is_flow_end(self):
        return self.__is_flow_end
    
    @is_flow_end.setter
    def is_flow_end(self, value: bool):
        self.__is_flow_end = value
    
    @property
    def message(self):
        return self.__message

    @property
    def session_tools(self):
        return self.__session_tools

    @property
    def res_formatter(self):
        return self.__res_formatter

    @property
    def cms_tools(self):
        return self.__cms_tools

    @property
    def dpn(self):
        return self.__dpn

    @property
    def cj(self):
        return self.__cj

    
    def set_req_attr(self, name, value) -> None:
        self.__request[name] = value
    