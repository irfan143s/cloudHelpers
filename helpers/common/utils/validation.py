from __future__ import annotations

from datetime import datetime

from libraries import phonenumbers
import re

from helpers.utils import get_current_time
from configuration import *

def is_valid_ph_landline_number(number) -> bool:
    try:
        parsed_number = phonenumbers.parse(number, "PH")
        
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.FIXED_LINE
        else:
            return False
    except phonenumbers.NumberParseException:
        return False


def is_valid_ph_mobile_number(number) -> bool:
    try:
        parsed_number = phonenumbers.parse(number, "PH")
        
        if phonenumbers.is_valid_number(parsed_number):
            return phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE
        else:
            return False
    except phonenumbers.NumberParseException:
        return False
    
    
def is_valid_mmdd_date_format(date_str: str) -> bool:
    if len(date_str.strip()) != 4:
        return False
    
    try:
        # datetime.datetime.strptime(date_str, "%m%d")
        datetime.strptime(f"2000{date_str}", "%Y%m%d")
        return True
    except ValueError:
        return False
    

def is_valid_amount_without_centavo(amount: str) -> bool:
    try:
        amount = amount.strip()
        if '.' in amount:
            return False
        
        float(amount)
        return True
    except ValueError:
        return False
    

def is_valid_number(text: str):
    number = []
    for match in phonenumbers.PhoneNumberMatcher(text, "PH"):
        number.append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.NATIONAL))
    
    try:
        result = {
            "validNumber": number[0],
            "isValid": True
        }
        
        return result
    except:
        regEx = re.findall(r'(\b[\d@_!#$%^&*()<>?/\|}{~:\[\]\+]+\b)', text)
        seperator = ''
        wholeNum = seperator.join(regEx)
        print(wholeNum)

        if len(wholeNum) == 10 and wholeNum[0] == "9":
            newNum = "0" + wholeNum
            number = []
            for match in phonenumbers.PhoneNumberMatcher(newNum, "PH"):
                number.append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.NATIONAL))
            try:
                result = {
                    "validNumber": number[0],
                    "isValid": True
                }
                return result
                
            except:
                result = {
                    "validNumber": "",
                    "isValid": False
                }
                return result

        if len(wholeNum) >= 8 and len(wholeNum) <= 12:
            result = {
                "validNumber": wholeNum,
                "isValid": True
            }

            return result
        else: 
            result = {
                "validNumber": wholeNum,
                "isValid": False
            }
            return result
        

def is_within_hoop(start_time, end_time):
    current_datetime_str = get_current_time()
    current_datetime = datetime.fromisoformat(current_datetime_str)
    current_time = current_datetime.time()
    hoop_start = datetime.strptime(start_time, "%H:%M:%S").time()
    hoop_end = datetime.strptime(end_time, "%H:%M:%S").time()

    if not (hoop_start <= current_time <= hoop_end ):
        return False

    return True