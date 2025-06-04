import logging
import boto3
import json

from configuration import REGION_OREGON
from resources.states import MAIN_MENU_STATE, INTENT_STATE, SESSION_END_CONFIRMATION_STATE
from resources.resourcemapping import (
        state_lmbd_mapping_dict,
        menu_state_mapping_dict,
        state_default_sub_state_mapping_dict,
        lmbd_menu_mapping_dict
    )

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class IntentTools:

    def __init__(self):
        self.invokeLambda = boto3.client("lambda", region_name=REGION_OREGON)
        

    def lex_event_handler(self, data, context):
        botName = data['bot']['name']
        payload = data['sessionAttributes']
        sessionState = payload['sessionState']
        
        if sessionState in [MAIN_MENU_STATE, INTENT_STATE, SESSION_END_CONFIRMATION_STATE]:
            logger.info("lambda was invoked via lex intent : valid")
            default_menu_id = lmbd_menu_mapping_dict[context.function_name]
            default_session_state = menu_state_mapping_dict[default_menu_id]
            payload['menuId'] = default_menu_id
            payload['sessionState'] = default_session_state
            payload['subState'] = state_default_sub_state_mapping_dict[default_session_state]
            payload['botName'] = botName

            return {
                'status': True,
                'payload': payload
            }
        else:
            logger.info("lambda was invoked via lex intent : invalid")
            lambda_to_invoke = ""

            if sessionState in state_lmbd_mapping_dict.keys():
                logger.info("state exists in mapping")
                lambda_to_invoke = state_lmbd_mapping_dict[sessionState]
            else:
                logger.info("state does not exists in mapping")
            
            logger.info(f"lambda to invoke: {lambda_to_invoke}")

            if (lambda_to_invoke != "") and (context.function_name != lambda_to_invoke):
                logger.info("lambda was invoked via lex intent : transferring to the right lambda")
                payload['message'] = data['sessionAttributes']['message']
                self.invokeLambda.invoke(FunctionName=lambda_to_invoke, InvocationType="Event", Payload=json.dumps(payload))
                return {
                    'status': False,
                    'payload': payload
                }
            else:
                logger.info("lambda was invoked via lex intent : main")
                return {
                    'status': True,
                    'payload': payload
                }