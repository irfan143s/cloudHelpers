
import json
import uuid
from time import sleep
from datetime import datetime, timedelta
from botocore.exceptions import ClientError
import boto3
import dateutil.tz
from resources.states import *
from resources.constants import *
from resources.spiels import *
from configuration import *
#STREAM:
DPN_VERBOSE = "Data Privacy Notice"
TRANSFER_VERBOSE = "Transfer to Agent"

tz_ph=dateutil.tz.gettz(TIMEZONE_PH)
RETRY_EXCEPTIONS = ('ProvisionedThroughputExceededException',
                    'ThrottlingException')

#constant values to be transfered to resources constants
VERBOSE_STATE = {
    DPN_STATE: DPN_VERBOSE,
    REG_STATE: "Registration",
    OTP_STATE: OTP_STATE,
    INTENT_STATE: "Intent Recognition",
    BUY_LOAD_STATE: "Buy Load",
    PAY_BILL_STATE: "Payment Options",
    INTENT_OTP_STATE: OTP_STATE,
    TRANSFER_STATE: "Transfer to Agent",
    MYB_MANAGING_STATE: "myBusiness Managing",
    LANG_STATE: "Language Option",
    REPORT_STATE: "Report Issue",
    SHOP_VOUCHER_STATE: "Shop Voucher",
    RENEW_PLAN_STATE: "Renew Plan Multiple Account",
    RENEW_ONE_ACCOUNT_STATE: "Renew Plan One Account",
    REPORT_SPAM_STATE: "Report Spam",
    BIRTHDAY_TREATS_STATE: "Birthday Treats",
    TERMINATE_LINE_STATE: "Terminate Line",
    RECONNECT_LINE_STATE: "Reconnect Line",
    GO_HEALTH_STATE: "GoHealth",
    OTHER_GLOBE_ACCOUNT_STATE: "Other Globe Account",
    REFLINK_DPN_STATE: DPN_VERBOSE,
    REFLINK_TRANSFER_STATE: TRANSFER_VERBOSE,
    REFLINK_STATE: "Reflink",
    INSTALLMENT_PAYMENT_STATE: "Installment Payment",
    REGFFUP_STATE: "Follow up",
    CHICAGO_STATE: "Chicago V1",
    AMAX_FAQS_STATE: "AMAX FAQs",
    VOUCHER_STATE: VOUCHER_INTENT,
    UPGRADE_PLATINUM_STATE: "Upgrade to Platinum",
    CAMPAIGN_1_STATE: CAMPAIGN_1_INTENT,
    CAMPAIGN_2_STATE: CAMPAIGN_3_INTENT,
    CAMPAIGN_3_STATE: CAMPAIGN_3_INTENT,
    CAMPAIGN_4_STATE: CAMPAIGN_4_INTENT,
    GAH_TRANSFER_STATE: GAH_TRANSFER_INTENT,
    CHICAGO_V2_STATE: "Chicago V2",
    REPORT_A_PROBLEM_STATE: "Report a Problem",
    OTHER_REQUESTS_STATE: "Other Requests",
    ACCOUNT_INFORAMTION_STATE: "Account Information",
    ACCOUNT_NUMBER_STATE: "Get Account Number",
    GET_REWARDS_STATE: "Get Rewards",
    CHANGE_PLAN_STATE: CHANGE_PLAN_INTENT,
    TERMINATE_LINE_STATE: TERMINATE_LINE_INTENT,
    REDEEM_REWARDS_STATE: REDEEM_REWARDS_INTENT,
    CONTRACT_END_DATE_STATE: CONTRACT_END_DATE_INTENT,
    CHECK_APPLICATION_STATUS_STATE: CHECK_APPLICATION_STATUS_INTENT,
    APPLY_NEW_LINE_STATE: "Apply New Line"
}

VERBOSE_STATE ={**VERBOSE_STATE, **dict.fromkeys(MYB_REGISTERING_LIST,'myBusiness Registering'), **dict.fromkeys(BTS_LIST,'Troubleshooting') }


VERBOSE_WORKBASKET = {
    # myBusiness Workbaskets
    "0200": "FB Pr SG Main",
    "0201": "FB Pr SG Postpaid",
    "0202": "FB Pr Prepaid Care and Tech",
    "0203": "FB Pr SG Wireline",
    "0204": "FB Pr THEA Postpaid",
    # GT Workbaskets
    "0100": "FB Pr Main",
    "0101": "FB Pr Postpaid Care and Tech",
    "0102": "FB Pr Prepaid Care and Tech",
    "0103": "FB Pr BB Care and Tech",
    "0104": "FB Pr THEA Postpaid",
    # Thea Workbaskets
    "0300": "FB Pr THEA Postpaid",
    "0301": "FB Pr Postpaid Care and Tech",
    "0302": "FB Pr Prepaid Care and Tech",
    "0303": "FB Pr BB Care and Tech",
    "0304": "FB Pr THEA Postpaid",
    "0305": "FB Pr THEA Aspire"
}

DELETE_MAP_VALUES={
    BUY_LOAD_STATE:{
            'buyload':['msisdn','lobName','wallet','amaxToken','amount','paymentId','paymentMethod']
    },
    CHICAGO_STATE:{
            'chicago':['benificiary','gift','noteName','success','quantity']
    },
    CHECK_APPLICATION_STATUS_STATE:{
        'application_status':['full_name','email']
    },
    SHOP_VOUCHER_STATE:{
        'shop_voucher':['items']
    },
    BIRTHDAY_TREATS_STATE:{
        'birthday_treats':['address','coupon_code']
    },
    RECONNECT_LINE_STATE:{
        'reconnect_line':['number','amount','date','account_number']
    },
    UPGRADE_PLATINUM_STATE:{
        'upgrade_platinum':['name','email','number_brand','number'],
        "upgradePlatinum": ["name", "email", "numberBrand", "number"]
    },
    REPORT_STATE:{
        'report_issue':['date_received','load_date','affected_number','load_amount','issue','payment_method','load_type']
    },
    RENEW_PLAN_STATE:{
        'rpma':['business','name','contact_number','email_add','multiple_renew']
    },
    RENEW_ONE_ACCOUNT_STATE:{
        'renew_plan':['contract_end_date','overdue_balance','last_choice','product']
    },
    RENEW_PLAN_ADVISORY_STATE:{},
    OTHER_GLOBE_ACCOUNT_STATE:{},
    GO_HEALTH_STATE:{},
    BTS_STATE:{},
    GAH_TRANSFER_STATE:{},
    TRANSFER_STATE:{},
    TERMINATE_LINE_STATE:{},
    CHANGE_PLAN_STATE:{},
    REPORT_A_PROBLEM_STATE:{
        'network_concern':['location','signal','issue'],
        'load_concern':['issue','date_time'],
        'promo_concern':['promo','date_time'],
    },
    AMAX_FAQS_STATE:{
        'transaction_history':['email','last_number']
    },
    REFLINK_STATE:{},
    PAY_BILL_STATE:{},
    MYB_REGISTERING_STATE:{
        'my_business_faq':['topic','subtopic']
    },
    MYB_MANAGING_STATE:{},
}

DELETE_ATTRIBUTES = {
    BUY_LOAD_STATE:[],
    CHICAGO_STATE:[],
    CHECK_APPLICATION_STATUS_STATE:[],
    SHOP_VOUCHER_STATE:[],
    BIRTHDAY_TREATS_STATE:[],
    RECONNECT_LINE_STATE:[],
    UPGRADE_PLATINUM_STATE:[],
    REPORT_STATE:[],
    RENEW_PLAN_STATE:[],
    RENEW_ONE_ACCOUNT_STATE:[],
    RENEW_PLAN_ADVISORY_STATE:[],
    OTHER_GLOBE_ACCOUNT_STATE:[],
    GO_HEALTH_STATE:['go_health_pax'],
    BTS_STATE:['troubleshooting_concern'],
    GAH_TRANSFER_STATE:['gah_metadata'],
    TRANSFER_STATE:['intent_id'],
    TERMINATE_LINE_STATE:['termination_reason'],
    CHANGE_PLAN_STATE:['chosen_plan'],
    REPORT_A_PROBLEM_STATE:['report_problem_concern','bill_concern','other_concern'],
    AMAX_FAQS_STATE:['chosen_faq'],
    REFLINK_STATE:[],
    PAY_BILL_STATE:['payment_option'],
    MYB_REGISTERING_STATE:['business_type'],
    MYB_MANAGING_STATE:['business_management_topic'],
    }

AMAX_FAQ_MAP = {
    FAQ_TRANSACTION_LABEL: "Transaction History",
    FAQ_AMAX_RETAILER_LABEL: "AMAX Earn",
    FAQS_DENOMINATIONS_LABEL: "Denominations",
    FAQ_AMAX_ACCOUNT_LABEL: "AMAX Requirements",
    FAQ_CHANGE_SIM_LABEL: "Change Sim",
    FAQ_ACCOUNT_DETAIL_LABEL: "Account Details"
}
class StreamTools:

    def __init__(self,table_name,region=REGION):
        self.dynamodb = boto3.resource("dynamodb", region_name=region)
        self.ingestion_table = self.dynamodb.Table(table_name)

    def get_common_fields(self,event,transaction_status="Success",failed_message="string"):
        #now = datetime.now(tz=tz_ph)
        #TTL = now + timedelta(days=365)
        return {
            'ps_id':event.get('fbId','string'),
            'account_or_phone_number':event.get('lastNumber','string'),
            'brand':event.get('lastBrand','string'),
            'state':VERBOSE_STATE(event.get('sessionState','string')),
            'substate':event.get('subState','string'),
            'channel':pageDictionary.get(event.get('channel','string'),'string'),
            'last_intent':event.get('lastIntent','string'),
            'registered_date':event.get('registeredDate','string'),
            'jr_date':event.get('jrDate','string'),
            'new_user_date':event.get('newUserDate','string'),
            'in_session':event.get('inSession','string'),
            'education_date':event.get('educationalDate','string'),
            'retry':event.get('retry','string'),
            'intent_source':event.get('intentSource','string'),
            'language_option':event.get('languageOption','English'),
            'transaction_start_date':event.get("transaction_start_date",'{}').get(event.get('sessionState','string'),'string'),
            'transaction_status':transaction_status, #Success or Failed
            'failed_message':failed_message,
            #'TTL':int(TTL),
        }
    
    def put_item(self,item:dict,retries=0,ttl_days=365):
        now = datetime.now(tz=tz_ph)
        item['timestamp_utc_8'] = now.strftime("%Y-%m-%dT%H:%M:%S%z")
        TTL = now + timedelta(days=ttl_days)
        item['TTL'] = int(TTL.timestamp())
        item['uuid']= str(uuid.uuid4())

        try:
            resp = self.ingestion_table.put_item(Item=item)
        except ClientError as err:
            if err.response['Error']['Code'] not in RETRY_EXCEPTIONS:
                raise
            else:
                sleep(2 ** retries)
                retries+=1
                self.put_item(item,retries)


    def batch_write(self,items:list,ttl_days=365):

        with self.ingestion_table.batch_writer() as batch:
            for item in items:
                now = datetime.now(tz=tz_ph)
                TTL = now + timedelta(days=ttl_days)
                item['timestamp_utc_8'] = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
                item['TTL'] = int(TTL.timestamp())
                item['uuid']= str(uuid.uuid4())
                batch.put_item(Item=items)


    def convert_other_registered_numbers(self,otherRegisteredNumbers):
        """
        Input:
            event["otherRegisteredNumber"] or sessionAttributes["otherRegisteredNumber"] in this format:
            {
                "Postpaid": {
                    "917xxxxxxx": {
                        "registeredDate": "String"
                    }
            }
        Output:
            Reformatted version of otherRegistedNumber to follow this format:
            {
                "brand": "Postpaid",
                "number: "917xxxxxxx",
                "registered_date": "String"
            }
        """
        parsed_registered_numbers = []
        for brand, numbers in otherRegisteredNumbers.items():
            for number, values in numbers.items():
                parsed_number = {
                    "brand": brand,
                    "number": number,
                    "registered_date": values("registeredDate", "")
                }

                parsed_registered_numbers.append(parsed_number)

        return parsed_registered_numbers
            
    def get_state_values(self,event):
        #STREAM: for pop back and persistent menu
        state_values = {
            BUY_LOAD_STATE:self.buyload_values,
            CHICAGO_STATE:self.chicago_values,
            CHECK_APPLICATION_STATUS_STATE:self.checkApplicationStatus_values,
            SHOP_VOUCHER_STATE:self.shopVoucher_values,
            BIRTHDAY_TREATS_STATE:self.birthdayTreats_values,
            RECONNECT_LINE_STATE:self.reconnectLine_values,
            UPGRADE_PLATINUM_STATE:self.upgradePlatinum_values,
            REPORT_STATE:self.reportIssue_values,
            RENEW_PLAN_STATE:self.rpma_values,
            RENEW_ONE_ACCOUNT_STATE:self.renewPlan_values,
            RENEW_PLAN_ADVISORY_STATE: self.renewPlanAdvisory_values,
            OTHER_GLOBE_ACCOUNT_STATE:self.otherRegisteredNumbers_values,
            GO_HEALTH_STATE:self.goHealth_values,
            BTS_STATE: self.troubleshooting_values,
            GAH_TRANSFER_STATE:self.transferToGAH_values,
            TRANSFER_STATE:self.transferToAgent_values,
            TERMINATE_LINE_STATE:self.terminateLine_values,
            CHANGE_PLAN_STATE:self.changePlan_values,
            REPORT_A_PROBLEM_STATE:self.reportProblem_values,
            AMAX_FAQS_STATE:self.amaxFaqs_values,
            REFLINK_STATE:self.reflink_values,
            PAY_BILL_STATE:self.paymentOptions_values,
            MYB_REGISTERING_STATE:self.myBusinessRegistering_values,
            MYB_MANAGING_STATE:self.myBusinessManaging_values
        }

        return state_values[event['sessionState']](event)


    def buyload_values(self,event):
        buyload = event.get('buyload',{})
        return {
            'buy_load':{
                'msisdn':buyload.get('msisdn',""),
                'lob_name':buyload.get('lobName',""),
                'wallet':buyload.get('wallet',""),
                'amax_token':buyload.get('amaxToken',""),
                'amount':buyload.get('amount',""),
                'payment_id':buyload.get('paymentId',""),
                'payment_method':buyload.get('paymentMethod',""),
            }
        }

    def chicago_values(self,event):
        chicago = event.get('chiacgo',{})
        return {
            'chicago':{
                'beneficiary':chicago.get('benificiary',""),
                'gift':chicago.get('gift',""),
                'note_name':chicago.get('noteName',""),
                'success':chicago.get('success',""),
                'quantity':chicago.get('quantity',""),
            }
        }

    def checkApplicationStatus_values(self, event):
        applicationStatus = event.get("applicationStatus", {})
        return {
            "application_status": {
                "full_name": applicationStatus.get("fullName", ""),
                "email": applicationStatus.get("email", ""),
            }
        }
        
    def shopVoucher_values(self, event):
        shopVoucher = event.get("shopVoucher", {})
        return {
            "shop_voucher": {
                "items": shopVoucher.get("items", [])
            }
        }
        
    def birthdayTreats_values(self, event):
        birthdayTreats = event.get("birthdayTreats", {})
        return {
            "birthday_treats": {
                "second_time_flag": birthdayTreats.get("2ndTimeFlag", ""),
                "address": birthdayTreats.get("address", ""),
                "coupon_code": birthdayTreats.get("CouponCode", "")
            }
        }
        
    def reconnectLine_values(self, event):
        reconnectLine = event.get("reconnectLine", {})
        return {
            "reconnect_line": {
                "number": reconnectLine.get("number", ""),
                "amount": reconnectLine.get("amount", ""),
                "date": reconnectLine.get("date", ""),
                "account_number": reconnectLine.get("accountNumber", ""),
                "advisory": event.get("reconnectAdvisory", ""),
            }
        }
        
    def upgradePlatinum_values(self, event):
        upgradePlatinum = event.get("upgradePlatinum", {})
        return {
            "upgrade_platinum": {
                "name": upgradePlatinum.get("fullName", ""),
                "email": upgradePlatinum.get("email", ""),
                "number_brand": upgradePlatinum.get("numberBrand", ""),
                "number": upgradePlatinum.get("number", "")
            }
        }
        
    def reportIssue_values(self, event):
        reportIssue = event.get("reportIssue", {})
        issue = event.get("spielId", "")

        PAYMENT_METHOD_MAP = {
            REPORT_NO_LOAD_LABEL: reportIssue.get("paymentMethod", "")
        }

        LOAD_TYPE_MAP = {
            REPORT_NO_TEXT_LABEL: reportIssue.get("paymentMethod", ""),
            REPORT_DOUBLE_TRANS_LABEL: reportIssue.get("paymentMethod", "")
        }

        return {
            "report_issue": {
                "date_received": reportIssue.get("dateReceived", ""),
                "load_date": reportIssue.get("loadDate", ""),
                "affected_number": reportIssue.get("affectedNumber", ""),
                "load_amount": reportIssue.get("loadAmount", ""),
                "issue": issue,
                "payment_method": PAYMENT_METHOD_MAP.get(issue, ""),
                "load_type": LOAD_TYPE_MAP.get(issue, "")
            }
        }
        
    def rpma_values(self, event):
        rpma = event.get("RPMA", {})
        return {
            "rpma": {
                "business": rpma.get("Business", ""),
                "name": rpma.get("Name", ""),
                "contact_number": rpma.get("ContactNumber", ""),
                "email_add": rpma.get("EmailAdd", ""),
                "multiple_renew": rpma.get("MultipleRenew", "")
            }
        }
        
    def renewPlan_values(self, event):
        renewPlan = event.get("renewPlan", {})
        return {
            "renew_plan": {
                "contract_end_date": renewPlan.get("contractEndDate", ""),
                "overdue_balance": renewPlan.get("overdueBalance", ""),
                "last_choice": renewPlan.get("lastChoice", ""),
                "product": renewPlan.get("product", "")
            }
        }

    def renewPlanAdvisory_values(self, event):
        return {
            "renew_plan_advisory": event.get("renewPlanAdvisoryDate", "")
        }

    def otherRegisteredNumbers_values(self, event):
        otherRegisteredNumbers = event.get("otherRegisteredNumber", {})

        return self.convert_other_registered_numbers(otherRegisteredNumbers)
        
    def goHealth_values(self, event):
        return {
            "go_health_pax": event.get("goHealthPax", "")
        }
    
    def troubleshooting_values(self, event):
        return {
            "troubleshooting_concern": event.get("btsConcern", "")
        }
    
    def transferToGAH_values(self, event):
        return {
            "gah_metadata": event.get("gahMetadata", "")
        }
    
    def transferToAgent_values(self, event):
        return {
            "conversation_summary": event.get("conversationSummary", []),
            "intent_id": VERBOSE_WORKBASKET.get(event.get("intentId", ""), ""),
            "unrecognized_retry": event.get("unrecognizedRetry", "")
        }
    
    def terminateLine_values(self, event):
        return {
            "termination_reason": event.get("terminateReason", "")
        }
    
    def changePlan_values(self, event):
        return {
            "chosen_plan": event.get("changePlan", "")
        }
    
    def reportProblem_values(self, event):
        concern = event.get("menuId", "")
        networkConcern = event.get("networkConcern", {})
        loadConcern = event.get("loadConcern", {})
        promoConcern = event.get("promoConcern", {})

        return {
            "report_problem_concern": concern.replace("[menu].", ""),
            "network_concern": { "location": "", "signal": "", "issue": ""}
                if concern != NETWORK_CONCERN else {
                    "location": networkConcern.get("location", ""),
                    "signal": networkConcern.get("signal", ""),
                    "issue": networkConcern.get("issue", "")
                },
            "load_concern": { "issue": "", "date_time": "" } if concern != LOAD_CONCERN else {
                "issue": loadConcern.get("issue", ""), 
                "date_time": loadConcern.get("dateTime", "")
            },
            "promo_concern": { "promo": "", "date_time": "" } if concern != PROMO_CONCERN else {
                "promo": promoConcern.get("promo", ""), 
                "date_time": promoConcern.get("dateTime", "")
            },
            "bill_concern": "" if concern != BILL_CONCERN else event.get("billConcern", ""),
            "other_concern": "" if concern != OTHER_CONCERNS else event.get("otherConcern", "")
        }
    
    def amaxFaqs_values(self, event):
        faq = event.get("amaxFaq", "")
        return {
            "chosen_faq": AMAX_FAQ_MAP.get(faq, ""),
            "transaction_history": { "email": "", "last_number": "" } if faq != FAQ_TRANSACTION_LABEL else {
                "email": event.get("transactEmail", ""), 
                "last_number": event.get("lastNumber", "")
            }
        }
    
    def reflink_values(self, event):
        return {
            "referral": event.get("referral", "")
        }

    def paymentOptions_values(self, event):
        return {
            "payment_option": event.get("payOption", "")
        }
    
    def myBusinessRegistering_values(self, event):
        business = event.get("businessType", "")
        faq = event.get("yodaFaq", {})
        return {
            "business_type": business ,
            "my_business_faq": { "topic": "", "subtopic": "" } if business else {
                "topic": faq.get("topic", ""), 
                "subtopic": faq.get("subtopic", "")
            }
        }
    
    def myBusinessManaging_values(self, event):
        return {
            "business_management_topic": event.get("businessManage", "")
        }