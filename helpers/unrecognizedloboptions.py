from configuration import socioBasket
from resources.spiels import LOB_OPTIONS_UNRECOGNIZED_NUMBER, LOB_OPTIONS_IDENTIFY_ACCOUNT, CONNECT_TO_AN_AGENT_SPIEL, INVALID_SUB_INTENT_MENU_SPIEL
from helpers.utils import invoke_transfer_to_agent
from helpers.facebooktools import FacebookTools
from helpers.resFormatter import ResFormatter
from resources.constants import *
from helpers.sessiontools import SessionTools

import helpers.common.utils.flow as common_utils_flow

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def render_spiels_options(**kwargs):
    session_attributes = kwargs.get("session_attributes")
    channel = session_attributes.get("channel")
    sender_id = session_attributes.get("fbId")

    sessionTools = SessionTools(sender_id, channel)
    method = kwargs.get("method", "")
    res_formatter = ResFormatter(channel)

    if method == "handle_invalid_sub_intent_menu":
        res_formatter.send_message(sender_id, INVALID_SUB_INTENT_MENU_SPIEL)
    else:
        session_context_attributes = sessionTools.get_session_context_attributes()
        if session_context_attributes.get("checkNumberConfirmation", "false") == "false":
            res_formatter.send_message(sender_id, LOB_OPTIONS_UNRECOGNIZED_NUMBER)
    return render_lob_options_only(resFormatter = res_formatter, sender_id = sender_id)

def render_lob_options_only(**kwargs):
    res_formatter = kwargs.get('resFormatter')
    sender_id = kwargs.get('sender_id')
    first_buttons = {
        "spiel":"Mobile",
        "buttons": [
            { "title":"Globe Postpaid", "optionId": "globepostpaid" },
            { "title":"Globe Prepaid", "optionId": "globeprepaid" },
            { "title":"TM", "optionId": "globetm" }
        ]
    }
    second_buttons = {
        "spiel":"Globe At Home (GAH)",
        "buttons": [
            { "title":"GAH Broadband", "optionId": "gahpostpaid" },
            { "title":"GAH Home Prepaid Wifi", "optionId": "gahhpw" },
            { "title":"GFiber Prepaid", "optionId": "gfiberprepaid" }
        ]
    }

    res_formatter.send_message(sender_id, LOB_OPTIONS_IDENTIFY_ACCOUNT)
    res_formatter.send_option_buttons(sender_id, first_buttons["spiel"], first_buttons["buttons"],False)
    res_formatter.send_option_buttons(sender_id, second_buttons["spiel"], second_buttons["buttons"],False)

def handle_selected_option(**kwargs):
    session_attributes = kwargs.get("session_attributes", {})
    option_id = session_attributes.get("menuId", "")
    page_id = session_attributes.get("channel")
    sender_id = session_attributes.get("fbId")
    lob_name = ""
    support_intent = ""

    fbtools = FacebookTools()
    getUser = fbtools.get_name(page_id, sender_id)

    if option_id:
        if option_id == "[option].globepostpaid":
            # lob = "postpaid"
            lob_name = POSTPAID_LOB_NAME
            support_intent = "postpaid-regular"
            logger.info("selected globepostpaid")

        elif option_id == "[option].globeprepaid":
            # lob = "prepaid"
            lob_name = PREPAID_LOB_NAME
            support_intent = "prepaid-regular"
            logger.info("selected globeprepaid")

        elif option_id == "[option].globetm":
            # lob = "prepaid"
            lob_name = TM_LOB_NAME
            support_intent = "prepaid-regular"
            logger.info("selected globetm")

        elif option_id == "[option].gahpostpaid":
            # lob = "main"
            lob_name = BB_LOB_NAME
            support_intent = "broadband-regular"
            logger.info("selected gahpostpaid")

        elif option_id == "[option].gahhpw":
            # lob = "main"
            lob_name = PREPAID_HOME_WIFI_LOB_NAME
            support_intent = "hpw-regular"
            logger.info("selected gahhpw")

        else:
            logger.info("invalid option id")

        # intent_id = socioBasket[page_id][lob]

        intents = [AGENT_INTENT]
        first_name = getUser["first_name"] if (getUser and ("first_name" in getUser.keys()))  else "NA"
        last_name = getUser["last_name"] if (getUser and ("last_name" in getUser.keys())) else "NA"

        meta_data = {
        "fbId": sender_id,
        "lob": lob_name,
        "intent": intents,
        "first_name": first_name,
        "last_name": last_name,
        "support_intent": support_intent
        }
        # all lobs are going to LP
        if support_intent:
            return common_utils_flow.transfer_to_live_person_agent(request = session_attributes, support_intent = support_intent)

        # ttaResponse = invoke_transfer_to_agent(session_attributes, intent_id, meta_data, CONNECT_TO_AN_AGENT_SPIEL)
        # ttaResponse = common_utils_flow.transfer_to_live_person_agent(request = session_attributes, support_intent = support_intent)
        # logger.info(f"Connect to Agent: {ttaResponse}")     
    else:
        logger.info("no option id")