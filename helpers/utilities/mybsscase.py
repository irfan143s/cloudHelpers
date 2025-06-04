# NIAS 2.0 - HISAMS - 2022-04-06
from __future__ import annotations

import copy
import json
import boto3
import logging

from dateutil import tz
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import Key, Attr

import resources.constants as constants
import resources.aws_lambda as lmb_functions
import resources.tableattributes as tableattributes

from helpers import utils

import configuration as config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

db_obejects = {
    "caseCreated": {
        "db_connector": None,
        "tbl_connector": None
    }
}
request = {
    "Details": {
        "ContactData": {
            "Attributes": {
            },
            "CustomerEndpoint": {
                "Address": ""
            }
        },
        "Parameters": {
        }
    },
    "Name": "Lex"
}

def __query_case_records(query_kwargs: dict) -> dict:
    if not db_obejects["caseCreated"]["db_connector"]:
        db_obejects["caseCreated"]["db_connector"] = boto3.resource("dynamodb", region_name=config.REGION_SINGAPORE)

    if not db_obejects["caseCreated"]["tbl_connector"]:
        db_obejects["caseCreated"]["tbl_connector"] = db_obejects["caseCreated"]["db_connector"].Table(config.DDB_CASE_CREATED)

    tbl_connector = db_obejects["caseCreated"]["tbl_connector"]

    try:
        data = tbl_connector.query(**query_kwargs)
        return data
    except Exception as error:
        logger.info(f'Error querying cases: {error}')
        return { "Items": [] }


def is_subscriber_has_failed_case_created_by_msisdn(**kwargs) -> bool:
    msisdn = kwargs.get("msisdn", "")
    time_range = kwargs.get("time_range", "")
    case_titles = kwargs.get("case_titles", [])
    now = datetime.now(tz = tz.gettz(config.TIMEZONE_PH))

    if not msisdn:
        logger.error("msisdn is required.")
        return False
    
    if not isinstance(case_titles, list):
        logger.error("Invalid case_titles value. Should be a list.")
        return False

    if time_range.lower() == "today":
        from_date = datetime(now.year, now.month, now.day, 0, 0, 0, 1)
        to_date = datetime(now.year, now.month, now.day, 23, 59, 59, 999999)
    else:
        from_date = now - timedelta(days = 1)
        to_date = now
    
    query_kwargs = {
        'KeyConditionExpression': Key("SubscriberNumber").eq(utils.get_10_digit_mobile_number(msisdn)),
        'IndexName': "SubscriberNumber-index",
        'FilterExpression': Attr('Status').eq('Failed') & Attr('DateOfRequest').between(from_date.isoformat(), to_date.isoformat())
    }

    if case_titles:
        query_kwargs["FilterExpression"] = query_kwargs["FilterExpression"] & Attr('Title').is_in(case_titles)

    logger.info(f"Query param => range: {from_date.isoformat()} to {to_date.isoformat()}, case_titles: {case_titles}")
 
    while True:
        query_result = __query_case_records(query_kwargs)
        logger.info(f'Query Result: {query_result}')

        if len(query_result["Items"]):
            return True
        
        if "LastEvaluatedKey" in query_result.keys():
            query_kwargs["ExclusiveStartKey"] = query_result["LastEvaluatedKey"]
        else:
            return False

        
def get_latest_case_id(msisdn= "",landline="",account_number ="",bss_contact_id=""):
    lmbd_clnt_singapore = boto3.client("lambda", region_name = config.REGION_SINGAPORE)
    if bss_contact_id.strip():
        request["Details"]["ContactData"]["Attributes"]["bssContactId"] = bss_contact_id
    if msisdn.strip(): 
        request["Details"]["ContactData"]["Attributes"]["concernedNumber"] = "+63"+msisdn
    elif account_number.strip() and landline.strip():
        request["Details"]["ContactData"]["Attributes"]["concernedAccountNumber"] = account_number
        request["Details"]["ContactData"]["Attributes"]["landline"] = landline
    else:
        logger.info("No msisdn/landlineNumber detected in payload")
        return False
        
    request["Details"]["Parameters"]["caseStatusFlag"] =  "lex-open"
    
    try:
        connect_response = lmbd_clnt_singapore.invoke(FunctionName = lmb_functions.GET_CASE_DETAILS_LAMBDA, InvocationType = "RequestResponse", Payload = json.dumps(request))
        connect_response = json.loads(connect_response['Payload'].read().decode())
    except Exception as error:
        logger.info(f"Error invoking {lmb_functions.GET_CASE_DETAILS_LAMBDA}: {str(error)}")
        return False
    
    if "CaseId" in connect_response:
        case_id = connect_response["CaseId"] if 'CaseId' in connect_response else ''
        if case_id != '':
            logger.info("Case found.")
            return case_id      
        else:
            logger.info(connect_response)
            return False
    else:
        logger.info(connect_response)
        return False
    

def is_case_id_in_open_case_list(case_id,type,brand):
    lmbd_clnt_singapore = boto3.client("lambda", region_name = config.REGION_SINGAPORE)
    
    request["Details"]["ContactData"]["Attributes"]["lobName"] = brand
    request["Details"]["Parameters"]["CaseId"] =  case_id
    request["Details"]["Parameters"]["channel"] =  "lex"
    request["Details"]["Parameters"]["type"] = type

    try:
        connect_response = lmbd_clnt_singapore.invoke(FunctionName = lmb_functions.CHECK_OPEN_CASE_DETAILS_LAMBDA, InvocationType = "RequestResponse", Payload = json.dumps(request))
        connect_response = json.loads(connect_response['Payload'].read().decode())
    except Exception as error:
        logger.info(f"Error invoking {lmb_functions.CHECK_OPEN_CASE_DETAILS_LAMBDA}: {str(error)}")
        return False
        
    if "openCaseStatus" in connect_response:    
        if connect_response["openCaseStatus"] == "true" :
            return True
        else:
            logger.info('latest case is not related')
            return False
    else:
        logger.info('latest case is not related')
        return False


def get_open_case_details(request: dict) -> dict:
    lmbd_clnt_sg = boto3.client("lambda", region_name = config.REGION_SINGAPORE)
    case_dtls = {
        "hasOpenCaseWithinThreeDays": False,
        "hasOpenCaseBeyondThreeDays": False,
        "hasOpenCase": False
    }

    bss_contact_id = request[tableattributes.LAST_BSS_CONTACT_ID]
    account_no = request[tableattributes.LAST_ACCOUNT_NUMBER]
    landline = request[tableattributes.LAST_LANDLINE]
    last_number = request[tableattributes.LAST_NUMBER]
    last_brand = request[tableattributes.LAST_BRAND]

    get_case_dtls_req = copy.deepcopy(constants.CONNECT_LMB_REQUEST)
    get_case_dtls_req["Details"]["Parameters"].update({
        "caseStatusFlag": "open"
    })

    if last_brand == constants.BB_LOB_NAME:
        get_case_dtls_req["Details"]["ContactData"]["Attributes"].update({
            "concernedAccountNumber": account_no,
            "landline": "+63" + landline,
            "bssContactId": bss_contact_id,
            "concernedNumber": 'NA',
            "msisdn": 'NA'
        })
    else:
        get_case_dtls_req["Details"]["ContactData"]["Attributes"].update({
            "concernedNumber": utils.get_13_digit_mobile_number(last_number),
            "bssContactId": bss_contact_id
        })

    try:
        logger.info(f"Request[{lmb_functions.GET_CASE_DETAILS_LAMBDA}]: {get_case_dtls_req}")
        get_case_dtls_res = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.GET_CASE_DETAILS_LAMBDA, InvocationType = "RequestResponse", Payload = json.dumps(get_case_dtls_req))
        get_case_dtls_res = json.loads(get_case_dtls_res['Payload'].read().decode())
        logger.info(f"Response[{lmb_functions.GET_CASE_DETAILS_LAMBDA}]: {get_case_dtls_res}")
    except Exception as err:
        logger.info(f"Error invoking {lmb_functions.GET_CASE_DETAILS_LAMBDA}: {utils.get_exception_str(err)}")
        return case_dtls
    
    if get_case_dtls_res.get("CaseId", []):
        case_dtls["hasOpenCaseWithinThreeDays"] = True
        case_dtls["hasOpenCase"] = True
        case_dtls["caseDetails"] = get_case_dtls_res["caseDetails"]
    elif "hasOpenCaseBeyondThreeDays" in get_case_dtls_res.keys() and get_case_dtls_res["hasOpenCaseBeyondThreeDays"].lower() == "true":
        case_dtls["hasOpenCaseBeyondThreeDays"] = True
        case_dtls["hasOpenCase"] = True
        case_dtls["caseDetails"] = get_case_dtls_res["caseDetails"]
    return case_dtls

def subscriber_mybss_case_info(msisdn = "",landline = "",info_type = "",titles = [],case_types = [],channel = "fbm"):
    lmbd_clnt_singapore = boto3.client("lambda", region_name = config.REGION_SINGAPORE)
    
    case_info_request = copy.deepcopy(constants.CONNECT_LMB_REQUEST)

    case_info_request["Details"]["Parameters"]["infoType"] = info_type
    if landline != "":
        case_info_request["Details"]["Parameters"]["landline"] = landline
    else:
        case_info_request["Details"]["Parameters"]["msisdn"] = msisdn
        
    case_info_request["Details"]["Parameters"]["titles"] =  titles
    case_info_request["Details"]["Parameters"]["caseTypes"] =  case_types
    case_info_request["Details"]["Parameters"]["channel"] = channel

    failed_response = {
        'hasCaseInfo': 'false',
        'hasOpenCase': 'false',
        'hasClosedCase': 'false'
    }

    logger.info(f"[[{lmb_functions.SUBSCRIBER_MYBSS_CASE_INFO_LAMBDA}]] request: {case_info_request}")

    try:
        connect_response = lmbd_clnt_singapore.invoke(FunctionName = lmb_functions.SUBSCRIBER_MYBSS_CASE_INFO_LAMBDA, InvocationType = "RequestResponse", Payload = json.dumps(case_info_request))
        connect_response = json.loads(connect_response['Payload'].read().decode())
    except Exception as error:
        logger.info(f"Error invoking {lmb_functions.SUBSCRIBER_MYBSS_CASE_INFO_LAMBDA}: {str(error)}")
        return failed_response


    if "hasCaseInfo" in connect_response:    
        logger.info(f'subscriber_mybss_case_info -> {connect_response}')
        return connect_response

    return failed_response