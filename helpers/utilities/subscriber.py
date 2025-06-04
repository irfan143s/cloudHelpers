import copy
import json
import boto3
import logging

import helpers.utils as utils
import helpers.tools as tools
import helpers.utilities.mybsscase as mybsscase_utils
import helpers.whitelistchecker as whitelist_utils
import helpers.common.utils.api as api

from helpers.sessiontools import SessionTools
from helpers.subscribertools import SubscriberTools
from helpers.ddbtools import DDBTools
from datetime import date, datetime, timedelta, timezone

import resources.aws_lambda as lmb_functions
import resources.constants as constants
import resources.casetype_duplicity as case_type

import configuration as configs

logger = logging.getLogger()
logger.setLevel(logging.INFO)


"""
    Getting the subscriber details from MainConnect using both MSISDN and ACCOUNTNUMBER
"""
def get_concern_no_subscriber_details(concern_no):

    inputted_num = concern_no.replace(" ","").strip()
    validated_num = tools.number_regex_validator(inputted_num)

    logger.info(f"Validated number result: {validated_num}")

    if not validated_num:
        subscriber = SubscriberTools("ACCOUNTNUMBER", inputted_num)
        if not subscriber.is_subscriber_exists():
            return subscriber
    else:
        subscriber = SubscriberTools("MSISDN", utils.format_concern_number(validated_num))
        if not subscriber.is_subscriber_exists():
            subscriber =  SubscriberTools("ACCOUNTNUMBER", inputted_num)
            if not subscriber.is_subscriber_exists():
                return subscriber

    return subscriber


def is_mybss_broadband_account(request, session_tools):
    landline = session_tools.get_last_landline()

    if not landline or landline.strip().lower() == "string":
        return False

    lmbd_clnt_sg = boto3.client("lambda", region_name = configs.REGION_SINGAPORE)
    retrieve_accnt_barring_info_req = copy.deepcopy(constants.CONNECT_LMB_REQUEST)
    retrieve_accnt_barring_info_req["Details"]["ContactData"]["CustomerEndpoint"].update({
        "Address": f"+63{landline}"
    })

    try:
        logger.info(f" Request[{lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA}]: {retrieve_accnt_barring_info_req}")
        retrieve_accnt_barring_info_res = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA, InvocationType = "RequestResponse", Payload = json.dumps(retrieve_accnt_barring_info_req))
        retrieve_accnt_barring_info_res = json.loads(retrieve_accnt_barring_info_res['Payload'].read().decode())
        logger.info(f"Response[{lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA}]: {retrieve_accnt_barring_info_res}")
    except Exception as err:
        logger.info(f"Error invoking {lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA}: {utils.get_exception_str(err)}")
        return False

    barr_ind = retrieve_accnt_barring_info_res['BarringIndicator'] if 'BarringIndicator' in retrieve_accnt_barring_info_res else ''

    if str(barr_ind) not in ['Y','N']:
        return False

    return True

def is_disconnected(request):
    landline = request.get("lastLandline","")
    lob_name = request.get("lobName","")
    msisdn = request.get("msisdn","")
    account_num = request.get("lastAccountNumber","")

    if not lob_name or lob_name == "String":
        return False

    lmbd_clnt_sg = boto3.client("lambda", region_name = configs.REGION_SINGAPORE)
    retrieve_accnt_barring_info_req = copy.deepcopy(constants.CONNECT_LMB_REQUEST)
    
    if lob_name == constants.BB_LOB_NAME:
        if not landline or landline == 'String':
            return False
        
        retrieve_accnt_barring_info_req["Details"]["ContactData"]["CustomerEndpoint"].update({
            "Address": f"+63{landline}"
        })

        retrieve_accnt_barring_info_req["Details"]["ContactData"]["Attributes"].update({
            "accountNumber": account_num
        })

        retrieve_accnt_barring_info_req["Details"]["ContactData"]["Attributes"].update({
            "isBroadband": True
        })
    else: 
        if not msisdn or msisdn == 'String':
            return False

        retrieve_accnt_barring_info_req["Details"]["ContactData"]["Attributes"].update({
            "concernedNumber": msisdn
        })
        
        retrieve_accnt_barring_info_req["Details"]["ContactData"]["Attributes"].update({
            "accountNumber": account_num
        })
    
    try:
        logger.info(f" Request[{lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA}]: {retrieve_accnt_barring_info_req}")
        retrieve_accnt_barring_info_res = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA, InvocationType = "RequestResponse", Payload = json.dumps(retrieve_accnt_barring_info_req))
        retrieve_accnt_barring_info_res = json.loads(retrieve_accnt_barring_info_res['Payload'].read().decode())
        logger.info(f"Response[{lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA}]: {retrieve_accnt_barring_info_res}")
    except Exception as err:
        logger.info(f"Error invoking {lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA}: {utils.get_exception_str(err)}")
        return False

    barr_ind = retrieve_accnt_barring_info_res['BarringIndicator'] if 'BarringIndicator' in retrieve_accnt_barring_info_res else ''
    barr_type = retrieve_accnt_barring_info_res['BarringType'] if 'BarringType' in retrieve_accnt_barring_info_res else ''

    if str(barr_ind) == 'Y' and barr_type in ['SL','CL']:
        return True
    elif str(barr_ind) == 'N':
        return False
    else:
        if lob_name == constants.BB_LOB_NAME:
            #ICCBS
            if not account_num or account_num == "String":
                return False
            get_customer_profile_info_req = copy.deepcopy(constants.CONNECT_LMB_REQUEST)
            get_customer_profile_info_req["Details"]["ContactData"]["Attributes"].update({
                "concernedAccountNumber": account_num
            })
            get_customer_profile_info_req["Details"]["ContactData"]["CustomerEndpoint"].update({
            "Address": f"+63{landline}"
            })

            try:
                logger.info(f" Request[{lmb_functions.GET_CUSTOMER_PROFILE_INFO_LAMBDA}]: {get_customer_profile_info_req}")
                get_customer_profile_info_res = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.GET_CUSTOMER_PROFILE_INFO_LAMBDA, InvocationType = "RequestResponse", Payload = json.dumps(get_customer_profile_info_req))
                get_customer_profile_info_res = json.loads(get_customer_profile_info_res['Payload'].read().decode())
                logger.info(f"Response[{lmb_functions.GET_CUSTOMER_PROFILE_INFO_LAMBDA}]: {get_customer_profile_info_res}")
            except Exception as err:
                logger.info(f"Error invoking {lmb_functions.GET_CUSTOMER_PROFILE_INFO_LAMBDA}: {utils.get_exception_str(err)}")
                return False
            
            barr_ind_iccbs = get_customer_profile_info_res['TDIndicator'] if 'TDIndicator' in get_customer_profile_info_res else ''

            if str(barr_ind_iccbs) == 'Y':
                return True
            else:
                return False
        else:
            return False

def is_valid_for_immediate_reversal(**kwargs):
        
    msisdn = kwargs.get('msisdn', '')
    amount = kwargs.get('amount', '')
    handlerId = kwargs.get('handlerId', '')
    requestReason = kwargs.get('requestReason', '')
    purchaseChannel = kwargs.get('purchaseChannel', '')
    amount_limit = 30

    if int(amount) < amount_limit:

        if whitelist_utils.is_lpr_first_timer_whitelisted(msisdn):

            logger.info(f"is_valid_for_immediate_reversal -> False")
            return False

        else:
            mybss_case_info = mybsscase_utils.subscriber_mybss_case_info(
                msisdn = msisdn, 
                info_type = "latest-case-with-casetypes", 
                case_types = case_type.CASE_TYPE_LEVEL_MAPPING['load-promos-rewards'],
                channel = "fbm-lpr"
            )
            if 'hasCaseInfo' in mybss_case_info and mybss_case_info['hasCaseInfo'] == 'true':

                logger.info(f"is_valid_for_immediate_reversal -> False")
                return False

            else:

                ddb_lpr_first_timer_whitelist = DDBTools(configs.DDB_LPR_FIRST_TIMER_WHITELIST, configs.REGION_SYDNEY)
                date_today = datetime.now() + timedelta(hours=8)
                item = {
                    'wallet_id': 'GT1920974',
                    'handler_id': handlerId,
                    'request_reason': requestReason,
                    'purchase_channel': purchaseChannel,
                    'product_type': '1',
                    'product': 'M',
                    'amount': amount,
                    'transaction_date': datetime.strftime(date_today, '%Y-%m-%dT%H:%M:%S.000Z'),
                    'expiry_timestamp': utils.modify_epoch_time("ADD", "DAYS", 365, utils.get_current_epoch_time()),
                    'index_status': 'SUCCESS'
                }
                    
                ddb_lpr_first_timer_whitelist.update_item('msisdn', msisdn, item)
                logger.info(f"is_valid_for_immediate_reversal -> True")
                return True
    
    else:
        logger.info(f"is_valid_for_immediate_reversal -> False")
        return False
    
    
def is_prepaid_fiber(**kwargs):
    msisdn = kwargs.get('msisdn', '')

    lmbd_clnt_sg = boto3.client("lambda", region_name = configs.REGION_SINGAPORE)
    prepaid_fiber_request = copy.deepcopy(constants.CONNECT_LMB_REQUEST)
    prepaid_fiber_request["Details"]["Parameters"]["msisdn"] = msisdn
    prepaid_fiber_request["Details"]["Parameters"]["apiName"] = "PrepaidFiber"

    logger.info(f"--------------{lmb_functions.PREPAID_FIBER_LAMBDA}--------------")
    try:
        logger.info(f" Request[{lmb_functions.PREPAID_FIBER_LAMBDA}]: {prepaid_fiber_request}")
        prepaid_fiber_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.PREPAID_FIBER_LAMBDA, InvocationType = "RequestResponse", Payload = json.dumps(prepaid_fiber_request))
        prepaid_fiber_response = json.loads(prepaid_fiber_response['Payload'].read().decode())
        logger.info(f"Response[{lmb_functions.PREPAID_FIBER_LAMBDA}]: {prepaid_fiber_response}")
    except Exception as err:
        logger.info(f"Error invoking {lmb_functions.PREPAID_FIBER_LAMBDA}: {utils.get_exception_str(err)}")
        return False

    if prepaid_fiber_response and prepaid_fiber_response['statusCode'] == 200:
        if 'data' in prepaid_fiber_response.keys():
            data = prepaid_fiber_response['data']
            if data['exists'] == True and data['code'] == 0 and data['module'] == "USER" :
                logger.info(f"{msisdn} ->: is_prepaid_fiber")
                return True
        return False

    return False


def is_mybss_account(**kwargs):
    account_no = kwargs.get('account_no', '')
    brand_type = kwargs.get('brand_type', '')
    service_id = kwargs.get('service_id', 'NA')
    
    connect_request = {
        "Details": {
            "ContactData": {
                "Attributes": {
                    "concernedNumber": f"+63{service_id}",
                    "concernedAccountNumber": account_no,
                }
            },
            "Parameters":{}
        }
    }

    if brand_type == "wireline":
        connect_request["Details"]["ContactData"]["Attributes"]["isBroadband"] = "true"

    lmbd_clnt_sg = boto3.client("lambda", region_name = configs.REGION_SINGAPORE)
        
    try:
        logger.info(f" Request[{lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA}]: {connect_request}")
        connect_response = lmbd_clnt_sg.invoke(FunctionName = lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA, InvocationType = "RequestResponse", Payload = json.dumps(connect_request))
        connect_response = json.loads(connect_response['Payload'].read().decode())
        logger.info(f"Response[{lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA}]: {connect_response}")
    except Exception as err:
        logger.info(f"Error invoking {lmb_functions.RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA}: {utils.get_exception_str(err)}")
        return False

    barr_ind = connect_response['BarringIndicator'] if 'BarringIndicator' in connect_response else ''

    if barr_ind not in ['Y','N']:
        return False

    return True

def is_temporarily_disconnected(**kwargs):
    account_no = kwargs.get("account_no", {})
    brand_type = kwargs.get("brand_type", "")
    customer_info_response = api.get_customer_info_api(account_no=account_no)

    if brand_type == 'wireline':
        if customer_info_response.get('SubscriberStatus') in ["83", "85", "68"]:
            return True
        else:
            return False
    else:
        if customer_info_response.get('SubscriberStatus') == '85':
            return True
        else:
            return False
    
def is_permanently_disconnected(**kwargs):
    account_no = kwargs.get("account_no", {})

    customer_info_response = api.get_customer_info_api(account_no=account_no)

    if customer_info_response.get('SubscriberStatus') in ["67", "76", "84"]:
        return True
    else:
        return False
    
def get_open_order(**kwargs):
    concerned_no = kwargs.get("concerned_no", "")

    search_order_response = api.search_order(concerned_no=concerned_no)

    if search_order_response.get("SearchOrderResult", {}).get("SearchResults", {}):
        # Has an open order
        return True
    else:
        return False
    

def is_within_lockup_period(**kwargs):
    concerned_no = kwargs.get("concerned_no", "")

    active_products_response = api.get_active_products(concerned_no=concerned_no)

    lockin_timestamp_str = active_products_response.get("lockinEndTimestamp", "")

    if lockin_timestamp_str:
        lockin_timestamp = datetime.fromisoformat(lockin_timestamp_str.replace("Z", "+00:00"))
        current_datetime = datetime.now(timezone.utc)
        if lockin_timestamp <= current_datetime:
            return True
        else:
            return False
    else:
        return False
    

def get_customer_info(**kwargs) -> dict:
    account_no = kwargs.get("account_no", "")
    msisdn = kwargs.get("msisdn", "")

    if msisdn:
        customer_info_api_response = api.get_customer_info_api(msisdn=msisdn)
    else:
        customer_info_api_response = api.get_customer_info_api(account_no=account_no)

    if not customer_info_api_response:
        return {}

    customer_info = {
        "first_name": customer_info_api_response.get("NameInfo", {}).get("FirstName", ""),
        "last_name": customer_info_api_response.get("NameInfo", {}).get("LastName", ""),
        "email": customer_info_api_response.get("ContactMedium", {}).get("EmailAddress", ""),
        "contact_no": customer_info_api_response.get("ContactMedium", {}).get("PhoneNumber", ""),
        "subscriber_status": customer_info_api_response.get("SubscriberStatus", ""),
        "credit_limit": customer_info_api_response.get("CreditLimit", '0'),
        "account_no": customer_info_api_response.get("AccountNumber", '0')
    }

    return customer_info


def is_kqi_whitelisted(**kwargs) -> bool:
    account_no = kwargs.get("account_no", "")
    check_kqi_whitelist_response = api.check_kqi_whitelist(account_no=account_no)

    is_kqi_whitelisted = check_kqi_whitelist_response.get("isKQIWhitelisted", False)

    if (is_kqi_whitelisted):
        return True
    return False


def is_fub_breached(**kwargs)  -> bool:
    landline = kwargs.get("landline", "")
    get_fup_status_response = api.get_fup_status(landline=landline)

    if not get_fup_status_response:
        return False

    is_fup_breached = get_fup_status_response.get("isFupBreached", "")

    if (is_fup_breached.upper() == "TRUE"):
        return True
    return False


def is_outage(**kwargs) -> bool:
    account_no = kwargs.get("account_no", "")
    bb_outage_response = api.bb_outage(account_no=account_no)

    if not bb_outage_response:
        return False

    is_outage = bb_outage_response.get("isOutage", "")

    if (is_outage.upper() == "TRUE"):
        return True
    return False

def get_diagnostic_details(**kwargs)-> dict:
    account_no = kwargs.get("account_no", "")
    response = api.get_bb_device_diagnostic_details(account_no=account_no)

    if not response:
        return {}

    return {
        "BroadbandAccountStatus": response.get("BroadbandAccountStatus", ""),
        "OutageResult": response.get("OutageResult","").lower(),
        "FUPIndicator": response.get("FUPIndicator", ""),
        "LineStatus": response.get("LineStatus", "").lower(),
        "ModemStatus": response.get("ModemStatus", ""),
        "SubscribedProduct": response.get("SubscribedProduct", "")
    }


def is_caif_whitelisted(**kwargs) -> bool:
    account_no = kwargs.get("account_no", "")
    check_service_recovery_whitelist_response = api.check_service_recovery_whitelist(account_no=account_no)

    if not check_service_recovery_whitelist_response:
        return False

    service_recovery_cohort = check_service_recovery_whitelist_response.get("serviceRecoveryCohort", "")

    if (service_recovery_cohort.upper() == "CAIF"):
        return True
    return False


def is_account_barred(**kwargs)  -> bool:
    account_no = kwargs.get("account_no", "")
    brand_type = kwargs.get("brand_type", "")
    msisdn = kwargs.get("msisdn", "")
    landline = kwargs.get("landline", "")

    retrieve_account_barring_info_response = api.retrieve_account_barring_info(account_no=account_no, brand_type=brand_type, msisdn=msisdn, landline=landline)

    if not retrieve_account_barring_info_response:
        return False

    barring_indicator = retrieve_account_barring_info_response.get("BarringIndicator", "")
    barring_type = retrieve_account_barring_info_response.get("BarringType", "")

    if (barring_indicator.upper() == "Y" and barring_type.upper() in ['SL', 'CL']):
        return True
    return False


def get_prolong_outage_info(**kwargs) -> dict:
    landline = kwargs.get("landline", "")

    get_resource_info_response = api.get_resource_info(concerned_no=landline)

    if not get_resource_info_response:
        return {}

    cabinet_id = get_resource_info_response.get("Cabinet ID", "")
    bb_outage_whitelist_info = whitelist_utils.is_bb_outage_whitelisted(cabinet_id)

    if(bb_outage_whitelist_info):
        return bb_outage_whitelist_info[0]
    return {}


def get_on_site_visit_info(**kwargs) -> dict:
    account_no = kwargs.get("account_no", "")

    check_onsite_visit_response = api.check_onsite_visit(account_no=account_no)

    if not check_onsite_visit_response:
        return {}

    has_result = check_onsite_visit_response.get("result", False)

    if (has_result):
        return check_onsite_visit_response
    return {}


def get_order_info(**kwargs) -> dict:
    # concerned_no is either mobile or landline no
    concerned_no = kwargs.get("concerned_no", "")

    search_order_response = api.search_order(concerned_no=concerned_no)
    search_order_result = search_order_response.get("SearchOrderResult", {})

    if(not search_order_result):
        return {}
    
    search_results = search_order_result.get("SearchResults", {})

    if(not search_results):
        return {}
    
    search_result = search_results.get("SearchResult", [])

    if(not search_result):
        return {}
    
    order_header = search_result[0].get("OrderHeader", {})
    order_action_header = search_result[0].get("OrderActionHeader", {}).get("OrderActionHeader", [])[0]

    return {
        "order_id": order_header.get("OrderID", ""),
        "order_mode": order_header.get("OrderMode", ""),
        "order_status": order_header.get("OrderStatus", ""),
        "application_date": order_header.get("ApplicationDate", ""),
        "serviceRequired_date": order_header.get("ServiceRequiredDate", ""),
        "sales_channel": order_header.get("SalesChannel", ""),
        "current_sales_channel": order_header.get("CurrentSalesChannel", ""),
        "lock_indicator": order_header.get("LockIndicator", ""),
        "days_to_expiration": order_header.get("DaysToExpiration", ""),
        "order_action_id": order_action_header.get("OrderActionId", ""),
        "order_action_type": order_action_header.get("OrderActionType", ""),
        "order_action_status": order_action_header.get("OrderActionStatus", ""),
        "due_date": order_action_header.get("DueDate", ""),
        "service_required_date": order_action_header.get("ServiceRequiredDate", ""),
        "process_id": order_action_header.get("ProcessId", ""),
        "reason": order_action_header.get("Reason", ""),
        "reason_text": order_action_header.get("ReasonText", ""),
    }


def get_balance_info(**kwargs) -> dict:
    brand_type = kwargs.get("brand_type", "")
    account_no = kwargs.get("account_no", "")
    msisdn = kwargs.get("msisdn", "")

    if brand_type=="wireline":
        get_outstanding_balance_response = api.get_outstanding_balance_by_account_id_api(account_no=account_no)
    else:
        get_outstanding_balance_response = api.get_outstanding_balance_by_msisdn_api(msisdn=msisdn)

    if(not get_outstanding_balance_response):
        return {}

    return {
        "outstanding_balance": get_outstanding_balance_response.get("ArBalance", '0'),
        "overdue_balance": get_outstanding_balance_response.get("OverdueBalance", '0'),
    }

def is_blacklisted(**kwargs) -> dict:
    msisdn = kwargs.get("msisdn", "")

    retrieve_subscriber_details_by_msisdn_response = api.retrieve_subscriber_details_by_msisdn_api(msisdn = msisdn)

    if retrieve_subscriber_details_by_msisdn_response["RetrieveSubscriberDetailsByMsisdn"]["ContactDetails"].get("IsBlackListed"):
        return True
    else:
        return False

def search_appointment_slot_info(**kwargs) -> dict:
    # define all static attributes and get the dynamic attributes from the kwargs parameter.
    request = {
        "account_no": kwargs.get("account_no", ""),
        "landline": kwargs.get("landline", ""),
        "case_id": kwargs.get("case_id", ""),
        "concern": kwargs.get("concern", ""),
        "caseTypeLevel1": kwargs.get("case_details", {}).get("lvl1", ""),
        "caseTypeLevel2": kwargs.get("case_details", {}).get("lvl2", ""),
        "caseTypeLevel3": kwargs.get("case_details", {}).get("lvl3", ""),
        "caseTypeLevel4": kwargs.get("case_details", {}).get("lvl4", ""),
        "caseTypeLevel5": kwargs.get("case_details", {}).get("lvl5", ""),
        "mobile": kwargs.get("session_context_attributes", {}).get("contactNo", ""),
        "altContactNo": kwargs.get("session_context_attributes", {}).get("altContactNo", ""),
        "acoountStatus": kwargs.get("session_context_attributes", {}).get("BroadbandAccountStatus", ""),
        "outageResult": kwargs.get("session_context_attributes", {}).get("OutageResult", ""),
        "fupIndicator": kwargs.get("session_context_attributes", {}).get("FUPIndicator", ""),
        "lineStatus": kwargs.get("session_context_attributes", {}).get("LineStatus", ""),
        "modemStatus": kwargs.get("session_context_attributes", {}).get("ModemStatus", ""),
        "billingOfferName": kwargs.get("session_context_attributes", {}).get("SubscribedProduct", ""),
    }

    search_appointment_slot_response = api.search_appointment_slot(**request)

    if not search_appointment_slot_response:
        return {}
    
    return {
        "hasAvailableAppointmentSlot": search_appointment_slot_response.get("hasAvailableAppointmentSlot", "false"),
        "orderNumber": search_appointment_slot_response.get("orderNumber", ""),
        "selectedChoice": search_appointment_slot_response.get("selectedChoice", ""),
        "amSlotDate": search_appointment_slot_response.get("amAppointmentSlotDate", ""),
        "pmSlotDate": search_appointment_slot_response.get("pmAppointmentSlotDate", ""),
        "date": search_appointment_slot_response.get("date", ""),
        "slot": search_appointment_slot_response.get("slot", ""),
    }


def confirm_appointment_slot(**kwargs) -> dict:
    # define all static attributes and get the dynamic attributes from the kwargs parameter.
    request = {
        "account_no": kwargs.get("account_no", ""),
        "order_number": kwargs.get("order_number", ""),
        "appointment_date": kwargs.get("appointment_date", ""),
        "appointment_slot": kwargs.get("appointment_slot", ""),
    
    }

    confirm_appointment_slot_response = api.confirm_appointment_slot_api(**request)

    if not confirm_appointment_slot_response:
        return {}
    
    appointment_id = confirm_appointment_slot_response.get("appointmentId", "")
    
    return {
        "appointmentId": appointment_id,
        "isSlotConfirmed": True if appointment_id else False
    }

def update_case_details(**kwargs) -> bool:
    # define all static attributes and get the dynamic attributes from the kwargs parameter.
    # request = {
    #     "case_id": kwargs.get("case_id", ""),
    #     "case_notes": kwargs.get("case_notes", ""),
    #     "queue": kwargs.get("queue", "")
    
    # }

    update_case_details_response = api.update_case_details_api(**kwargs)

    if "UpdateCaseDetailResult" in update_case_details_response and update_case_details_response.get("UpdateCaseDetailResult", {}).get("Status", "") == "1":
        return True
    return False


def get_overdue_balance_info(**kwargs) -> dict:

    request = {
        "msisdn": kwargs.get("msisdn", "")
    }

    logger.info(f"get_overdue_balance_info(request): {request}")
    get_overdue_balance_info_response = api.get_overdue_balance_by_msisdn_api(**request)
    logger.info(f"get_overdue_balance_info_response:{get_overdue_balance_info_response}")
    if not get_overdue_balance_info_response:
        return {}
    
    return {
        "overdue_balance": get_overdue_balance_info_response.get("overDueBalance", 0),
        "last_payment_date": get_overdue_balance_info_response.get("lastPaymentDate", ''),
        "last_payment_amount": get_overdue_balance_info_response.get("lastPaymentAmount", 0)    
    }    


def get_bb_overdue_balance_info(**kwargs) -> dict:
    request = {
        "accountId": kwargs.get("accountId", "")
    }

    logger.info(f"get_bb_overdue_balance_info(request): {request}")
    get_bb_overdue_balance_response = api.get_overdue_balance_by_accountId_api(**request)
    logger.info(f"get_bb_overdue_balance_response:{get_bb_overdue_balance_response}")
    if not get_bb_overdue_balance_response:
        return {}
    
    return {
        "overdue_balance": get_bb_overdue_balance_response.get("overDueBalance", 0),
        "last_payment_date": get_bb_overdue_balance_response.get("lastPaymentDate", ''),
        "last_payment_amount": get_bb_overdue_balance_response.get("lastPaymentAmount", 0)    
    }


def get_account_barring_info(**kwargs)  -> dict:
    account_no = kwargs.get("account_no", "")
    brand_type = kwargs.get("brand_type", "")
    msisdn = kwargs.get("msisdn", "")
    landline = kwargs.get("landline", "")

    retrieve_account_barring_info_response = api.retrieve_account_barring_info(
        account_no=account_no,
        brand_type=brand_type,
        msisdn=msisdn,
        landline=landline
    )

    if not retrieve_account_barring_info_response:
        return {}

    barring_indicator = retrieve_account_barring_info_response.get("BarringIndicator", "")
    barring_type = retrieve_account_barring_info_response.get("BarringType", "")

    return {
        "barring_indicator": barring_indicator,
        "barring_type": barring_type
    }
