# NIAS 2.0 - HISAMS - 2022-02-14
from __future__ import annotations

import time
import random
import logging
import asyncio

from helpers.ddbtools import DDBTools
from helpers.ddbutils import DDBUtils
from helpers.resFormatter import ResFormatter
from helpers.facebooktools import FacebookTools
from helpers.data_logger.datalogger import DataLogger
from helpers.data_logger.conf import LOG_TYPE_SINGLE_IDENTITY_CROSSING_USER
from helpers.utils import (
    generate_random_id,
    get_current_time,
    get_exception_str
)
from helpers.utilities.logger import (
    log_execution_time
)

from resources.resourcemapping import (
    page_ddb_mapping_dict,
    page_name_mapping_dict
)
from resources.constants import (
    SESSION_STATUS_TICKET_CLOSURE
)
from resources.spiels import (
    SINGLE_IDENTITY_CURRENT_PAGE_NOTIFY_SPIELS,
    SINGLE_IDENTITY_ACTIVE_PAGE_NOTIFY_SPIELS
)

from configuration import (
    SECONDARY_APP_ID,
    REGION_OREGON,
    DDB_FACEBOOK_USER_IDENTITY,
    GT_PAGE_ID,
    THEA_PAGE_ID,
    TM_PAGE_ID,
    GAH_PAGE_ID,
    TM_PAGE_ID,
    MYBUSINESS_PAGE_ID,
    SWITCH_FB_PAGES_SINGLE_IDENTITY_PAGES,
    MESSENGER_PAGE_URLS
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ENTITY_AGENT = "AGENT"
ENTITY_BOT = "BOT"


PSID_KEY_ATTRIBUTES = {
    GT_PAGE_ID: {
        "attribute_name": "psidGt",
        "index_name": "psidGt-index"
    },
    MYBUSINESS_PAGE_ID: {
        "attribute_name": "psidBiz",
        "index_name": "psidBiz-index"
    },
    THEA_PAGE_ID: {
        "attribute_name": "psidThea",
        "index_name": "psidThea-index"
    },
    GAH_PAGE_ID: {
        "attribute_name": "psidGah",
        "index_name": "psidGah-index"
    },
    TM_PAGE_ID: {
        "attribute_name": "psidTm",
        "index_name": "psidTm-index"
    }
}

""" Contains the requied id attributes from table. This is based on the pages switche. """
REQUIRED_ID_ATTRIBUTES = [PSID_KEY_ATTRIBUTES[pageid]["attribute_name"] for pageid in SWITCH_FB_PAGES_SINGLE_IDENTITY_PAGES 
        if SWITCH_FB_PAGES_SINGLE_IDENTITY_PAGES[pageid].strip().upper() == "ON"]

SWITCHED_ON_PAGE_IDS = [pageid for pageid in SWITCH_FB_PAGES_SINGLE_IDENTITY_PAGES 
        if SWITCH_FB_PAGES_SINGLE_IDENTITY_PAGES[pageid].strip().upper() == "ON"]


""" *****************************************************************************************************
    *****************************************************************************************************
    *****************************************************************************************************
    If you'll be modifying this class, please observe code pattern.
    Consider others who will modify or read this.
    -HISAM
    *****************************************************************************************************
    *****************************************************************************************************
    *****************************************************************************************************
"""
class FbPagesSingleIdentity:

    def __init__(self, page_id: str, psid: str, identity_key: str = ""):
        self.__page_id = page_id
        self.__psid = psid

        self.__ddb_fbui:DDBTools = DDBTools(DDB_FACEBOOK_USER_IDENTITY, REGION_OREGON)
        self.__facebook_tools:FacebookTools = FacebookTools()
        self.__response_formatter:ResFormatter = ResFormatter(self.__page_id)
        self.__data_logger = None
        self.__ddb_main_instances = {}

        self.__has_an_active_bot_session = False
        self.__has_an_active_agent_session = False
        self.__user_identity_data = {}
        self.__user_psids = {}
        self.__user_page_thread_owners = {}
        self.__active_entity = ""
        self.__active_page_id = ""
        self.__active_psid = ""
        self.__identity_key = identity_key
        self.__is_identity_key_exists:bool = True if self.__identity_key.strip() else False

        self.__init_identity_check()


    def __init_identity_check(self) -> None:
        logger.info(f"Initiating FbPagesSingleIdentity for user {self.__psid}...")
        is_user_and_main_identity_keys_equals:bool = True

        if not self.__is_identity_key_exists:
            # identity_key does not exists from the current page main table
            logger.info(f"Current user MAIN data does not have \"identityKey\".")
            self.__user_psids = self.__get_user_psids_from_api()

            if not self.__user_psids:
                logger.info(f"NO psids returned from \"get_ids_for_pages\" api.")
                return

            self.__user_page_thread_owners = asyncio.run(self.__get_thread_owners_from_api_async())

            counter_001_start = time.perf_counter()
            self.__user_identity_data = self.__get_user_identity_data_by_user_psids()
            counter_001_end = time.perf_counter()
            self.__performance_logger(counter_001_start, counter_001_end, "Getting user identity data by psids")
            logger.info(f"facebookUserIdentity data by psid result: {self.__user_identity_data}")

            if self.__user_identity_data:
                logger.info(f"One or More/All psid(s) exist(s) on identity table.")
                self.__identity_key = self.__user_identity_data["identityKey"]
                self.__update_identity_data_psids()
            else:
                logger.info(f"None of psid(s) exist(s) on user identity table.")
                self.__user_identity_data = self.__create_user_identity_data()
            
            self.__update_identity_key_on_main_tables()
            return
            
        # identity_key exists from the current page main table
        logger.info(f"Current user MAIN data has identityKey: {self.__identity_key}")
        self.__user_identity_data = self.__get_user_identity_data_by_identity_key(self.__identity_key)
        
        if not self.__user_identity_data:
            logger.info(f"identityKey exists from MAIN data, but does not exists on userIdentity data.")

            self.__user_identity_data = self.__get_user_identity_data_by_psid(self.__page_id, self.__psid)
                
            if not self.__user_identity_data:
                logger.info(f"psid does not exists on userIdentity data.")
                self.__user_psids = self.__get_user_psids_from_api()
                self.__user_page_thread_owners = asyncio.run(self.__get_thread_owners_from_api_async())
                self.__user_identity_data = self.__create_user_identity_data()
                self.__identity_key = self.__user_identity_data["identityKey"]
                self.__update_identity_key_on_main_tables()

                logger.info(f"User identity data from creating new: {self.__user_identity_data}")
                return
            else:
                is_user_and_main_identity_keys_equals = False

        logger.info(f"User identity data: {self.__user_identity_data}")
        self.__identity_key = self.__user_identity_data["identityKey"]

        if self.__are_required_psid_attributes_exist():
            logger.info(f"All required attributes exist.")
            self.__user_psids = self.__get_user_psids_from_identity_data()
        else:
            logger.info(f"Not all required attributes exist.")
            self.__user_psids = self.__get_user_psids_from_api()
            
        self.__user_page_thread_owners = asyncio.run(self.__get_thread_owners_from_api_async())
        self.__update_identity_data_psids()

        if not is_user_and_main_identity_keys_equals:
            logger.info(f"identityKey exists on main but not equals to identityKey on facebookUserIdentity.")
            self.__identity_key = self.__user_identity_data["identityKey"]
            self.__update_identity_key_on_main_tables()

    
    def __update_identity_data_psids(self) -> None:
        update_item = {}
        update_item = {
            "updateTimestamp": get_current_time()
        }
        
        for pageid, psid in self.__user_psids.items():
            id_attr = PSID_KEY_ATTRIBUTES[pageid]["attribute_name"]
            update_item[id_attr] = psid

        logger.info(f"Updating user identity data with: {update_item}")

        try:
            self.__ddb_fbui.update_item("identityKey", self.__identity_key, update_item)
        except Exception as error:
            logger.error(f"Error updating identity psid and threadInfos: {get_exception_str(error)}")

    
    """ Check if requied page id attributes are existing on user identity table """
    def __are_required_psid_attributes_exist(self) -> bool:
        for attribute in REQUIRED_ID_ATTRIBUTES:
            if attribute not in self.__user_identity_data:
                return False
        return True

    
    """ Getting the PSIDs from Matching API """
    def __get_user_psids_from_api(self) -> dict:
        logger.info(f"Getting psids via get_ids_for_pages api.")
        page_ids_data = self.__facebook_tools.get_ids_for_pages(self.__page_id, self.__psid)
        ids_data = {}

        for page_data in page_ids_data:
            pageid = page_data["page"]["id"]
            psid = page_data["id"]
            
            # Only get the page id which is part of Project Lex since Globe BusinessManager may be handling other fb pages.
            if page_data["page"]["id"] in SWITCHED_ON_PAGE_IDS:
                ids_data[pageid] = psid

        return ids_data


    """ Getting the PSIDs from identity table """
    def __get_user_psids_from_identity_data(self) -> dict:
        psids = {}
        for pageid, value in PSID_KEY_ATTRIBUTES.items():
            psids[pageid] = self.__user_identity_data[value["attribute_name"]]
        
        return psids


    """ Get thread owners of pages from get_thread_owner API """
    async def __get_thread_owners_from_api_async(self) -> dict:
        logger.info(f"Getting thread owners via get_thread_owner api.")
        thread_owners = {}

        counter_004_start = time.perf_counter()
        owners_info = await asyncio.gather(*[self.__facebook_tools.get_thread_owner_async(pageid, psid) for pageid, psid in self.__user_psids.items()])
        
        logger.info(f"owners_info: {owners_info}")
        for info in owners_info:
            thread_owners[info["page_id"]] = info["owner_app_id"]
        counter_004_end = time.perf_counter()
        self.__performance_logger(counter_004_start, counter_004_end, "Getting thread info via async API")

        return thread_owners


    """ Creating data in single identity table for new entries """
    def __create_user_identity_data(self) -> dict:
        logger.info(f"Creating user identity data...")
        fname, lname = self.__get_fb_name()    

        create_data = {}
        create_data["firstName"] = fname
        create_data["lastName"] = lname
        create_data["identityKey"] = generate_random_id()
        create_data["createTimestamp"] = get_current_time()

        for pageid, psid in self.__user_psids.items():
            id_attr = PSID_KEY_ATTRIBUTES[pageid]["attribute_name"]
            create_data[id_attr] = psid

        if not self.__ddb_fbui.put_item(create_data):
            logger.info(f"Failed to add user identity item.")
            return {}
        
        return create_data


    def __get_main_psids(self) -> list:
        main_psids = []
        batch_keys = {}

        for pageid, psid  in self.__user_psids.items():
            if not pageid in SWITCHED_ON_PAGE_IDS:
                continue
            table_name = page_ddb_mapping_dict[pageid]['main']
            batch_keys[table_name] = {
                "Keys": [{ 'fbId': psid}]
            }
        
        logger.info(f"Get MAIN psids batch_keys: {batch_keys}")

        responses = DDBUtils.batch_get_item(REGION_OREGON, batch_keys)
        logger.info(f"Responses: {responses}")

        for table, items in responses.items():
            if len(items):
                main_psids.append(items[0]["fbId"])

        return main_psids


    def __update_identity_key_on_main_tables(self) -> None:
        counter_007_start = time.perf_counter()
        main_psids = self.__get_main_psids()

        for pageid, psid in self.__user_psids.items():
            if pageid not in self.__ddb_main_instances.keys() or not self.__ddb_main_instances[pageid]:
                self.__ddb_main_instances[pageid] = DDBTools(page_ddb_mapping_dict[pageid]['main'], REGION_OREGON) 

            if psid in main_psids:
                logger.info(f"Main data for psid: {psid} EXISTS on {page_ddb_mapping_dict[pageid]['main']}")
                self.__ddb_main_instances[pageid].update_item("fbId", psid, {"identityKey": self.__user_identity_data["identityKey"]})
            else:
                logger.info(f"Main data for PSID: {psid} does NOT EXISTS on {page_ddb_mapping_dict[pageid]['main']}.")

        counter_007_end = time.perf_counter()
        self.__performance_logger(counter_007_start, counter_007_end, "Updating main with identityKey")


    def __get_user_identity_data_by_user_psids(self) -> dict:
        logger.info(f"Getting identity data by psids.")
        for pageid, psid in self.__user_psids.items():
            data_result = self.__get_user_identity_data_by_psid(pageid, psid)
            if data_result:
                return data_result

        return {}

    
    def __get_user_identity_data_by_identity_key(self, identity_key: str) -> dict:
        logger.info(f"Getting user identity data using identityKey: {identity_key}")
        identity_result = self.__ddb_fbui.get_item("identityKey", identity_key)
        if len(identity_result):
            return identity_result[0]
        return {}


    def __get_user_identity_data_by_psid(self, page_id: str, psid: str) -> dict:
        attribute_name = PSID_KEY_ATTRIBUTES[page_id]["attribute_name"]
        index_name = PSID_KEY_ATTRIBUTES[page_id]["index_name"]

        identity_data = self.__ddb_fbui.get_item_by_index(attribute_name, psid, index_name)

        logger.info(f"Getting user identity data by psid. attribute_name={attribute_name}, psid={psid}, index_name={index_name}, result={identity_data}")

        if len(identity_data):
            return identity_data[0]
        return {} 


    """ Checks the thread owner id if is it is to Socio App Id """
    def __is_page_connected_to_an_agent(self, page_id: str) -> bool: 
        if self.__user_page_thread_owners[page_id] == SECONDARY_APP_ID:
            return True
        return False


    def __get_fb_name(self) -> tuple:
        try:
            result = self.__facebook_tools.get_name(self.__page_id, self.__psid)
            fname = result.get("first_name", " ")
            lname = result.get("last_name", " ") 
        except Exception as error:
            logger.error(f"Failed to get fb_name: {get_exception_str(error)}")
            fname = " "
            lname = " "

        return fname, lname


    def __performance_logger(self, start: float, end: float, msg: str) -> None:
        IS_TRACK_PERFORMANCE = True
        if IS_TRACK_PERFORMANCE:
            log_execution_time(start, end, msg)


    def __get_current_page_options_spiel(self, pageid: str, spiel: str = "") -> dict:        
        option_btn_template = {}
        option_btn_template["spiel"] = spiel
        option_btn_template["buttons"] = []
        option_btn_template["buttons"].append({
            "title": "Go back",
            "url": MESSENGER_PAGE_URLS[pageid]
        })
        logger.info(f"Option spiels template: {option_btn_template}") 
        return option_btn_template



    """ ******************************************************************************************************************
    **************************************** Public methods **************************************************************
    ****************************************************************************************************************** """

    def has_active_bot_session(self) -> bool:
        if not self.__user_psids:
            return False

        batch_keys = {}
        table_psid_map = {}

        for pageid, psid  in self.__user_psids.items():
            if not pageid in SWITCHED_ON_PAGE_IDS or self.__page_id == pageid:
                continue

            table_name = page_ddb_mapping_dict[pageid]['session']
            batch_keys[table_name] = {
                "Keys": [{ 'fbId': psid}]
            }
            table_psid_map[table_name] = psid
        
        logger.info(f"Session tables batch_get_item:batch_keys: {batch_keys}")

        if not batch_keys:
            return False

        responses = DDBUtils.batch_get_item(REGION_OREGON, batch_keys)

        for table, items in responses.items():
            if len(items) and items[0]["status"] != SESSION_STATUS_TICKET_CLOSURE:
                logger.info(f'User is currently has an active BOT session on: {page_name_mapping_dict[items[0]["pageId"]]}')
                self.__active_entity = ENTITY_BOT
                self.__active_page_id = items[0]["pageId"].strip()
                self.__active_psid = table_psid_map[table]
                self.__has_an_active_bot_session = True
                return True

        self.__has_an_active_bot_session = False
        return False
        

    def has_active_agent_session(self) -> bool:
        logger.info(f"Checking if user has an active AGENT session. thread_owners: {self.__user_page_thread_owners}")
        for pageid, psid  in self.__user_psids.items():
            if not pageid in SWITCHED_ON_PAGE_IDS or self.__page_id == pageid:
                continue

            if self.__is_page_connected_to_an_agent(pageid):
                logger.info(f"User is currently connected to an AGENT on: {page_name_mapping_dict[pageid]}")
                self.__active_entity = ENTITY_AGENT
                self.__active_page_id = pageid
                self.__active_psid = psid
                self.__has_an_active_agent_session = True
                return True
        logger.info(f"User has no active AGENT session.")
        self.__has_an_active_agent_session = False
        return False


    def has_active_session(self, is_fresh: bool = True) -> bool:
        logger.info(f"Checking if user has an active session either on BOT or AGENT. is_fresh={is_fresh}")
        if is_fresh:
            if self.has_active_bot_session() or self.has_active_agent_session():
                return True
            return False
        
        if self.__has_an_active_bot_session or self.__has_an_active_agent_session:
            return True
        return False

    
    def is_bot_session_active(self) -> bool:
        if self.__active_entity == ENTITY_AGENT:
            return True
        return False

    
    def is_agent_session_active(self) -> bool:
        if self.__active_entity == ENTITY_BOT:
            return True
        return False

    def get_active_entity(self) -> str:
        return self.__active_entity

    
    def get_active_page_id(self) -> str:
        return self.__active_page_id

    
    def get_active_psid(self) -> str:
        return self.__active_psid


    def get_first_name(self) -> str:
        return self.__user_identity_data.get("firstName", "")


    def get_last_name(self) -> str:
        return self.__user_identity_data.get("lastName", "")


    def get_fb_name(self) -> str:
        fname = self.__user_identity_data.get("firstName", "")
        lname = self.__user_identity_data.get("lastName", "")
        return f"{fname} {lname}"


    def notify_user_on_active_page(self, notif_spiel: str = "") -> None:
        active_page_id = self.get_active_page_id()
        active_psid = self.get_active_psid()
        resformatter = ResFormatter(active_page_id)

        logger.info(f"Notifying user from the active page. page_id={active_page_id}, psid={active_psid}")

        if not notif_spiel:
            spiel_index = random.randint(0, (len(SINGLE_IDENTITY_ACTIVE_PAGE_NOTIFY_SPIELS) - 1))
            notif_spiel = SINGLE_IDENTITY_ACTIVE_PAGE_NOTIFY_SPIELS[spiel_index].format(page_name_mapping_dict[self.__page_id])

        if self.__active_entity == ENTITY_BOT:
            resformatter.send_message(active_psid, notif_spiel)
        else:
            logger.info(f"User is active on AGENT on {page_name_mapping_dict[active_page_id]}, we'll not notify.")

    
    def notify_user_on_current_page(self, notif_spiel: str = "") -> None:
        logger.info(f"Notifying user from current page. page_id={self.__page_id}, psid={self.__psid}")
        active_page_id = self.get_active_page_id()
        if not self.__response_formatter:
            self.__response_formatter = ResFormatter(self.__page_id)

        if not notif_spiel:
            spiel_index = random.randint(0, (len(SINGLE_IDENTITY_CURRENT_PAGE_NOTIFY_SPIELS) - 1))
            notif_spiel = SINGLE_IDENTITY_CURRENT_PAGE_NOTIFY_SPIELS[spiel_index].format(page_name_mapping_dict[active_page_id])

        options_spiel = self.__get_current_page_options_spiel(active_page_id, notif_spiel)
        buttons = options_spiel["buttons"]
        spiel = options_spiel["spiel"]
        self.__response_formatter.send_option_buttons(self.__psid, spiel, buttons, True)

    
    def log_crossing_data(self):
        if not self.__has_an_active_bot_session and not self.__has_an_active_agent_session:
            logger.info(f"Cannot log data unless user has an active session on other page.")

        if not self.__data_logger:
            self.__data_logger = DataLogger()

        log_data = {
            "fbName": f"{self.get_first_name()} + {self.get_last_name()}",
            "currentPsid": self.__psid,
            "currentPageId": self.__page_id,
            "currentPageEntity": "BOT",
            "activePsid": self.__active_psid,
            "activePageId": self.__active_page_id,
            "activePageEntity": self.__active_entity
        }
        
        try:
            self.__data_logger.log_data(log_type=LOG_TYPE_SINGLE_IDENTITY_CROSSING_USER, data=log_data)
        except Exception as error:
            logger.error(f"Error logging data: {get_exception_str(error)}")