from __future__ import annotations

import json
import boto3
import logging

import helpers.utils as utils

import resources.states as states
import resources.resourcemapping as resourcemapping

import configuration as configs

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def is_valid_lex_event_to_be_processed(**kwargs) -> bool:
    logger.info(f"Checking if valid lex event: {kwargs}")
    request = kwargs.get("event_data", {})
    page_id = kwargs.get("page_id", "")

    session_state = request.get("sessionState", "")

    if page_id == configs.THEA_PAGE_ID:
        if session_state in [
                    states.MAIN_MENU_STATE,
                    states.THEA_MAIN_MENU_STATE,
                    states.THEA_NIA_MENU_STATE,
                    states.INTENT_STATE,
                    states.SESSION_END_CONFIRMATION_STATE]:
            return True
        return False

    if session_state in [states.MAIN_MENU_STATE, states.INTENT_STATE, states.SESSION_END_CONFIRMATION_STATE]:
        return True
    return False


def invoke_lambda_function_by_session_state(lmb_request_event: dict) -> bool:
    payload = lmb_request_event

    STATE_LMBD_MAPPING_BY_PAGE_ID = {
        configs.GT_PAGE_ID: resourcemapping.state_lmbd_mapping_dict,
        configs.THEA_PAGE_ID: resourcemapping.thea_state_lmbd_mapping_dict,
        configs.MYBUSINESS_PAGE_ID: resourcemapping.myBiz_state_lmbd_mapping_dict,
        configs.GAH_PAGE_ID: resourcemapping.gah_state_lmbd_mapping_dict,
        configs.TM_PAGE_ID: resourcemapping.state_lmbd_mapping_dict
    }

    if "bot" in lmb_request_event.keys():
        payload = lmb_request_event["sessionAttributes"]

    page_id = payload["channel"]
    session_state = payload["sessionState"] if "sessionState" in payload else ""
    lambda_function_to_be_invoked = STATE_LMBD_MAPPING_BY_PAGE_ID[page_id].get(session_state)

    if not lambda_function_to_be_invoked:
        logger.info(f"{session_state} does not exists in state_lambda_mapping")
        return False

    try:
        logger.info(f"Invoking {lambda_function_to_be_invoked}.")
        lmbd_clnt_oregon = boto3.client("lambda", region_name = configs.REGION_OREGON)
        func_reponse = lmbd_clnt_oregon.invoke(FunctionName=lambda_function_to_be_invoked, InvocationType="Event", Payload=json.dumps(payload))
        logger.info(f"{lambda_function_to_be_invoked} response: {func_reponse}")
        return True
    except Exception as error:
        logger.error(f"Error invoking {lambda_function_to_be_invoked}: {utils.get_exception_str(error)}")
        return False
    

