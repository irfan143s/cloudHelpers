import json
import logging
from time import sleep
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
import boto3
from resources.states import *
from resources.constants import *
from resources.spiels import *
from configuration import *
from helpers.utils import *
from helpers.dbtools import DbTools
from configuration import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)
RETRY_EXCEPTIONS = ("ProvisionedThroughputExceededException",
                    "ThrottlingException")
class KafkaTools:

    def __init__(self,table_name=LEX_EDO_INGESTION_TABLE,region=REGION):
        self.dynamodb = boto3.resource("dynamodb", region_name=region)
        self.ingestion_table = self.dynamodb.Table(table_name)

    def __get_common_fields(self,event,transaction_status,failed_message,ttl_days):
        now = get_current_datetime()
        dateTimeWithoutMarker = str(get_current_datetime_without_marker())
        TTL = now + timedelta(days=ttl_days)
        response = {
            "ps_id":event.get("fbId","null"),
            "account_or_phone_number":self.__get_phone_and_account_number(event),
            "brand":event.get("lastBrand","null"),
            "state":event.get("sessionState","null"),
            "substate":event.get("subState","null"),
            "channel":pageDictionary.get(event.get("channel","null"),"null"),
            "last_intent":event.get("lastIntent","null"),#null
            "registered_date":self.__get_registered_date(event), #same with new_user_date
            "jr_date":event.get("jrDate","null"), #null
            "new_user_date":self.__get_registered_date(event),#same with registered date
            "in_session":event.get("inSession","null"),#null
            "educational_date":event.get("educationalDate","null"),#null
            "retry":str(event.get("retry","null")),
            "intent_source":event.get("intentSource","null"),#null
            "language_option":event.get("languageOption","null"), #null
            "transaction_start_date":event.get("transactionStartDate","null"), #insert every start of function
            "transaction_status":transaction_status, #Success or Failed
            "failed_message":failed_message, #if failed transactions are not applicable, this can be set to "null",
            "timestamp_utc_8": dateTimeWithoutMarker,
            "record_creation_time":dateTimeWithoutMarker,
            "uuid":generate_random_id(),
            "TTL":int(TTL.timestamp()),
            "application_status": {
                "full_name": "null",
                "email":"null",
                "order_reference_number": "null"
            },
            "buy_load":{
                "msisdn":"null",
                "lob_name":"null",
                "wallet":"null",
                "amax_token":"null",
                "amount":"null",
                "payment_id":"null",
                "payment_method":"null",
                "payment_status":"null"
            },
            "chicago":{
                "beneficiary":"null",
                "gift":"null",
                "note_name":"null",
                "success":"null",
                "quantity":"null"
            },
            "shop_voucher": {
                "items": "null"
            },
            "birthday_treats": {
                "second_time_flag":"null",
                "address": "null",
                "coupon_code": "null"
            },           
            "reconnect_line": {
                "number": "null",
                "amount": "null",
                "date": "null",
                "account_number": "null",
                "advisory": "null",
            },
            "upgrade_platinum": {
                "name": "null",
                "email":"null",
                "number_brand": "null",
                "number": "null"
            },            
            "report_issue": {
                "date_received":"null",
                "load_date": "null",
                "affected_number":"null",
                "load_amount":"null",
                "issue": "null",
                "payment_method": "null",
                "load_type": "null"
            },
            "rpma": {
                "business": "null",
                "name":"null",
                "contact_number": "null",
                "email_add":"null",
                "multiple_renew": "null"
            },
            "renew_plan": {
                "contract_end_date":"null",
                "overdue_balance":"null",
                "last_choice": "null",
                "product": "null"
            },
            "renew_plan_advisory_date": "null",
            "other_registered_numbers": "null",
            "go_health_pax":"null",
            "troubleshooting_concern":"null",
            "gah_metadata":"null",
            "conversation_summary": "null",
            "intent_id": "null",
            "unrecognized_retry": "null",
            "termination_reason": "null",
            "chosen_plan": "null",
            "report_problem_concern": "null",
            "network_concern": { 
                "location": "null", 
                "signal": "null", 
                "issue": "null"
            },
            "load_concern":{
                "issue": "null", 
                "date_time": "null"
            },
            "promo_concern": {
                "promo": "null", 
                "date_time": "null"
            },
            "bill_concern": "null" ,
            "other_concern": "null" ,
            "chosen_faq":"null",
            "transaction_history": { 
                "email": "null", 
                "last_number":"null"
            },
            "referral": "null",
            "payment_option": "null",
            "business_type": "null" ,
            "my_business_faq": { 
                "topic":"null", 
                "subtopic": "null"
            },
            "business_management_topic": "null"
        }
        
        return response

    def __get_registered_date(self,event):
        try:
            if pageDictionary.get(event.get("channel","null"),"null") ==  THEA_PAGE_NAME:
                if "registeredDate" in event:
                    registeredDate = event["registeredDate"]
                    if "T" in registeredDate:
                        registeredDate = datetime.strptime(registeredDate,"%Y-%m-%dT%H:%M:%S.%f%z")
                        return str(registeredDate)
                    else:
                        return registeredDate
                else:
                    logger.info("kafka thea: registered not registered")
                    return '1900-01-01 00:00:00.00000+08:00'
            else:
                return event.get("newUserDate","null")

        except Exception as error:
            logger.info(f"Kafka: error in registered Date {str(error)}")
            return '1900-01-01 00:00:00.00000+08:00'
            

    def __get_phone_and_account_number(self,event):
        if pageDictionary.get(event.get("channel","null"),"null") ==  THEA_PAGE_NAME:
            if event.get('registeredNumber'):
                return event.get('registeredNumber')
            elif event.get('platinumNumber'):
                return event.get('platinumNumber')
            else:
                return event.get("lastNumber","null")
        else:
            return event.get("lastNumber","null")

    def __get_state_values(self,event):
        sessionState = event["sessionState"]
        state_values = {
            FORM_TO_MAIL_STATE:self.__checkApplicationStatus_values,
            CHECK_APPLICATION_STATE:self.__checkApplicationStatus_values,
            THEA_BIRTHDAY_TREATS_STATE:self.__birthdayTreats_values,
            BUY_LOAD_OR_PROMO_STATE:self.__no_values,
            REFLINK_CONCIERGE_STATE:self.__conciergeReflink_values,
            REFLINK_RENEW_PLAN_STATE:self.__renewPlanReflink_values,
            MODIFY_OR_TERMINATE_CHANGE_PLAN_STATE:self.__changePlan_values,
            NETWORK_CONCERN_STATE:self.__networkConcern_values,
            RENEW_PLAN_IPHONE13_RESERVE_NOW_STATE:self.__renewPlan_values,
            RENEW_PLAN_IPHONE13_CHECK_STATUS_STATE:self.__renewPlan_values,
            RENEW_PLAN_CHECK_ELIGIBILITY_STATE:self.__renewPlan_values,
            RENEW_PLAN_VISIT_ONLINE_SHOP_STATE:self.__renewPlan_values,
            RENEW_PLAN_REPORT_ONLINE_ISSUE_STATE:self.__renewPlan_values,
            RENEW_PLAN_FOLLOWUP_ORDER_STATE:self.__renewPlan_values,
            MYB_REGISTERING_STATE:self.__myBusinessRegistering_values,
            MYB_MANAGING_STATE:self.__myBusinessManaging_values,
            BILLS_AND_PAYMENTS_STATE:self.__billsAndPayments_values,
            LOAD_PROMOS_AND_REWARDS_STATE:self.__loadPromosAndRewards_values,
            THEA_REGISTRATION_STATE:self.__upgradePlatinum_values,
            THEA_MAIN_MENU_STATE:self.__upgradePlatinum_values,
            THEA_NIA_MENU_STATE:self.__upgradePlatinum_values,
            MODIFY_OR_TERMINATE_TERMINATE_LINE_STATE:self.__terminateLine_values,
            RECONNECT_MY_LINE_STATE:self.__reconnectLine_values
        }
        if sessionState in state_values:
            return state_values[sessionState](event)
        else:
            logger.info(f"KAFKA: Session_state: {sessionState} not existing on state values. Kindly check __get_state_values function")
            return False
        

    def __checkApplicationStatus_values(self,event):
        applicationStatus = event.get("formToMail", {})
        return {
            "application_status": {
                "full_name": applicationStatus.get("customerName", "null"),
                "email": applicationStatus.get("emailAdd", "null"),
                "order_reference_number": applicationStatus.get("orderRefNum","null")
            }
        }
    def __birthdayTreats_values(self, event):
        return {
            "birthday_treats": {
                "second_time_flag":"null",
                "address":  "null",
                "coupon_code": event.get("couponCode", "null"),
                "message":event.get("message", "null")

            },
            "referral": BIRTHDAY_TREATS_REFLINK
        }

    def __conciergeReflink_values(self, event):
        return {
            "conversation_summary": "null",
            "unrecognized_retry": "null",
            "intent_id": event.get("intent_id", "null"),
            "referral": "https://www.messenger.com/t/1395480467129397/?ref=concierge" 
        }
    
    def __renewPlanReflink_values(self, event):
        return {
            "renew_plan": {
                "contract_end_date": "null",
                "overdue_balance": "null",
                "last_choice": "null",
                "product": "null" 
            },
            "intent_id": event.get("intent_id", "null"),
            "referral": "https://www.messenger.com/t/1395480467129397/?ref=renewplan" 
        }

    def __changePlan_values(self, event):
        return {
            "account_or_phone_number": event.get("inputNumber", "null"),
            "chosen_plan": "null" 
        }

    def __networkConcern_values(self, event):
        return { 
            "network_concern":{
                # entire house/some part
                "location": event.get("location","null"), 
                "signal": "null", 
                # carousel option
                "issue": event.get("issue","null"),
                "lob":event.get("lobName","null"),
                "visit_time_of_day": event.get("visit_time_of_day","null"),
                "alternate_contact_number":event.get("alternate_contact_number","null"),
                "concern_details":event.get("concern_details","null"),
                "case_number":event.get("case_id","null")
            }
        }

    def __renewPlan_values(self, event):
        return { 
            "renew_plan":{
                "contract_end_date":"null",
                "overdue_balance":"null",
                "last_choice": "null",
                "product": "null",
                "option_selected": event.get("option_selected", "null"),
                "lob": event.get("lob", "null")
            }
        }

    def __myBusinessRegistering_values(self, event):
        return { 
            "state": "MY-BUSINESS-REGISTERING",
            "my_business_faq": { 
                "topic": event.get("business_type", "null"),
                "subtopic": "null"
            }
        }

    def __myBusinessManaging_values(self, event):
        return { 
             "state": "MY-BUSINESS-MANAGING",
             "business_management_topic": event.get("business_topic", "null")  
        }

    def __billsAndPayments_values(self,event):
        return {
            "report_issue": {
                "date_received":"null",
                "load_date": "null",
                "affected_number":"null",
                "load_amount":"null",
                "issue": event.get("issue", "null"),
                "payment_method": "null",
                "load_type": "null",
                "lob": event.get("lastBrand", "null"),
                "case_number": event.get("case_number","null"),
                "bill_number_or_date": event.get("bill_number_or_date","null"),
                "alternate_contact_num": event.get("alternate_contact_num","null"),
                "dispute_amount":event.get("dispute_amount","null")
            }
        }
    
    def __loadPromosAndRewards_values(self,event):
        return {
            "load_concern":{
                "issue": event.get("issue", "null"),
                "transaction_date_time": event.get("transactionDate", "null"),
                "lob": event.get("lobName", "null"),
                "channel_used": event.get("channelUsed", "null"),
                "load_affected": event.get("loadAffected", "null")
            }
        }

    def __upgradePlatinum_values(self, event):
        return {
            "state": event.get("customState", "null"),
            "upgrade_platinum": {
                "name": "null",
                "email": "null",
                "number_brand": event.get("lastBrand", "null"),
                "number": "null",
                "message": "null"
            }
        }

    def __terminateLine_values(self, event):
        return {
            "state": event.get("customState", "null"),
            "termination_reason": "null"
        }

    def __reconnectLine_values(self, event):
        return {
            "reconnect_line": {
                "number": event.get("number", "null"),
                "amount": event.get("amount", "null"),
                "date": event.get("date", "null"),
                "account_number": event.get("accountNumber", "null"),
                "advisory": "null",
                "lob": event.get("lastBrand", "null"),
                "case_id": event.get("caseId", "null"),
                "payment_channel": event.get("paymentChannel", "null")
            }
        }

    def __no_values(self,event):
        return 'noValues'
    
    def put_transaction_start_date(self,event,sessionTools):
        if not event.get('transactionStartDate') or event['transactionStartDate'] == 'String':
            transactionStartDate =  str(get_current_datetime_without_marker())
            sessionTools.update_attributes({ 'transactionStartDate':transactionStartDate })
            return transactionStartDate
        else:
            return event['transactionStartDate']
         
    def put_item(self,event,transaction_status="Success",failed_message="null",retries=0,ttl_days= 10):
        item ={}
        try:
            
            #adding values from state_values based on sessionState
            stateValues = self.__get_state_values(event)
            if stateValues:
                item = self.__get_common_fields(event,transaction_status,failed_message,ttl_days)
                if stateValues != 'noValues':
                    for index, key in enumerate(stateValues):
                        item[list(stateValues.keys())[index]] = list(stateValues.values())[index]

                for object in item:
                    if str(item[object]).lower() == "string" or item[object] is None or str(item[object]).strip() == "":
                        item[object] = "null"
                logger.info(f"KAFKA items:{item}")
                resp = self.ingestion_table.put_item(Item=item)
            else:
                pass

        except ClientError as err:
            if err.response["Error"]["Code"] not in RETRY_EXCEPTIONS:
                raise
            else:
                sleep(2 ** retries)
                retries+=1
                self.put_item(event,transaction_status,failed_message,retries)