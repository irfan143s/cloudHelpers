# NIAS 2.0 - HISAMS
import re
import copy
import boto3
import json
import uuid
import random
import logging

from datetime import datetime, timedelta
from configuration import TIMEZONE_PH, REGION_OREGON
from dateutil import parser, tz
from dateutil.relativedelta import relativedelta

import helpers.tools as tools

from libraries import phonenumbers

from helpers.agenttools import AgentTools

from resources.api import SOCIO_UPDATE_API
from resources.aws_lambda import (
    TRANSFER_TO_AGENT_LAMBDA,
    FOLLOWUP_LAMBDA,
    MAIN_MENU_LAMBDA,
    BILLS_AND_PAYMENTS_LAMBDA,
    LOSTPHONE_OR_SIM_LAMBDA,
    CHAT_TO_CALL_LAMBDA,
    CHECK_APPLICATION_LAMBDA
)
from resources.states import (
    MAIN_MENU_STATE,
    BILLS_AND_PAYMENTS_STATE,
    LOSTPHONE_OR_SIM_STATE,
    CHECK_APPLICATION_FOLLOW_UP_STATE
)
from resources.resourcemapping import (
    state_default_sub_state_mapping_dict
)

from configuration import (
    GT_PAGE_ID,
    MYBUSINESS_PAGE_ID,
    THEA_PAGE_ID,
    TM_PAGE_ID,
    GAH_PAGE_ID,
    SOCIO_PROFILE_ID_GT,
    SOCIO_PROFILE_ID_MB,
    SOCIO_PROFILE_ID_TP,
    SOCIO_PROFILE_ID_TM,
    SOCIO_PROFILE_ID_GH,
    SOCIO_ORG_ID
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

LANGUAGES = ['english', 'tagalog']
REGEX_PH_MOBILE_NUMBER= r'^(\+63|63|0)?(8|9)([0-9]{9})$'

def _get_time_period(hour):
    tmp = {}
    if hour >= 1 and hour <= 11:
        tmp['english'] = "Morning"
        tmp['tagalog'] = "Umaga"
    elif hour >= 12 and hour <= 17:
        tmp['english'] = "Afternoon"
        tmp['tagalog'] = "Hapon"
    else:
        tmp['english'] = "Evening"
        tmp['tagalog'] = "Gabi"

    return tmp


def get_exception_str(exception):
    return str(exception.__class__.__name__) + " | " + str(exception)


def modify_epoch_time(operation, unit, quantity, epoch_time):

    if operation.upper().strip() not in ["ADD", "SUBTRACT"]:
        raise ValueError("Invalid oparation:", operation)

    if unit.upper().strip() not in ["YEARS", "MONTHS", "DAYS", "HOURS", "MINUTES", "SECONDS"]:
        raise ValueError("Invalid unit:", unit)

    unit = unit.upper().strip()
    operation = operation.upper().strip()
    quantity = int(quantity)
    epoch_time = int(epoch_time)
    time_delta = 0

    if unit == "YEARS":
        time_delta = relativedelta(years=quantity)
    elif unit == "MONTHS":
        time_delta = relativedelta(months=quantity)
    elif unit == "DAYS":
        time_delta = timedelta(days=quantity)
    elif unit == "HOURS":
        time_delta = timedelta(hours=quantity)
    elif unit == "MINUTES":
        time_delta = timedelta(minutes=quantity)
    elif unit == "SECONDS":
        time_delta = timedelta(seconds=quantity)

    tmp_time = datetime.fromtimestamp(epoch_time)

    if operation == "ADD":
        tmp_time = tmp_time + time_delta
    else:
        tmp_time = tmp_time - time_delta

    return int(tmp_time.timestamp())


def get_time_period(timestamp=None, language=None):
    if timestamp is not None:
        try:
            hour = parser.parse(timestamp).hour
        except Exception as error:
            print("Error parsing timestamp:", get_exception_str(error))
            return
    else:
        hour = datetime.now(tz = tz.gettz(TIMEZONE_PH)).hour

    if language is not None and language.lower() in LANGUAGES:
        return _get_time_period(hour)[language.lower()]
    else:
        return _get_time_period(hour)['english']


def get_current_epoch_time():
    return datetime.now(tz = tz.gettz(TIMEZONE_PH)).timestamp()

def get_current_time():
    return datetime.now(tz = tz.gettz(TIMEZONE_PH)).isoformat()


def get_current_datetime():
    return datetime.now(tz = tz.gettz(TIMEZONE_PH)).replace(tzinfo=None)
    
def get_current_datetime_without_marker():
    return datetime.now(tz = tz.gettz(TIMEZONE_PH)).astimezone(tz = tz.gettz(TIMEZONE_PH))    

def get_datetime_from_string(str_date):
    return parser.parse(str_date).replace(tzinfo=None)


def get_datetime_from_millisecond(millisecond):
    return datetime.fromtimestamp(int(millisecond)/1000.0)


def generate_random_id():
    return str(uuid.uuid4())


def generate_6_digits_otp():
    return random.randint(100000, 999999)
  

def format_concern_number(num):
    num = num.replace(" ","").strip()
    
    if num.startswith('0') and len(num) == 11:
        num = num[-10:]
    elif num.startswith('('):
        num = num.replace('(', "").replace(')', "")
        num = num[1:]
    
    return '+63' + num


def get_10_digit_mobile_number(num):
    return num[-10:]


def get_11_digit_mobile_number(num):
    return '0' + num[-10:]


def get_12_digit_mobile_number(num):
    return '63' + num[-10:]


def get_13_digit_mobile_number(num):
    return '+63' + num[-10:]


def get_E164_formatted_PH_no(num):
    return phonenumbers.format_number(phonenumbers.parse(num, 'PH'), phonenumbers.PhoneNumberFormat.E164)


def is_valid_phonenumber(num):
    if not tools.number_regex_validator(num):
        return False
    
    return True


def is_valid_ph_mobile_number(num=''):
    if not re.fullmatch(REGEX_PH_MOBILE_NUMBER, num):
        return False
    return True

def format_mobile_number(number):
    number = re.sub('[^0-9a-zA-Z()]+', '', number)
    if number.startswith("0") and len(number) == 11:
        number = number[1:] 

    elif number.startswith("9") and len(number) == 10:
        number = number[0:]
        
    elif number.startswith("63") and len(number) in [11, 12]:
        number = number[2:]

    elif number.startswith("+63") and len(number) in [12, 13]:
        number = number[3:]

    elif number.startswith("(") and len(number) == 12:
        ccodeLen = len(number.split(')')[0])
        ccode = number.split(')')[0]
        
        logger.info(f"{ccodeLen} {ccode}")
        
        if (ccodeLen == 3 and ccode != '(02'):
            number = number[4:]
        elif (ccodeLen == 3 and ccode == '(02'):
            number = '2' + number[4:]
        else:
            number = re.sub('[^0-9]+', '', number)[1:]
    else:
        return number
    number = "+63" + number
    return number

def is_valid_ph_landline_number(number):
    try:
        parsed_number = phonenumbers.parse(number, "PH")
        
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.FIXED_LINE
        else:
            return False
    except phonenumbers.NumberParseException:
        return False

def  is_valid_ph_number(number):
    try:
        parsed_number = phonenumbers.parse(number, "PH")  # "PH" is the country code for the Philippines
        return phonenumbers.is_valid_number(parsed_number)
    except phonenumbers.NumberParseException:
        return False


def invoke_transfer_to_agent(request, intent_id, meta_data={}, connect_to_agent_spiel=None):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)

    transfer_to_agent_payload = request
    transfer_to_agent_payload['intentId'] = intent_id
    transfer_to_agent_payload['intentMetadata'] = meta_data
    transfer_to_agent_payload['connectToAgentSpiel'] = connect_to_agent_spiel

    try:
        transfer_to_agent_response = lmbd_clnt_oregon.invoke(FunctionName = TRANSFER_TO_AGENT_LAMBDA, InvocationType = "Event", Payload = json.dumps(transfer_to_agent_payload))
        # transfer_to_agent_response = json.loads(transfer_to_agent_response['Payload'].read().decode())
        logger.info(f"transferToAgent response: {transfer_to_agent_response}")
    except Exception as error:
        logger.info(f"Error invoking {TRANSFER_TO_AGENT_LAMBDA}: {get_exception_str(error)}")
        return False

    return True

    # if  transfer_to_agent_response['statusCode'] != 200:
    #     return False
    # else:
    #     return True


def invoke_chat_to_call(request):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)

    try:
        logger.info(f"Invoking {CHAT_TO_CALL_LAMBDA}")
        lmbd_clnt_oregon.invoke(FunctionName=CHAT_TO_CALL_LAMBDA, InvocationType="Event", Payload=json.dumps(request))
    except Exception as e:
        logger.error(f"chat to call lambda invocation error: {get_exception_str(e)}")

    return True


def append_string_to_option_ids(buttons, str=""):
    btns = copy.deepcopy(buttons)
    for button in btns:
        button.update({
            "optionId": button["optionId"] + str
        })
    return btns


def close_socio_ticket(page_id, fb_id):
    agent = AgentTools(page_id)

    if page_id == GT_PAGE_ID:
        profile_id = SOCIO_PROFILE_ID_GT
    elif page_id == MYBUSINESS_PAGE_ID:
        profile_id = SOCIO_PROFILE_ID_MB
    elif page_id == THEA_PAGE_ID:
        profile_id = SOCIO_PROFILE_ID_TP
    elif page_id == TM_PAGE_ID:
        profile_id = SOCIO_PROFILE_ID_TM
    elif page_id == GAH_PAGE_ID:
        profile_id = SOCIO_PROFILE_ID_GH

    agent.updateStatus(SOCIO_UPDATE_API.format(SOCIO_ORG_ID), page_id, fb_id, profile_id, None, "CLOSE")


    """*************************************************************************************************
    ********************* Transferring flow utils ******************************************************
    *************************************************************************************************"""

def invoke_followup(request):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request['subState'] = "0"
    lmbd_clnt_oregon.invoke(FunctionName = FOLLOWUP_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))


def invoke_main_menu(request, session_tools):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "subState": "0",
        "sessionState": MAIN_MENU_STATE
    })
    session_tools.reset_state()
    session_tools.update_attributes({"sessionState": MAIN_MENU_STATE, "subState": "0"})
    lmbd_clnt_oregon.invoke(FunctionName = MAIN_MENU_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))


def invoke_bills_and_payment(request):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": BILLS_AND_PAYMENTS_STATE,
        "subState":  state_default_sub_state_mapping_dict[BILLS_AND_PAYMENTS_STATE]
    })
    lmbd_clnt_oregon.invoke(FunctionName = BILLS_AND_PAYMENTS_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))


def invoke_lost_phone_or_sim(request, request_attrs={}):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": LOSTPHONE_OR_SIM_STATE,
        "subState":  "DPN"
    })

    if request_attrs:
        for key, value in request_attrs.items():
            request[key] = value 

    lmbd_clnt_oregon.invoke(FunctionName = LOSTPHONE_OR_SIM_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))

def invoke_check_application(request):
    lmbd_clnt_oregon = boto3.client("lambda", region_name = REGION_OREGON)
    request.update({
        "sessionState": CHECK_APPLICATION_FOLLOW_UP_STATE,
        "subState":  '0',
        "optionId": '[option].checkapprenewapplication'
    })
    lmbd_clnt_oregon.invoke(FunctionName = CHECK_APPLICATION_LAMBDA, InvocationType = "Event", Payload = json.dumps(request))

def subtract_datetime(date, unit, num, format):
    date_obj = datetime.strptime(date, format)
    past_date = None
    if unit == "months":
        past_date = date_obj - relativedelta(months=num)
    if unit == "days":
        past_date = date_obj - relativedelta(days=num)
    if unit == "years":
        past_date = date_obj - relativedelta(years=num)
    if unit == "hours":
        past_date = date_obj - relativedelta(hours=num)
    if unit == "minutes":
        past_date = date_obj - relativedelta(minutes=num)
    if unit == "seconds":
        past_date = date_obj - relativedelta(seconds=num)

    return past_date


def add_datetime(date, unit, num, format):
    date_obj = datetime.strptime(date, format)
    new_date = None
    if unit == "months":
        new_date = date_obj + relativedelta(months=num)
    if unit == "days":
        new_date = date_obj + relativedelta(days=num)
    if unit == "years":
        new_date = date_obj + relativedelta(years=num)
    if unit == "hours":
        new_date = date_obj + relativedelta(hours=num)
    if unit == "minutes":
        new_date = date_obj + relativedelta(minutes=num)
    if unit == "seconds":
        new_date = date_obj + relativedelta(seconds=num)

    return new_date

def arrange_dict_keys(input_dict, key_order):
    arranged_dict = {}
    for key in key_order:
        if key in input_dict:
            arranged_dict[key] = input_dict[key]
    return arranged_dict