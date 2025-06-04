from __future__ import annotations

import copy
import json
import boto3
import logging

import helpers.utils as utils
import helpers.common.utils.formatter as formatter_utils
import resources.aws_lambda as lmb_functions
import resources.common.constants.templates as templates
import resources.constants as constants
import resources.common.constants.str as str_const

import configuration as configs

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_cem_suggestions(**kwargs) -> dict:
    request_payload = copy.deepcopy(templates.CONNECT_LMB_REQUEST)
    lmbd_clnt_sg = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)

    channel = kwargs.get("channel", "")
    session_id = kwargs.get("sessionId", "")
    date_period = kwargs.get("datePeriod", "")
    case_type = kwargs.get("caseType", "")
    request_type = kwargs.get("requestType", "").lower()
    msisdn = kwargs.get("msisdn","")

    request_payload['Details']['Parameters'].update({
        "channel": channel,
        "sessionId": session_id,
        "datePeriod": date_period,
        "caseType": case_type,
        "requestType": request_type,
        "msisdn": msisdn
    })

    invokation_type = "RequestResponse" if request_type == "sync" else "Event"
    
    try:
        cem_suggestions_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.GET_CEM_SUGGESTIONS_LAMBDA, InvocationType=invokation_type, Payload=json.dumps(request_payload))
        return json.loads(cem_suggestions_response['Payload'].read().decode())
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.GET_CEM_SUGGESTIONS_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}



def update_connect_chat_session_status(**kwargs) -> dict:
    lmbd_clnt = boto3.client("lambda", region_name=configs.REGION_SYDNEY)

    user_id = kwargs.get("user_id", "")
    channel_id = kwargs.get("channel_id", "")
    status = kwargs.get("status", "")

    if not user_id:
        logger.info(f"chat_update_session_status() user_id:str is required")
        return {}

    if not channel_id:
        logger.info(f"chat_update_session_status() channel_id:str is required")
        return {}

    if not status:
        logger.info(f"chat_update_session_status() status:str is required")
        return {}
 
    request_payload = {
        "userId": user_id,
        "channelId": channel_id,
        "status": status
    }
    
    try:
        response = lmbd_clnt.invoke(FunctionName = lmb_functions.CHAT_UPDATE_SESSION_STATUS, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        return json.loads(response['Payload'].read().decode())
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.CHAT_UPDATE_SESSION_STATUS} due to: {utils.get_exception_str(error)}")
        return {}
        

def get_customer_info_api(**kwargs) -> dict:
    lmbd_clnt_sg = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)

    account_no = kwargs.get("account_no", "")
    msisdn = kwargs.get("msisdn", "")

    request_payload = {
        "payload": {}
    }

    if msisdn:
        request_payload["payload"]["ResourceValue"] = msisdn
    else:
        request_payload["payload"]["AccountNumber"] = account_no

    logger.info(f"[[{lmb_functions.GET_CUSTOMER_INFO_API_LAMBDA}]] request: {request_payload}")
    
    try:
        get_customer_info_api_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.GET_CUSTOMER_INFO_API_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        get_customer_info_api_response = json.loads(get_customer_info_api_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.GET_CUSTOMER_INFO_API_LAMBDA}]] response: {get_customer_info_api_response}")
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.GET_CUSTOMER_INFO_API_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}

    if not get_customer_info_api_response.get("statusCode", 0) == 200:
        return {}
    
    return get_customer_info_api_response.get("body", {}).get("GetCustomerInfoResult", [])[0] if get_customer_info_api_response["body"] else {}


def reconnection(**kwargs) -> bool:
    request_payload = kwargs.get("payload", {})

    lmbd_clnt_sg = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)

    try:
        reconnection_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.DISCONNECTION_CONNECT_LAMBDA, InvocationType="Event", Payload=json.dumps(request_payload))
        logger.info(f"[[{lmb_functions.DISCONNECTION_CONNECT_LAMBDA} response: {reconnection_response}]]")
        return True
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.DISCONNECTION_CONNECT_LAMBDA} due to: {utils.get_exception_str(error)}")
        return False


def publish_sms_through_raven(**kwargs):
    lmbd_clnt_sg = boto3.client("lambda", region_name = configs.REGION_SINGAPORE)
    
    payload = kwargs.get("payload", {})
    logger.info(f"Payload: {payload}")

    try:
        logger.info(f"Request[{lmb_functions.SMS_CONNECT_LAMBDA}]: {payload}")
        send_sms_res = lmbd_clnt_sg.invoke(FunctionName=lmb_functions.SMS_CONNECT_LAMBDA, InvocationType="Event", Payload=json.dumps(payload))
        logger.info(f" Response[{lmb_functions.SMS_CONNECT_LAMBDA}]: {send_sms_res}")
    except Exception as err:
        logger.error(f"Error invoking {lmb_functions.SMS_CONNECT_LAMBDA}: {utils.get_exception_str(err)}")
        return False

def get_resource_info(**kwargs) -> dict:
    request_payload = copy.deepcopy(templates.CONNECT_LMB_REQUEST)
    lmbd_clnt_sg = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)

    concerned_no = kwargs.get("concerned_no", "")

    request_payload['Details']['ContactData']['Attributes'].update({
        "concernedNumber": concerned_no
    })
    logger.info(f"[[{lmb_functions.GET_RESOURCE_INFO_LAMBDA}]] request: {request_payload}")
    try:
        get_resource_info_api_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.GET_RESOURCE_INFO_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        get_resource_info_api_response = json.loads(get_resource_info_api_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.GET_RESOURCE_INFO_LAMBDA}]] response: {get_resource_info_api_response}]]")
        return get_resource_info_api_response
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.GET_RESOURCE_INFO_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}

def get_assigned_products(**kwargs) -> dict:
    serviceId = kwargs.get("serviceId", {})
    request_payload = {
        "payload": {
            "ResourceValue":serviceId,
            "ResourceType": "SVID"
        }
    }
    
    lmbd_clnt_sg = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)
    logger.info(f"[[{lmb_functions.GET_ASSIGNED_PRODUCTS_API_LAMBDA} request: {request_payload}]]")
    try:
        assigned_products_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.GET_ASSIGNED_PRODUCTS_API_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        assigned_products_response = json.loads(assigned_products_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.GET_ASSIGNED_PRODUCTS_API_LAMBDA} response: {assigned_products_response}]]")
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.GET_ASSIGNED_PRODUCTS_API_LAMBDA} due to: {utils.get_exception_str(error)}")
    
    if not assigned_products_response.get("statusCode", 0) == 200:
        return {}
    
    return assigned_products_response.get("body", {}) if assigned_products_response["body"] else {}

def get_active_products(**kwargs) -> dict:
    request_payload = copy.deepcopy(templates.CONNECT_LMB_REQUEST)
    concerned_no = kwargs.get("concerned_no", {})

    request_payload['Details']['ContactData']['Attributes'].update({
        "concernedNumber": concerned_no
    })  
    
    lmbd_clnt_sg = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)
    logger.info(f"[[{lmb_functions.GET_ACTIVE_PRODUCTS_LAMBDA} request: {request_payload}]]")
    try:
        active_products_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.GET_ACTIVE_PRODUCTS_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        active_products_response = json.loads(active_products_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.GET_ACTIVE_PRODUCTS_LAMBDA} response: {active_products_response}]]")
        return active_products_response
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.GET_ACTIVE_PRODUCTS_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}

def search_order(**kwargs) -> dict:
    concerned_no = kwargs.get("concerned_no", {})
    
    request_payload = {
        "payload": {
            "SelectionCriteria": {
            "FilterCriteriaInfoList": {
                "FilterCriteria": [
                {
                    "FilterField": "AssignedProductServiceID",
                    "FilterValues": {
                    "FilterValue": concerned_no
                    }
                },
                {
                    "FilterField": "ActiveOrders",
                    "FilterValues": {
                    "FilterValue": "True"
                    }
                }
                ]
            }
            }
        }
    }
    
    lmbd_clnt_sg = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)
    logger.info(f"[[{lmb_functions.SEARCH_ORDER_API_LAMBDA}]] request: {request_payload}")
    try:
        search_order_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.SEARCH_ORDER_API_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        search_order_response = json.loads(search_order_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.SEARCH_ORDER_API_LAMBDA}]] response: {search_order_response}")
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.SEARCH_ORDER_API_LAMBDA} due to: {utils.get_exception_str(error)}")
    
    if not search_order_response.get("statusCode", 0) == 200:
        return {}
    
    return search_order_response.get("body", {}) if search_order_response["body"] else {}

def _retrieve_account_barring_info(**kwargs) -> dict:
    request_payload = copy.deepcopy(templates.CONNECT_LMB_REQUEST)
    request = kwargs.get("request", {})
    lob_name = request.get("lobName", "")
    landline = request.get("lastLandline","")
    account_num = request.get("lastAccountNumber","")
    msisdn = request.get("msisdn","")

    if lob_name == constants.BB_LOB_NAME:
        if not landline or landline == 'String':
            return False
        
        request_payload["Details"]["ContactData"]["CustomerEndpoint"].update({
            "Address": f"+63{landline}"
        })

        request_payload["Details"]["ContactData"]["Attributes"].update({
            "accountNumber": account_num
        })

        request_payload["Details"]["ContactData"]["Attributes"].update({
            "isBroadband": True
        })
    else: 
        if not msisdn or msisdn == 'String':
            return False

        request_payload["Details"]["ContactData"]["Attributes"].update({
            "concernedNumber": msisdn
        })
        
        request_payload["Details"]["ContactData"]["Attributes"].update({
            "accountNumber": account_num
        })
    
    lmbd_clnt_sg = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)
    logger.info(f"[[{lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA} request: {request_payload}]]")
    try:
        retrieve_accnt_barring_info_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        retrieve_accnt_barring_info_response = json.loads(retrieve_accnt_barring_info_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA} response: {retrieve_accnt_barring_info_response}]]")
        return retrieve_accnt_barring_info_response
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}
    

def check_kqi_whitelist(**kwargs) -> dict:
    request_payload = copy.deepcopy(templates.CONNECT_LMB_REQUEST)
    lmbd_clnt = boto3.client("lambda", region_name=configs.REGION_SYDNEY)

    account_no = kwargs.get("account_no", "")

    request_payload['Details']['ContactData']['Attributes'].update({
        "concernedAccountNumber": account_no
    })

    logger.info(f"[[{lmb_functions.CHECK_KQI_WHITELIST_LAMBDA}]] request: {request_payload}")

    try:
        check_kqi_whitelist_response = lmbd_clnt.invoke(FunctionName = lmb_functions.CHECK_KQI_WHITELIST_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        check_kqi_whitelist_response = json.loads(check_kqi_whitelist_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.CHECK_KQI_WHITELIST_LAMBDA}]] response: {check_kqi_whitelist_response}")
        return check_kqi_whitelist_response
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.CHECK_KQI_WHITELIST_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}
    

def get_fup_status(**kwargs) -> dict:
    request_payload = copy.deepcopy(templates.CONNECT_LMB_REQUEST)
    lmbd_clnt = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)

    landline = kwargs.get("landline", "")

    request_payload['Details']['ContactData']['Attributes'].update({
        "landline": landline
    })

    logger.info(f"[[{lmb_functions.GET_FUP_STATUS_LAMBDA}]] request: {request_payload}")

    try:
        get_fup_status_response = lmbd_clnt.invoke(FunctionName = lmb_functions.GET_FUP_STATUS_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        get_fup_status_response = json.loads(get_fup_status_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.GET_FUP_STATUS_LAMBDA}]] response: {get_fup_status_response}")
        return get_fup_status_response
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.GET_FUP_STATUS_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}
    

def bb_outage(**kwargs) -> dict:
    request_payload = copy.deepcopy(templates.CONNECT_LMB_REQUEST)
    lmbd_clnt = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)

    account_no = kwargs.get("account_no", "")

    request_payload['Details']['ContactData']['Attributes'].update({
        "accountNumber": account_no
    })

    logger.info(f"[[{lmb_functions.BROADBAND_OUTAGE_LAMBDA}]] request: {request_payload}")

    try:
        bb_outage_response = lmbd_clnt.invoke(FunctionName = lmb_functions.BROADBAND_OUTAGE_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        bb_outage_response = json.loads(bb_outage_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.BROADBAND_OUTAGE_LAMBDA}]] response: {bb_outage_response}")
        return bb_outage_response
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.BROADBAND_OUTAGE_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}
    

def get_bb_device_diagnostic_details(**kwargs) -> dict:

    lmbd_clnt = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)

    account_no = kwargs.get("account_no", "")
    request_payload = {
        "BroadbandAccountId": account_no
    }

    logger.info(f"[[{lmb_functions.GET_BB_DEVICE_DIAGNOSTIC_DETAILS_LAMBDA}]] request: {request_payload}")

    try:
        bb_device_diagnostic_details_reponse = lmbd_clnt.invoke(FunctionName = lmb_functions.GET_BB_DEVICE_DIAGNOSTIC_DETAILS_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        bb_device_diagnostic_details_reponse = json.loads(bb_device_diagnostic_details_reponse['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.GET_BB_DEVICE_DIAGNOSTIC_DETAILS_LAMBDA}]] response: {bb_device_diagnostic_details_reponse}")
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.GET_BB_DEVICE_DIAGNOSTIC_DETAILS_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}
    if bb_device_diagnostic_details_reponse and bb_device_diagnostic_details_reponse.get("statusCode", 0) == 200:
        return bb_device_diagnostic_details_reponse.get("body", {}) if bb_device_diagnostic_details_reponse.get("body") else {}
    else:
        return {}


def check_service_recovery_whitelist(**kwargs) -> dict:
    request_payload = copy.deepcopy(templates.CONNECT_LMB_REQUEST)
    lmbd_clnt = boto3.client("lambda", region_name=configs.REGION_SYDNEY)

    account_no = kwargs.get("account_no", "")

    request_payload['Details']['ContactData']['Attributes'].update({
        "concernedAccountNumber": account_no
    })

    logger.info(f"[[{lmb_functions.CHECK_SERVICE_RECOVERY_WHITELIST_LAMBDA}]] request: {request_payload}")

    try:
        check_service_recovery_whitelist_response = lmbd_clnt.invoke(FunctionName = lmb_functions.CHECK_SERVICE_RECOVERY_WHITELIST_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        check_service_recovery_whitelist_response = json.loads(check_service_recovery_whitelist_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.CHECK_SERVICE_RECOVERY_WHITELIST_LAMBDA}]] response: {check_service_recovery_whitelist_response}")
        return check_service_recovery_whitelist_response
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.CHECK_SERVICE_RECOVERY_WHITELIST_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}


def retrieve_account_barring_info(**kwargs) -> dict:
    request_payload = copy.deepcopy(templates.CONNECT_LMB_REQUEST)
    lmbd_clnt = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)

    brand_type = kwargs.get("brand_type", "")
    account_no = kwargs.get("account_no", "")
    msisdn = formatter_utils.to_13_digits_ph_mobile_no(kwargs.get("msisdn",""))
    landline = kwargs.get("landline", "")

    if(brand_type == "wireline"):
        request_payload['Details']['ContactData']['Attributes'].update({
            "accountNumber": account_no,
            "isBroadband": True
        })
        request_payload["Details"]["ContactData"]["CustomerEndpoint"].update({
            "Address": f"+63{landline}"
        })
    else:
        request_payload["Details"]["ContactData"]["Attributes"].update({
            "concernedNumber": msisdn,
            "accountNumber": account_no,
        })

    logger.info(f"[[{lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA}]] request: {request_payload}")

    try:
        retrieve_account_barring_info_response = lmbd_clnt.invoke(FunctionName = lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        retrieve_account_barring_info_response = json.loads(retrieve_account_barring_info_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA}]] response: {retrieve_account_barring_info_response}")
        return retrieve_account_barring_info_response
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}
    

def check_onsite_visit(**kwargs) -> dict:
    request_payload = copy.deepcopy(templates.CONNECT_LMB_REQUEST)
    lmbd_clnt = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)

    account_no = kwargs.get("account_no", "")

    request_payload['Details']['ContactData']['Attributes'].update({
        "concernedAccountNumber": account_no,
    })

    logger.info(f"[[{lmb_functions.CHECK_ONSITE_VISIT_LAMBDA}]] request: {request_payload}")

    try:
        check_onsite_visit_response = lmbd_clnt.invoke(FunctionName = lmb_functions.CHECK_ONSITE_VISIT_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        check_onsite_visit_response = json.loads(check_onsite_visit_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.CHECK_ONSITE_VISIT_LAMBDA}]] response: {check_onsite_visit_response}")
        return check_onsite_visit_response
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.CHECK_ONSITE_VISIT_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}
    

def get_outstanding_balance_by_account_id_api(**kwargs) -> dict:
    lmbd_clnt = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)
    account_no = kwargs.get("account_no", "")

    request_payload = {
        "accountNo": account_no,
    }

    logger.info(f"[[{lmb_functions.GET_OUTSTANDING_BALANCE_BY_ACCOUNT_ID_API}]] request: {request_payload}")

    try:
        get_outstanding_balance_by_account_id_api_response = lmbd_clnt.invoke(FunctionName = lmb_functions.GET_OUTSTANDING_BALANCE_BY_ACCOUNT_ID_API, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        get_outstanding_balance_by_account_id_api_response = json.loads(get_outstanding_balance_by_account_id_api_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.GET_OUTSTANDING_BALANCE_BY_ACCOUNT_ID_API}]] response: {get_outstanding_balance_by_account_id_api_response}")
        return get_outstanding_balance_by_account_id_api_response
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.GET_OUTSTANDING_BALANCE_BY_ACCOUNT_ID_API} due to: {utils.get_exception_str(error)}")
        return {}
    

def get_outstanding_balance_by_msisdn_api(**kwargs) -> dict:
    lmbd_clnt = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)
    msisdn = kwargs.get("msisdn", "")

    request_payload = copy.deepcopy(templates.CONNECT_LMB_REQUEST)

    request_payload['Details']['Parameters'].update({
        "concernedNumber": f"+63{msisdn}"
    })

    logger.info(f"[[{lmb_functions.GET_OUTSTANDING_BALANCE_BY_MSISDN_LAMBDA}]] request: {request_payload}")

    try:
        get_outstanding_balance_by_msisdn_api_response = lmbd_clnt.invoke(FunctionName = lmb_functions.GET_OUTSTANDING_BALANCE_BY_MSISDN_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        get_outstanding_balance_by_msisdn_api_response = json.loads(get_outstanding_balance_by_msisdn_api_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.GET_OUTSTANDING_BALANCE_BY_MSISDN_LAMBDA}]] response: {get_outstanding_balance_by_msisdn_api_response}")
        return get_outstanding_balance_by_msisdn_api_response
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.GET_OUTSTANDING_BALANCE_BY_MSISDN_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}
    

def retrieve_subscriber_details_by_msisdn_api(**kwargs) -> dict:
    lmbd_clnt = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)
    msisdn = kwargs.get("msisdn", "")
    
    request_payload = copy.deepcopy(templates.CONNECT_LMB_REQUEST)

    request_payload['Details']['Parameters'].update({
        "payload": {
            "MSISDN": f"{msisdn}"
        }
    })

    logger.info(f"[[{lmb_functions.FRAUD_TAGGING_API_LAMBDA}]] request: {request_payload}")

    try:
        retrieve_subscriber_details_by_msisdn_api_response = lmbd_clnt.invoke(FunctionName = lmb_functions.FRAUD_TAGGING_API_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        retrieve_subscriber_details_by_msisdn_api_response = json.loads(retrieve_subscriber_details_by_msisdn_api_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.FRAUD_TAGGING_API_LAMBDA}]] response: {retrieve_subscriber_details_by_msisdn_api_response}")
        return retrieve_subscriber_details_by_msisdn_api_response
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.FRAUD_TAGGING_API_LAMBDA} due to: {utils.get_exception_str(error)}")
    
    if not retrieve_subscriber_details_by_msisdn_api_response.get("statusCode", 0) == 200:
        return {}
    
    return retrieve_subscriber_details_by_msisdn_api_response.get("body", {}) if retrieve_subscriber_details_by_msisdn_api_response["body"] else {}


def send_email(**kwargs) -> bool:
    lmbd_clnt_sg = boto3.client("lambda", region_name=configs.REGION_OREGON)
    email_type = kwargs.get("email_type", "")
    attributes = kwargs.get("attributes", {})
    
    request_payload = {
        "emailType": email_type,
        **attributes
    }
    
    logger.info(f"[[{lmb_functions.SEND_EMAIL}]] request: {request_payload}")
    try:
        send_email_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.SEND_EMAIL, InvocationType="Event", Payload=json.dumps(request_payload))
        logger.info(f"[[{lmb_functions.SEND_EMAIL}]] response: {send_email_response}")
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.SEND_EMAIL} due to: {utils.get_exception_str(error)}")
        return False
    
    return True


def search_appointment_slot(**kwargs) -> dict:
    lmbd_clnt_sg = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)

    account_no = kwargs.get("account_no", "")
    landline = kwargs.get("landline", "")
    case_id = kwargs.get("case_id", "")
    case_type_1 = kwargs.get("caseTypeLevel1", "")
    case_type_2 = kwargs.get("caseTypeLevel2", "")
    case_type_3 = kwargs.get("caseTypeLevel3", "")
    case_type_4 = kwargs.get("caseTypeLevel4", "")
    case_type_5 = kwargs.get("caseTypeLevel5", "")
    concern = kwargs.get("concern", "")
    mobile = kwargs.get("mobile", "")
    alt_mobile_no = kwargs.get("altContactNo", "")
    account_status = kwargs.get("acoountStatus", "")
    outage_result = kwargs.get("outageResult", "")
    fup_indicator = kwargs.get("fupIndicator", "")
    line_status = kwargs.get("lineStatus", "")
    modem_status = kwargs.get("modemStatus", "")
    billing_offer_name = kwargs.get("billingOfferName", "")

    request_payload = {
        "Details": {
            "Parameters": {
                "prefferedDayPeriod": "ALL",
                "accountNo": account_no,
                "landline": landline,
                "caseId": case_id,
                "caseTypeLevel1": case_type_1,
                "caseTypeLevel2": case_type_2,
                "caseTypeLevel3": case_type_3,
                "caseTypeLevel4": case_type_4,
                "caseTypeLevel5": case_type_5,
                "concern": concern,
                "mobile": mobile,
                "alternativeMobileNumber": alt_mobile_no,
                "channel": str_const.LEX,
                "accountStatus": account_status,
                "outageResult": outage_result,
                "fupIndicator": fup_indicator,
                "lineStatus": line_status,
                "modemStatus": modem_status,
                "billingOfferName": billing_offer_name
            }
        }
    } 

    logger.info(f"[[{lmb_functions.SEARCH_APPOINTMENT_SLOT_LAMBDA}]] request: {request_payload}")

    try:
        search_appointment_slot_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.SEARCH_APPOINTMENT_SLOT_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        search_appointment_slot_response = json.loads(search_appointment_slot_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.SEARCH_APPOINTMENT_SLOT_LAMBDA}]] response: {search_appointment_slot_response}")
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.SEARCH_APPOINTMENT_SLOT_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}
    
    if search_appointment_slot_response and search_appointment_slot_response.get("statusCode", 0) == 200:
        return search_appointment_slot_response.get("body", {}) if search_appointment_slot_response.get("body") else {}
    else:
        return {}
    

def confirm_appointment_slot_api(**kwargs) -> dict:
    lmbd_clnt_sg = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)

    account_no = kwargs.get("account_no", "")
    order_number = kwargs.get("order_number", "")
    appointment_date = kwargs.get("appointment_date", "")
    appointment_slot = kwargs.get("appointment_slot", "")
   
    # Old Payload
    request_payload = {
        "payload": {
            "orderNumber": order_number,
            "preferedAppointmentSlot": {
                "date": appointment_date,
                "slot": appointment_slot
            }   
        }
    } 

    # New Payload
    # request_payload = {
    #     "payload": {
    #         "accountId": account_no,
    #         "channel": "GBP",
    #         "orderId": order_number + "-1",
    #         "orderActionId": order_number,
    #         "targetType": "2",
    #         "notes": "",
    #         "preferredAppointmentSlot": {
    #             "date": appointment_date,
    #             "slot": appointment_slot
    #         },
    #         "accountNumber": account_no
    #     }
    # }

    logger.info(f"[[{lmb_functions.CONFIRM_APPOINTMENT_SLOT_API_LAMBDA}]] request: {request_payload}")

    try:
        confirm_appointment_slot_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.CONFIRM_APPOINTMENT_SLOT_API_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        confirm_appointment_slot_response = json.loads(confirm_appointment_slot_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.CONFIRM_APPOINTMENT_SLOT_API_LAMBDA}]] response: {confirm_appointment_slot_response}")
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.CONFIRM_APPOINTMENT_SLOT_API_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}
    
    if confirm_appointment_slot_response and confirm_appointment_slot_response.get("statusCode", 0) == 200:
        return confirm_appointment_slot_response.get("body", {}) if confirm_appointment_slot_response.get("body") else {}
    else:
        return {}
    
def update_case_details_api(**kwargs) -> dict:
    lmbd_clnt_sg = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)

    flex_attrs = kwargs.get("flex_attrs", {})

    KEY_MAPPING = {
        "case_id": "CaseId",
        "flex_attrs": "FlexibleAttributes",
        "case_notes": "Note",
        "queue": "QueueId",
        "case_status": "CaseStatus" #Solving
    }

    request_payload = {
        "payload": {
            KEY_MAPPING[key]: value for key, value in ((key, kwargs.get(key, "")) for key in KEY_MAPPING) if value
        }
    }

    if flex_attrs:
        request_payload["payload"]["FlexibleAttributes"] = [{"FlexibleAttribute":{"Name": item["name"], "Value": item["value"]}} for item in flex_attrs]

    key_sequence = ["CaseId", "FlexibleAttributes", "CaseStatus", "Note", "QueueId"]
    request_payload["payload"] = utils.arrange_dict_keys(request_payload["payload"], key_sequence)

    logger.info(f"[[{lmb_functions.UPDATE_CASE_DETAILS_API}]] request: {request_payload}")

    try:
        update_case_details_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.UPDATE_CASE_DETAILS_API, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        update_case_details_response = json.loads(update_case_details_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.UPDATE_CASE_DETAILS_API}]] response: {update_case_details_response}")
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.UPDATE_CASE_DETAILS_API} due to: {utils.get_exception_str(error)}")
        return {}
    
    if update_case_details_response and update_case_details_response.get("statusCode", 0) == 200:
        return update_case_details_response.get("body", {}) if update_case_details_response.get("body") else {}
    else:
        return {}


def get_overdue_balance_by_msisdn_api(**kwargs) -> dict:
    lmbd_clnt_sg = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)

    msisdn = kwargs.get("msisdn", "")
    request_payload = {
        "msisdn": msisdn
    } 

    logger.info(f"[[{lmb_functions.GET_RECON_OUTSTANDING_BALANCE_BY_MSISDN_LAMBDA}]] request: {request_payload}")

    try:
        get_overdue_balance_by_msisdn_api_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.GET_RECON_OUTSTANDING_BALANCE_BY_MSISDN_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        get_overdue_balance_by_msisdn_api_response = json.loads(get_overdue_balance_by_msisdn_api_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.GET_RECON_OUTSTANDING_BALANCE_BY_MSISDN_LAMBDA}]] response: {get_overdue_balance_by_msisdn_api_response}")
        
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.GET_RECON_OUTSTANDING_BALANCE_BY_MSISDN_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}
    
    return get_overdue_balance_by_msisdn_api_response


def get_overdue_balance_by_accountId_api(**kwargs) -> dict:
    lmbd_clnt_sg = boto3.client("lambda", region_name=configs.REGION_SINGAPORE)

    accountId = kwargs.get("accountId", "")
    request_payload =  {
        "accountId": accountId
    }

    logger.info(f"[[{lmb_functions.GET_RECON_OUTSTANDING_BALANCE_BY_ACCT_ID_LAMBDA}]] request: {request_payload}")

    try:
        get_overdue_balance_by_accountId_api_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.GET_RECON_OUTSTANDING_BALANCE_BY_ACCT_ID_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(request_payload))
        get_overdue_balance_by_accountId_api_response = json.loads(get_overdue_balance_by_accountId_api_response['Payload'].read().decode())
        logger.info(f"[[{lmb_functions.GET_RECON_OUTSTANDING_BALANCE_BY_ACCT_ID_LAMBDA}]] response: {get_overdue_balance_by_accountId_api_response}")
        
    except Exception as error:
        logger.error(f"Failed to invoke: {lmb_functions.GET_RECON_OUTSTANDING_BALANCE_BY_ACCT_ID_LAMBDA} due to: {utils.get_exception_str(error)}")
        return {}
    
    return get_overdue_balance_by_accountId_api_response