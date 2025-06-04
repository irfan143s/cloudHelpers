import boto3
from libraries import requests, phonenumbers
import json
import re
import logging
from datetime import datetime
from resources.aws_lambda import MENU_LAMBDA, OTP_LAMBDA
from resources.constants import LEX
from resources.api import GLOBE_ONE_PLAN_DETAILS
from resources.spiels import *
from resources.states import INTENT_OTP_STATE 



logger = logging.getLogger()
logger.setLevel(logging.INFO)

##recursively look/return for an item in dict given key
def find_item(obj, key):
    item = None
    if key in obj: return obj[key]
    for k, v in obj.items():
        if isinstance(v,dict):
            item = find_item(v, key)
            if item is not None:
                return item

##recursivley check for items in a dict given key
def keys_exist(obj, keys):
    for key in keys:
        if find_item(obj, key) is None:
            return(False)
    return(True)

# error handling
def error_handling(res, convo, sessionAttributes,invokeLambda, senderId, lastNumber, lastBrand , lastIntent, lexPayload):
    res.send_message(senderId, ERROR_SPIEL)
    convo.log(senderId, lastNumber, lastBrand, LEX, lastIntent, ERROR_SPIEL)
    sessionAttributes['FollowUpSpiel'] = ERROR_SPIEL_FOLLOW_UP_SPIEL
    invokeLambda.invoke(FunctionName = MENU_LAMBDA, InvocationType = "Event", Payload = json.dumps(sessionAttributes))   
    return lexPayload

# session handling
def session_handling(res, dynamodb, senderId, currentIntent, sessionAttributes, invokeLambda,language="english"):
    dynamodb.updateIntent(senderId, currentIntent)
 
    if(sessionAttributes['inSession'] == "0"):
        res.send_message(senderId, OTP_SESSION_DICT_SPIEL[language])
        sessionAttributes['sessionState'] = INTENT_OTP_STATE
        sessionAttributes['subState'] = '0'
        invokeLambda.invoke(FunctionName = OTP_LAMBDA, InvocationType = "Event", Payload=json.dumps(sessionAttributes))
        return True
    else:
        return False

def number_regex_validator(text):
    number = []
    for match in phonenumbers.PhoneNumberMatcher(text, "PH"):
        number.append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.NATIONAL))
    
    try:
        return number[0]
        
    except:
        regEx = re.findall(r'(\b[\d@_!#$%^&*()<>?/\|}{~:\[\]\+]+\b)', text)
        seperator = ''
        wholeNum = seperator.join(regEx)
        print(wholeNum)
        if len(wholeNum) == 9:
            broadbandNumber = wholeNum
            return broadbandNumber
        elif len(wholeNum) == 10:
            tenDigitBroadbandNumber = wholeNum
            return tenDigitBroadbandNumber
        
        else:
            newNum = "0" + wholeNum
            number = []
            for match in phonenumbers.PhoneNumberMatcher(newNum, "PH"):
                number.append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.NATIONAL))
            try:
                return number[0]
                
            except:
                return False

def api_call(api,params,headers,request,method):

    data = json.dumps(request)
    if method == "GET":
        req = requests.get(api, params=params, headers=headers, data=data)
    elif method == "POST":
        req = requests.post(api, params=params, headers=headers, data=data)
    return req
    
def send_email(region, sourceAddress, destinationAddress, subject, emailBody):
    try:
        client = boto3.client('ses', region_name=region)
        resp = client.send_email(
            Source=sourceAddress,
            Destination={
                'ToAddresses': destinationAddress
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': emailBody
                    }
                }
            }
        )
    except Exception as e:
        raise Exception(json.dumps({'statusCode':500,'body':e.__str__()}))
    return {
        "statusCode": 200,
        "body": "Success"
    }
#for regex and date validation


def dateValidation(message):
    """sample valid inputs:
        06/22/2020 11:30AM
        06/22/20
        11:30 PM
        06 /22 / 20 11:30 AM
        June 22, 2020 11:30AM
        11:30AM June 22, 2020
        aaaadsfa 06/22/2020 11:30 PM dfadf
    Args:
        message (string): accepts the specified date format with non military time

    Returns:-
        [type]: True/False
    """

    validation1={
    "regexValidation" : "(([0-9]+\s?\/\s?[0-9]+\s?\/\s?[0-9]+\s?[0-9]+:[0-9]+\s?)(AM|PM))|(([0-9]+:[0-9]+\s?)(AM|PM)(\s[0-9]+\s?\/\s?[0-9]+\s?\/\s?[0-9]+))",
    "dateValidation": ["%m/%d/%Y","%m/%d/%Y%I:%M%p","%I:%M%p%m/%d/%Y%","%m/%d/%y%I:%M%p","%I:%M%p%m/%d/%y"]
    }

    validation2 = {
        "regexValidation":"(([a-zA-Z]+\s[0-9]+\,\s[0-9]+\s[0-9]+:[0-9]+\s?)(AM|PM))|(([0-9]+:[0-9]+\s?)(AM|PM)(\s[a-zA-Z]+\s[0-9]+\,\s[0-9]+))",
        "dateValidation":["%m/%d/%Y","%B%d,%Y%I:%M%p","$I:%M%p%B%d,%Y","%B%d,%y$I:%M%p","$I:%M%p%B%d,%y"]
    }

    validation3 = {
        "regexValidation" : "^(?:(1[0-2]|0?[1-9])\/(3[01]|[12][0-9]|0?[1-9])|\?(3[01]|[12][0-9]|0?[1-9])\/(1[0-2]|0?[1-9]))\/(?:(?:1[6-9]|[2-9]\d)?\d{2})$",
        "dateValidation":["%m/%d/%Y","%B%d,%Y%I:%M%p","$I:%M%p%B%d,%Y","%B%d,%y$I:%M%p","$I:%M%p%B%d,%y"]
    }

    validationList=[validation1,validation2,validation3]

    for validation in validationList:
        cleanmessage = re.search(validation["regexValidation"],message,re.IGNORECASE)
        if cleanmessage is not None:
            for dateValidation in validation["dateValidation"]:
                try:
                    date = datetime.strptime(str(cleanmessage.group(0)).replace(" ",""), dateValidation)
                    if(date < datetime.now()): return date
                except ValueError:
                    print(ValueError)
    else:
        return False
        
def emailValidation(email):
    """[summary]
        checks if the string has a valid email in it.
        sample:
            input: this is a email trial@globe.com random random
            return: trial_email@globe.com.ph
    Args:
        email (string): enter a the string with email present in it
    Returns:-
        [string]: first email within the string / empty string
    """
    regex = re.compile(r"[A-Za-z0-9]+[\w.-]*[A-Za-z0-9]@+[\w.-]+[A-Za-z]+[.]+[\w]+")
    emails = regex.findall(email)
    if len(emails) == 0:
        return ""
    else:

        return emails[0]

# G1 Postpaid Plan Details API Call
def getContractEndDate(globe_one_token, g_channel, g_platform, lastNumber, retry=0):
    headers = {
        "Authorization" : globe_one_token,
        "g-channel" : g_channel,
        "g-platform" :g_platform
    }

    data = {
        "serviceNumber": f"0{lastNumber}",
        "primaryResourceType": "C",
        "forceRefresh": False
    }

    try:
        data = json.dumps(data)
        req = requests.post(GLOBE_ONE_PLAN_DETAILS, headers=headers, data=data)
        response = req.json()
        print(f"[API] {GLOBE_ONE_PLAN_DETAILS}|{lastNumber}|Retry:{retry}|Response:{response}")
        
        # Request Error
        if response["responseCode"] != 200:
            # API Retry
            if retry <= 3:
                getContractEndDate(globe_one_token, g_channel, g_platform, lastNumber, retry+1)

            # Max API retries
            else:
                print(f"[API] Max retries achieved|{GLOBE_ONE_PLAN_DETAILS}|{lastNumber}")
                return None, None, None

        # Successful Request
        else:
            contractExpired = response["planDetail"]["contractExpired"] / 1000
            contractEndDate = datetime.utcfromtimestamp(contractExpired)
            dateToday = datetime.now()
            delta = contractEndDate - dateToday

            return contractEndDate.strftime("%B %-d, %Y"), delta.days < 0, delta.days <= 30

    except Exception as error:
        print(f"[ERROR] {GLOBE_ONE_PLAN_DETAILS}|{lastNumber}|{str(error.__class__.__name__)}")
        return None, None, None