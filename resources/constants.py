# brands
UKNOWN_LOB_NAME = "Uknown"
BUSINESS_LOB_NAME = "Business"
BUSINESS_EG_LOB_NAME = "Business EG"
BUSINESS_SG_LOB_NAME = "Business SG"
PLATINUM_MOBIE_LOB_NAME = "Platinum Mobile"
PLATINUM_BB_LOB_NAME = "Platinum Broadband"
POSTPAID_LOB_NAME = "Postpaid"
IN_HOUSE_LOB_NAME = "In House"
PREPAID_LOB_NAME = "Prepaid"
TRAVELER_LOB_NAME = "Traveler"
SHP_LOB_NAME = "SHP"
BB_LOB_NAME = "Broadband"
LANDLINE_LOB_NAME = "Landline"
PREPAID_HOME_WIFI_LOB_NAME = "Prepaid Home Wifi"
TM_LOB_NAME = "TM"
UNREGISTERED_LOB_NAME = "String"

vocBrandLob = {
    POSTPAID_LOB_NAME: "Globe Postpaid",
    PLATINUM_MOBIE_LOB_NAME: "Globe Platinum",
    PREPAID_LOB_NAME: "Globe Prepaid",
    TM_LOB_NAME: "TM",
    BB_LOB_NAME: "Globe At Home Postpaid",
    PREPAID_HOME_WIFI_LOB_NAME: "Globe At Home Prepaid",
    BUSINESS_SG_LOB_NAME: "Globe myBusiness",
    BUSINESS_LOB_NAME: "Globe Business"

}
# brands in list
GAH_LASTBRANDS = [PLATINUM_BB_LOB_NAME, PREPAID_HOME_WIFI_LOB_NAME, BB_LOB_NAME]

# logs
LEX = "LEX"
CUSTOMER = "CUSTOMER"
AGENT = "AGENT" 

# options
accountList = ("i have a globe account", "i have an account",
               "globe account", "i have globe account", "i have account", "register my account",'log in')
inquiryList = ("i have an inquiry", "i have inquiry", "i have a question",
               "i want a plan", "how to get a plan", "i want to apply")

# intents
PLAN_DETAILS_INTENT = "Plan details"
DATA_USAGE_INTENT = "Data usage"
UNBILLED_CHARGES_INTENT = "Unbilled charges"
OUTSTANDING_BALANCE_INTENT = "Amount to pay"
BILL_REQUEST_INTENT = "Send my bill"
PAYMENT_OPTIONS_INTENT = "Payment options"
INSTALLMENT_PAYMENT_INTENT = "Installment payment"
ACCOUNT_NUMBER_INTENT = "Account number"
RECONNECTION_INTENT = "Reconnect line"
REWARDS_INTENT = "Rewards"
NETWORK_INTENT = "Network"
LOAD_BALANCE_INTENT = "Load balance"
PROMOS_INTENT = "My promos"
AGENT_INTENT = "Talk to agent"
TROUBLESHOOTING_INTENT = "Troubleshooting"
BUSINESS_REGISTERING_INTENT = "Business reg"
BUY_LOAD_INTENT = "Buy load"
INSTALLMENT_PAYMENT_INTENT = "Installment payment"
CHICAGO_INTENT = "Chicago"
MENU_INTENT = "Menu"
REPORT_ISSUE_INTENT = "Report an issue"
AMAX_FAQS_INTENT= "AMAX FAQS"
AMAX_FAQS_FOLLOW_UP_INTENT = "AMAX FOLLOW UP"
RENEW_PLAN_INTENT = "Renew my plan"
ASK_5G_INTENT = "What is 5g"
TERMINATE_LINE_INTENT = "Terminate Line"
REPORT_LOAD_CONCERN_INTENT = "Load concern" 
REPORT_PROMO_CONCERN_INTENT = "Promo concern"
REPORT_BILL_CONCERN_INTENT = "Bill concern"
REPORT_OTHER_CONCERN_INTENT = "Other concern"
REPORT_NETWORK_CONCERN_INTENT = 'Network concern'
#Report a problem intent list
reportProblemIntents = [REPORT_LOAD_CONCERN_INTENT, REPORT_PROMO_CONCERN_INTENT, REPORT_BILL_CONCERN_INTENT, REPORT_OTHER_CONCERN_INTENT]

UPGRADE_PLATINUM_INTENT = "Upgrade to Platinum"
SHOP_VOUCHER_INTENT = "shop Voucher"
GAH_TRANSFER_INTENT = "Transfer to GAH"

REPORT_SPAM_INTENT = "report a spam"
REG_UPGRADE_PLAT_INTENT = "reg upgrade plat"
BIRTHDAY_TREATS_INTENT = "birthday treats"
VOUCHER_INTENT = "Voucher"

RECONNECT_LINE_INTENT = 'recconect line'
GO_HEALTH_INTENT= 'Go Health'

CAMPAIGN_1_INTENT = "Campaign 1"
CAMPAIGN_2_INTENT = "Campaign 2"
CAMPAIGN_3_INTENT = "Campaign 3"
CAMPAIGN_4_INTENT = "Campaign 4"

FINANCIAL_CARE_INTENT = "Financial Care"
CHANGE_PLAN_INTENT = 'Change Plan'
OTHER_GLOBE_ACCOUNT_INTENT = "Other globe account"
REG_OTHER_GLOBE_ACCOUNT_INTENT= 'Other globe account - Registration'
# Globe one constants
EVENT_SERVICE_VOICE = "Globe Voice Charge"
EVENT_SERVICE_SMS = "Globe SMS Charge"
EVENT_SERVICE_DATA = "Globe Data Traffic Charge"
EVENT_SERVICE_VAS = "Globe VAS Charge"
EVENT_SERVICE_OTHERS = "Globe Passthrough"

# reflink
GLOBE_ONE_REFLINK = "globeonesupport"
CHICAGO_REFLINK = "donatetofrontliners"
AMAX_RETAILER_REFLINK = "retailer"
BIRTHDAY_TREATS_REFLINK = "birthday"
VOUCHER_REFLINK = "shoor"
UPGRADE_PLATINUM_REFLINK = "upgradetoplatinum"
GAH_PREPAID_REFLINK = "gahprepaidhelp"
GAH_POSTPAID_REFLINK = "gahpostpaidhelp"
GO_HEALTH_REFLINK = 'gohealth'
RECOVERY_REFLINK = "survey"
G1_BILL_DISPUTE_REFLINK = "NG1BillDispute"
G1_REPORT_PAYMENT_REFLINK = "NG1ReportPayment"
G1_LOAD_PROMOS_REWARDS_REFLINK = "NG1LoadPromoRewards"
G1_LOAD_REFLINK = "NG1Load"
G1_PROMOS_REFLINK = "NG1Promo"
G1_REWARDS_REFLINK = "NG1Rewards"
G1_RECONNECT_LINE_REFLINK = "NG1ReconnectLine"
G1_MANAGE_ACCOUNT_REFLINK = "NG1ManageAccount"
G1_NETWORK_REFLINK = "NG1BBNetwork"
G1_FOLLOW_UP_CONCERN_REFLINK = "NG1FollowupConcern"
CONCIERGE_REFLINK = "concierge"
RENEW_PLAN_REFLINK = "renewplan"
CHANGE_PLAN_REFLINK = "changeplan"
GCASH_PLATINUM_REFLINK = 'gcashplatinum'
PLATINUM_UPGRADE_REFLINK = 'platupgrade'
G1_GOFAM_LOAD_PROMOS_REWARDS_REFLINK = "NG1GoFamLoadPromoRewards"

# GAH Integration
GAH_METADATA_SHOP_NOW = "shopNow"
GAH_METADATA_HPW = "hpwCustomer"
GAH_METADATA_POSTPAID = "gahPostpaidCustomer"
GAH_METADATA_ACTIVATE_10 = "hpwActivate10GB"
GAH_METADATA_REGISTER_PROMO = "hpwRegisterPromo"
GAH_METADATA_CHECK_LOAD = "hpwCheckLoad"
GAH_METADATA_SETUP_MODEM = "hpwSetUpModem"
GAH_METADATA_REPORT_NETWORK = "bbReportNetworkIssue"
GAH_METADATA_TRACK_INSTALLATION_STATUS = "bbTrackInstallationStatus"
GAH_METADATA_TRACK_REPAIR_STATUS = "bbTrackRepairStatus"

GAH_INTENT_ACTIVATE_10 = "GAHActivateTenGB"
GAH_INTENT_REGISTER_PROMO = "GAHRegisterPromo"
GAH_INTENT_CHECK_LOAD = "KnowAmountToPay"
GAH_INTENT_SETUP_MODEM = "GAHSetupModem"
GAH_INTENT_REPORT_NETWORK = "Troubleshooting"
GAH_INTENT_TRACK_INSTALLATION_STATUS = "GAHTrackInstallationStatus"
GAH_INTENT_TRACK_REPAIR_STATUS = "GAHTrackRepairStatus"

gahIntentMap = {
    GAH_INTENT_ACTIVATE_10: GAH_METADATA_ACTIVATE_10,
    GAH_INTENT_REGISTER_PROMO: GAH_METADATA_REGISTER_PROMO,
    GAH_INTENT_CHECK_LOAD: GAH_METADATA_CHECK_LOAD,
    GAH_INTENT_SETUP_MODEM: GAH_METADATA_SETUP_MODEM,
    GAH_INTENT_REPORT_NETWORK: GAH_METADATA_REPORT_NETWORK,
    GAH_INTENT_TRACK_INSTALLATION_STATUS: GAH_METADATA_TRACK_INSTALLATION_STATUS,
    GAH_INTENT_TRACK_REPAIR_STATUS: GAH_METADATA_TRACK_REPAIR_STATUS
}

CAMPAIGN_1_REFLINK = "campaign1"
CAMPAIGN_2_REFLINK = "campaign2"
CAMPAIGN_3_REFLINK = "campaign3"
CAMPAIGN_4_REFLINK = "campaign4"

# SNS
SNS_MESSAGE = "[LEX] {env}|{alarm_type}|{date}|{time}|{channel}|{fbId}|{message}"
# alarm types
SNS_ALARM_GLOBEONETOKEN_ERROR = "ERROR - G1 Token"
SNS_ALARM_GLOBEONE_ANON_TOKEN_ERROR = "ERROR - G1 Anonymous Token"
SNS_ALARM_VOC_TOKEN_ERROR = "ERROR - VOC Token"
SNS_ALARM_BCP_ERROR = "ERROR - BCP"
SNS_ALARM_SOIC_IN_SESSION_USERS = "SOIC - In Session Users Count"
SNS_ALARM_SOIC_STATECHECKER_REPORTS = "SOIC - Statechecker Reports"

# NIA Intents
REPORT_A_PROBLEM_INTENT = "Report a Problem Submenu"
OTHER_REQUESTS_INTENT = "Other Requests Submenu"
ACCOUNT_INFORMATION_INTENT = "Account Information Submenu"

#Submenu
subMenuList =["report a problem", "manage my plan", "check details", "see other options", "go to previous menu"]
payloadMenu = ["[menu].report a problem", "[menu].manage my plan", "[menu].check details", "[menu].see other options", "[menu].go to previous menu", "[menu].exclusive offers"]

NETWORK_CONCERN = "[menu].NetworkConcern"
LOAD_CONCERN = "[menu].LoadConcern"
PROMO_CONCERN = "[menu].PromoConcern"
BILL_CONCERN = "[menu].BillConcern"
OTHER_CONCERNS = "[menu].OtherConcerns"
GCASH_CONCERN = "[menu].GcashConcern"

reportAProblemSubMenuIds = [NETWORK_CONCERN, LOAD_CONCERN, PROMO_CONCERN, BILL_CONCERN, NETWORK_CONCERN, OTHER_CONCERNS, GCASH_CONCERN]

MENU_ID_ACCT_NUM = "[menu].AccountNumber"
MENU_IDS_ACCT_INFO = [
    MENU_ID_ACCT_NUM
]

MENU_ID_TERMINATE_LINE = "[menu].TerminateLine"
MENU_IDS_OTHER_REQUESTS = [
    MENU_ID_TERMINATE_LINE
]

MENU_ID_RENEW_PLAN = "[menu].RenewPlan"

MENU_ID_EXCESS_CHARGES = "[menu].ExcessCharges"

MENU_ID_CHANGE_PLAN = '[menu].ChangePlan'

MENU_ID_OTHER_GLOBE_ACCOUNT = '[menu].changeAccount'

MENU_ID_GAH_OFFERS = '[menu].gah offer'

MENU_ID_KNOW_CONTRACT_END_DATE = "[menu].ContractEndDate"

# persistent menu
BUTTON_MY_GLOBE_ACCOUNT = "My Globe Account"
PAYLOAD_MY_GLOBE_ACCOUNT = "[persistentMenu].myGlobeAccount"
BUTTON_SHOP_PLANS_OFFERS = "Shop Plans & Offers"
PAYLOAD_SHOP_PLANS_OFFERS= "[persistentMenu].shopPlansOffers"

# Redeem Rewards
REDEEM_REWARDS_INTENT = "Redeem Rewards"
REPORT_GCASH_CONCERN_INTENT = "GCash concern"

# Check Application Status
CHECK_APPLICATION_STATUS_INTENT = "Check application status"

# Know Contract End Date
CONTRACT_END_DATE_INTENT = "Know Contract End Date"

SKIP_EDUCATION_INTENTS = [ASK_5G_INTENT, BILL_REQUEST_INTENT, PAYMENT_OPTIONS_INTENT, OUTSTANDING_BALANCE_INTENT, AMAX_FAQS_FOLLOW_UP_INTENT, UPGRADE_PLATINUM_INTENT,SHOP_VOUCHER_INTENT,RENEW_PLAN_INTENT,REPORT_SPAM_INTENT,GO_HEALTH_INTENT,RECONNECT_LINE_INTENT, REDEEM_REWARDS_INTENT, REPORT_GCASH_CONCERN_INTENT, CHECK_APPLICATION_STATUS_INTENT, CONTRACT_END_DATE_INTENT]
# this will have .format(timelog=... , senderId=... , lastNumber=... , lastBrand=... , source=... , facebookmessenger=... , lastIntent=... , sessionState=... , subState=... , channel=... , lastIntentDate=... , details=... , messageText )
LOG_PARSE = "[INFO], {timelog}|{senderId}|{lastNumber}|{lastBrand}|{source}|{facebookmessenger}|{lastIntent}|{sessionState}|{subState}|{channel}|{lastIntentDate}|{details}|{messageText}"

# Chicago V2
CHICAGO_V2_INTENT = "Christmas"
CHICAGO_V2_REFLINK = "christmas"

#reports type constants
REPORTS_TRANSFERED_TO_AGENT_TYPE= 'Count of missed intent transfers with agent DPN'

# Unregistered Intent Recognition
REGISTRATION_BUTTONS = ["log in", "shop now"]

APPLY_NEW_LINE_INTENT = "Apply new line"



# ************************************************************************************************************************
# ************************************************* NIAS 2.0 *************************************************************
# ************************************************************************************************************************
LOSTPHONE_OR_SIM_INTENT = "lost phone or sim"
ACTIVATE_FREEBIES_INTENT = "activate freebies"
HOW_TOS_INTENT = "how to"
SPAM_OR_SCAM_INTENT = "report spam or scam"
ACTIVATE_SIM_INTENT ="activate sim"
NETWORK_CONCERN_INTENT ="network concern"
CHECK_APPLICATION_INTENT = "check application"
FOLLOWUP_CONCERN_INTENT = "follow-up concern"
TECHNICIAN_VISIT_INTENT = "technician visit"
RECONNECT_MY_LINE_INTENT = "reconnect line"
RENEW_PLAN_INTENT = "renew plan"
APPLY_NEW_LINE_INTENT = "apply a new line"
BUY_LOAD_OR_PROMO_INTENT = "buy load or promo"
TRANSFER_OWNERSHIP_INTENT = "transfer ownership"
REPLACE_RETURN_DEVICE_INTENT = "replace or return device"
ACCOUNT_OTHERS_INTENT = "account others"
ACCOUNT_FOLLOWUP_INTENT = "account followup"
UNLOCK_DEVICE_INTENT = "unlock device"
PORT_NUMBER_INTENT = "port number"
LOAD_PROMOS_AND_REWARDS_INTENT = "load, promos and rewards"
BILLS_AND_PAYMENTS_INTENT = "bills and payments"
MODIFY_OR_TERMINATE_INTENT = "modify or terminate"
GCASH_CONCERN_INTENT = "gcash concern"
CHECK_BALANCE_INTENT = "check balance"
ACCOUNT_REQUESTS_INTENT = "account requests"
REGISTER_SIM_INTENT = "register sim"
FAQ_SIM_INTENT = "faq sim"
ISSUE_WITH_SIM_INTENT = "issue with sim"
SESSION_STATUS_ACTIVE = "ACTIVE"
SESSION_STATUS_IDLE = "IDLE"
SESSION_STATUS_TICKET_CLOSURE = "TICKET_CLOSURE"

session_status_list = [SESSION_STATUS_ACTIVE, SESSION_STATUS_IDLE, SESSION_STATUS_TICKET_CLOSURE]

VALID_ACCOUNTNO_REGEX = '^([0-9]{8,10})$'
FB_ERROR_CODE_RATE_LIMIT_REACHED = 4
STATUS_RED = "RED"
STATUS_GREEN = "GREEN"

OPEN_CASE_STATUS_WITHIN = 'WITHIN'
OPEN_CASE_STATUS_BEYOND = 'BEYOND'
OPEN_CASE_STATUS_NO_CASE ='NOCASE'
OPEN_CASE_STATUS_NOT_EXISTING = 'NOTEXISTING'

POSTPAID_ACCOUNT_BRANDS = [PLATINUM_MOBIE_LOB_NAME, POSTPAID_LOB_NAME]
BROADBAND_ACCOUNT_BRANDS = [PLATINUM_BB_LOB_NAME, SHP_LOB_NAME, BB_LOB_NAME]
ACCOUNT_BRANDS = [*POSTPAID_ACCOUNT_BRANDS, *BROADBAND_ACCOUNT_BRANDS, BUSINESS_SG_LOB_NAME]
ACCOUNT_BRANDS_FOR_SENIOR = [*POSTPAID_ACCOUNT_BRANDS, *BROADBAND_ACCOUNT_BRANDS]

CONNECT_LMB_REQUEST = {
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

LEX_BOT_PAYLOAD = {
    "dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
        "message":{
            "contentType": "PlainText",
            "content": "Default message"
        }
    }
}

#THEA PLATINUM UPGRADE
THEA_PLATINUM_OLD_PHONE_TRAVEL = 'Old_Phone - Travel'
THEA_PLATINUM_OLD_PHONE_SHOPPING = 'Old_Phone - Shopping'
THEA_PLATINUM_OLD_PHONE_RESTAURANT = 'Old_Phone - Restaurant'
THEA_PLATINUM_NEW_PHONE_SHOPPING = 'New_Phone - Shopping'

THEA_PLATINUM_UPGRADE_CAROUSEL = {
    THEA_PLATINUM_OLD_PHONE_TRAVEL: 'thea-offer1-old-phone-travel',
    THEA_PLATINUM_OLD_PHONE_SHOPPING: 'thea-offer1-old-phone-shopping',
    THEA_PLATINUM_OLD_PHONE_RESTAURANT: 'thea-offer1-old-phone-restaurant',
    THEA_PLATINUM_NEW_PHONE_SHOPPING: 'thea-offer1-new-phone-shopping'
}

THEA_PLATINUM_UPGRADE_PLAN_OFFERS = {
    THEA_PLATINUM_OLD_PHONE_TRAVEL: 'Platinum GPlan Plus 3799',
    THEA_PLATINUM_OLD_PHONE_SHOPPING: 'Platinum GPlan Plus 3799',
    THEA_PLATINUM_OLD_PHONE_RESTAURANT: 'Platinum GPlan Plus 3799',
    THEA_PLATINUM_NEW_PHONE_SHOPPING: 'Platinum GPlan Plus 3799'
}


THEA_PLATINUM_UPGRADE_REPORT_LOGGING = {
    'index_status': 'success',
    'registered_status': '',
    'registered_date': '',
    'response_tagging_offer1': '',
    'response_date_offer1': '',
    'response_tagging_offer2': '',
    'response_date_offer2': '',
    'plan_summary_offer1': '',
    'plan_summary_date_offer1': '',
    'plan_summary_offer2': '',
    'plan_summary_date_offer2': '',
    'free_thea': '',
    'free_thea_date': '',
    'transacted_status': '',
    'transacted_date': '',
    'free_thea_expiry': ''
}

GO_TO_MENU = "go to menu"
CHAT_WITH_AGENT = "chat with agent"

#PREPAID FIBER
OTHERS_PREPAID_FIBER = '[menu].othersprepaidfiber'
OTHERS_OTHER_ACCOUNT = '[menu].othersotheraccount'
NETWORK_PREPAID_FIBER = '[menu].networkprepaidfiber'
NETWORK_OTHER_ACCOUNT = '[menu].networkotheraccount'
MODIFY_OR_TERMINATE_PREPAID_FIBER = '[menu].modifyandterminateprepaidfiber'
MODIFY_OR_TERMINATE_OTHER_ACCOUNT = '[menu].modifyandterminateotheraccount'
RECONNECT_LINE_PREPAID_FIBER  = '[menu].reconnectprepaidfiber'
RECONNECT_LINE_OTHER_ACCOUNT = '[menu].reconnectotheraccount'
LPR_PREPAID_FIBER = '[menu].lprprepaidfiber'
LPR_OTHER_ACCOUNT = '[menu].lprotheraccount'
BILL_PREPAID_FIBER = '[menu].billprepaidfiber'
BILL_OTHER_ACCOUNT = '[menu].billotheraccount'
FOLLOW_UP_PREPAID_FIBER = '[menu].followupprepaidfiber'
FOLLOW_UP_OTHER_ACCOUNT = '[menu].followupotheraccount'

# CEM SCENE DESCRIPTIONS
ROOT_CAUSE_NOT_FOUND = "The root cause is not found"
NO_MATCHED_DATA_IS_FOUND = "No matched data is found"
NO_OBVIOUS_ISSUE_FOUND = "No_obvious_issue_found"
NO_ISSUE = "No_Issue"
DATA_SERVICE_IS_NOT_SUBSCRIBED = "Data_service_is_not_subscribed"
LONG_DELAY_BY_TERMINAL = "LongDelay_by_Terminal"
MTSMS_ABSENT_SUBSCRIBER = "Called_party(B-num)_unreachable_Absent_Subscriber_Memory_Capacity_Exceeded_Service_Barring_etc(MTSMS_AbsentSubscriber)"
TERMINAL_ISSUE_SLOW_BROWSING = "Terminal_issue-Slow_Browsing"
NO_SIGNAL_ISSUE_FOUND = "No_Signal_issue_found"
CS_CALL_FAIL_CALLED_PARTY_NOT_REACHABLE = "CSCallFail_CalledPartyNotReachable"
CS_CALL_FAIL_NETWORK_FAILURE = "CSCallFail_NetworkFailure"
USER_ISSUE_NO_SERVICE_REQUEST = "User_issue-No_Service_Request"