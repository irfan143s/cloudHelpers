import logging              

import helpers.utils as utils

from helpers.ddbtools import DDBTools
from helpers.sessiontools import SessionTools

from configuration import REGION_SINGAPORE, REGION_OREGON, DDB_CASE_CREATED, DDB_CHECK_OPEN_CASE_REPORT, pageDictionary

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class OpenCaseTagging:
    
    def __init__(self, sender_id, page_id):
        self.__sender_id = sender_id
        self.__page_id = page_id
        self.__page_name = pageDictionary.get(page_id, "null")
        self.__ddb_case_created = DDBTools(DDB_CASE_CREATED, REGION_SINGAPORE)
        self.__ddb_report = DDBTools(DDB_CHECK_OPEN_CASE_REPORT, REGION_OREGON)
        self.__session_tools = SessionTools(sender_id, page_id)
        self.__session_data = self.__session_tools.get_session_data()
        self.__account_number = self.__session_data['lastAccountNumber'] if self.__is_valid_value(self.__session_data['lastAccountNumber']) else ""
        self.__msisdn = self.__session_data['lastMsisdn'] if self.__is_valid_value(self.__session_data['lastMsisdn']) else ""
        self.__landline = self.__session_data['lastLandline'] if self.__is_valid_value(self.__session_data['lastLandline']) else ""
        self.__intent = self.__session_data['lastIntent'] if self.__is_valid_value(self.__session_data['lastIntent']) else ""
    

    def append_open_case_tagging(self, caseDetails):
        open_case_tagging_data = {
            'uuid': utils.generate_random_id(),
            'tagTimestamp': utils.get_current_time(),
            'qryIdx': 'QI',
            'channel': 'LEX',
            'fbId': self.__sender_id,
            'callingNumber': '',
            'pageId': self.__page_id,
            'pageName': self.__page_name,
            'accountNumber': self.__account_number,
            'msisdn': self.__msisdn,
            'landline': self.__landline,
            'intent': self.__intent,
            'caseId': caseDetails['latestOpenCaseId'] if 'latestOpenCaseId' in caseDetails else "",
            'caseTitle': caseDetails['latestOpenCaseTitle'] if 'latestOpenCaseTitle' in caseDetails else "",
            'caseTypeLevel1': caseDetails['latestOpenCaseType1'] if 'latestOpenCaseType1' in caseDetails else "",
            'caseTypeLevel2': caseDetails['latestOpenCaseType2'] if 'latestOpenCaseType2' in caseDetails else "",
            'caseTypeLevel3': caseDetails['latestOpenCaseType3'] if 'latestOpenCaseType3' in caseDetails else "",
            'caseStatus': caseDetails['latestOpenCaseStatus'] if 'latestOpenCaseStatus' in caseDetails else "",
            'caseCreationDate': caseDetails['latestOpenCaseCreationTimestamp'] if 'latestOpenCaseCreationTimestamp' in caseDetails else ""
        }

        if self.__intent != "":
            logger.info(f"open_case_tagging -> entry : {open_case_tagging_data}")
            try:
                self.__ddb_report.put_item(open_case_tagging_data)
            except Exception as error:
                logger.info(f"Error inserting open_case_tagging data: {utils.get_exception_str(error)}")

    def get_case_title(self, caseId):
        result = self.__ddb_case_created.get_item('CaseId', caseId)
        caseTitle = result.Title if result else ''
        return caseTitle

    def __is_valid_value(self, value):
        if value.strip() not in ["", "String"]:
            return True
        return False
