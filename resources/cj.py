#NIAS 2.0
from configuration import *
from resources.constants import *

CJ_NO_FLOW = "no-flow"
CJ_NO_BRAND = "no-brand"
CJ_ENTER_CONCERNED_NUMBER = "enter-concerned-number"
CJ_ANSWERED_SURVEY = "answered-survey"

CJ_NETWORK_CONCERN = "network-concern"
CJ_LOAD_PROMO_REWARDS = "load-promo-rewards"
CJ_BILL_AND_PAYMENTS = "bill-and-payments"
CJ_RECONNECT_MY_LINE = "reconnect-my-line"
CJ_MODIFY_OR_TERMINATE = "modify-or-terminate"
CJ_MODIFY_OR_TERMINATE_POSTPAID_ESIM = "modify-or-terminate-postpaid-esim"
CJ_MODIFY_OR_TERMINATE_PREPAID_ESIM = "modify-or-terminate-prepaid-esim"
CJ_ACCOUNT_REQUESTS = "account-requests"
CJ_CHECK_BALANCE = "check-balance"
CJ_CHECK_APPLICATION = "check-application"
CJ_FOLLOWUP_A_CONCERN = "followup-a-concern"
CJ_TECHNICIAN_VISIT = "technician-visit"
CJ_RENEW_MY_PLAN = "renew-my-plan"
CJ_APPLY_FOR_A_NEW_LINE = "apply-for-a-new-line"
CJ_BUY_LOAD_OR_PROMOS = "buy-load-or-promos"
CJ_ACTIVATE_SIM = "activate-sim"
CJ_ACTIVATE_FREEBIES = "activate-freebies"
CJ_HOW_TO = "how-to"
CJ_REPORT_SPAM_OR_SCAM = "spam-or-scam"
CJ_REPORT_LOST_PHONE_OR_SIM = "lost-phone-or-sim"
CJ_REPORT_GCASH_CONCERN = "gcash-concerns"
CJ_BILLPYMNT_PAYMENT_ISSUE = "bills-and-payments-payment-issue"
CJ_BILLPYMNT_BILL_DISPUTE = "bills-and-payments-bill-dispute"
CJ_BILLPYMNT_COPY_OF_BILL = "bills-and-payments-copy-of-bill"
CJ_BILLPYMNT_OTHER_ISSUE = "bills-and-payments-other-issue"
CJ_BILLPYMNT_FOLLOW_UP = "bills-and-payments-follow-up"
CJ_BILLPYMNT_INSTALLMENT = "bills-and-payments-installment"
CJ_BILLPYMNT_FINANCIAL_CARE = "bills-and-payments-financial-care"
CJ_LOADPRMRWRD_LOAD_DEDUCTED ="load-promo-rewards-load-deducted"
CJ_LOADPRMRWRD_UNRECEIVED_LOAD = "load-promo-rewards-didnt-received-load"
CJ_LOADPRMRWRD_LOAN_LOAD = "load-promo-rewards-loan-load"
CJ_LOADPRMRWRD_CANT_SAL = "load-promo-rewards-cannot-share-load"
CJ_LOADPRMRWRD_UNRECEIVED_SAL = "load-promo-rewards-didnt-received-share-load"
CJ_LOADPRMRWRD_WRONG_NUMBER_SAL = "load-promo-rewards-sent-to-wrong-number-share-load"
CJ_LOADPRMRWRD_UNRECEIVED_PROMO = "load-promo-rewards-didnt-received-promo"
CJ_LOADPRMRWRD_DATA_CONSUMED_FAST = "load-promo-rewards-data-consumed-faster"
CJ_LOADPRMRWRD_UNRECEIVED_SAP = "load-promo-rewards-didnt-received-sap"
CJ_LOADPRMRWRD_CANT_REDEEM_REWARDS = "load-promo-rewards-cant-redeem-rewards"
CJ_LOADPRMRWRD_UNRECEIVED_POINTS = "load-promo-rewards-didnt-received-points"
CJ_LOADPRMRWRD_PUK = "load-promo-rewards-puk"
CJ_YODA_BUSINESS_MANAGEMENT = "yoda-business-management"
CJ_YODA_REGISTRATION_PROCESS = "yoda-registration-process"
CJ_BB_UPGRADE_PLAN = "mod-or-terminate-bb-upgrade-plan"
CJ_SIM_REGISTRATION = "sim-registration"
CJ_SIM_FAQ = "sim-faq"
CJ_ISSUE_WITH_SIM = "issue-with-sim"
CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN = "acctchnge-cancelplan"
CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_FINANCIAL_CONCERNS = "acctchnge-cancelplan-finconcerns"
CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_SWITCH_PROVIDER = "acctchnge-cancelplan-switchprovider"
CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_CONN_ISSUES = "acctchnge-cancelplan-connissues"
CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_XFER_LOC = "acctchnge-cancelplan-xferloc"
CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_OTHERS = "acctchnge-cancelplan-others"
CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_EXPLORE_PLANS = "acctchnge-cancelplan-exploreplans"
CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_CONN_ISSUES_TBS_CONNECTION = "acctchnge-cancelplan-connissues-tbsconn"
CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_XFER_LOC_XFER_INSTALL_LOC = "acctchnge-cancelplan-xferloc-xferinstallationloc"
CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_CONT_CANCEL_PLAN = "acctchnge-cancelplan-continuecancelplan"
CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_EXPLORE_PLANS_DOWNGRADEPLAN_OFFER1 = "acctchnge-cancelplan-exploreplans-downgrade-offer1"
CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_EXPLORE_PLANS_DOWNGRADEPLAN_OFFER2 = "acctchnge-cancelplan-exploreplans-downgrade-offer2"
CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_EXPLORE_PLANS_DOWNGRADEPLAN_OFFER3 = "acctchnge-cancelplan-exploreplans-downgrade-offer3"
CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_EXPLORE_PLANS_GET_PLAN = "acctchnge-cancelplan-exploreplans-getotherplans"

customer_journey_page_codes= {
    GT_PAGE_ID: "GT",
    THEA_PAGE_ID: "TH",
    TM_PAGE_ID: "TM",
    MYBUSINESS_PAGE_ID: "MB",
    GAH_PAGE_ID: "GH"
}


customer_journey_brand_codes = {
    CJ_NO_BRAND: "00",
    POSTPAID_LOB_NAME: "01",
    BB_LOB_NAME: "02",
    BUSINESS_LOB_NAME: "03",
    BUSINESS_EG_LOB_NAME: "04",
    BUSINESS_SG_LOB_NAME: "05",
    PLATINUM_MOBIE_LOB_NAME: "06",
    PLATINUM_BB_LOB_NAME: "07",
    IN_HOUSE_LOB_NAME: "08",
    PREPAID_LOB_NAME: "09",
    TRAVELER_LOB_NAME: "10",
    SHP_LOB_NAME: "11",
    PREPAID_HOME_WIFI_LOB_NAME: "12",
    TM_LOB_NAME: "13",
    UKNOWN_LOB_NAME: "14"
}

customer_journey_flow_codes = {
    CJ_NO_FLOW: "0000",
    CJ_NETWORK_CONCERN: "0001",
    CJ_LOAD_PROMO_REWARDS: "0002",
    CJ_BILL_AND_PAYMENTS: "0003",
    CJ_RECONNECT_MY_LINE: "0004",
    CJ_MODIFY_OR_TERMINATE: "0005",
    CJ_ACCOUNT_REQUESTS: "0006",
    CJ_CHECK_APPLICATION: "0007",
    CJ_FOLLOWUP_A_CONCERN: "0008",
    CJ_TECHNICIAN_VISIT: "0009",
    CJ_RENEW_MY_PLAN: "0010",
    CJ_APPLY_FOR_A_NEW_LINE:  "0011",
    CJ_BUY_LOAD_OR_PROMOS: "0012",
    CJ_ACTIVATE_SIM: "0013",
    CJ_ACTIVATE_FREEBIES: "0014",
    CJ_HOW_TO: "0015",
    CJ_REPORT_SPAM_OR_SCAM: "0016",
    CJ_REPORT_LOST_PHONE_OR_SIM: "0017",
    CJ_REPORT_GCASH_CONCERN: "0018",
    CJ_CHECK_BALANCE: "0006",
    CJ_BILLPYMNT_PAYMENT_ISSUE: "0020",
    CJ_BILLPYMNT_BILL_DISPUTE: "0021",
    CJ_BILLPYMNT_COPY_OF_BILL: "0022",
    CJ_BILLPYMNT_OTHER_ISSUE: "0023",
    CJ_BILLPYMNT_FOLLOW_UP: "0024",
    CJ_LOADPRMRWRD_LOAD_DEDUCTED: "0025",
    CJ_LOADPRMRWRD_UNRECEIVED_LOAD: "0026",
    CJ_LOADPRMRWRD_LOAN_LOAD: "0027",
    CJ_LOADPRMRWRD_CANT_SAL: "0028",
    CJ_LOADPRMRWRD_UNRECEIVED_SAL: "0029",
    CJ_LOADPRMRWRD_WRONG_NUMBER_SAL: "0030",
    CJ_LOADPRMRWRD_UNRECEIVED_PROMO: "0031",
    CJ_LOADPRMRWRD_DATA_CONSUMED_FAST: "0032",
    CJ_LOADPRMRWRD_UNRECEIVED_SAP: "0033",
    CJ_LOADPRMRWRD_CANT_REDEEM_REWARDS: "0034",
    CJ_LOADPRMRWRD_UNRECEIVED_POINTS: "0035",
    CJ_LOADPRMRWRD_PUK: "0036",
    CJ_YODA_BUSINESS_MANAGEMENT: "0037",
    CJ_YODA_REGISTRATION_PROCESS: "0038",
    CJ_BB_UPGRADE_PLAN: "0039",
    CJ_ENTER_CONCERNED_NUMBER: "0040",
    CJ_ANSWERED_SURVEY: "0041",
    CJ_MODIFY_OR_TERMINATE_POSTPAID_ESIM: "0042",
    CJ_MODIFY_OR_TERMINATE_PREPAID_ESIM: "0043",
    CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN: "0044",
    CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_FINANCIAL_CONCERNS: "0045",
    CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_SWITCH_PROVIDER: "0046",
    CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_CONN_ISSUES: "0047",
    CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_XFER_LOC: "0048",
    CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_OTHERS: "0049",
    CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_EXPLORE_PLANS: "0050",
    CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_CONN_ISSUES_TBS_CONNECTION: "0051",
    CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_XFER_LOC_XFER_INSTALL_LOC: "0052",
    CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_CONT_CANCEL_PLAN: "0053",
    CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_EXPLORE_PLANS_DOWNGRADEPLAN_OFFER1: "0054",
    CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_EXPLORE_PLANS_DOWNGRADEPLAN_OFFER2: "0055",
    CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_EXPLORE_PLANS_DOWNGRADEPLAN_OFFER3: "0056",
    CJ_MODIFY_OR_TERMINATE_CANCEL_PLAN_EXPLORE_PLANS_GET_PLAN: "0057",
    CJ_SIM_REGISTRATION: "0058",
    CJ_SIM_FAQ: "0059",
    CJ_ISSUE_WITH_SIM: "0060"
}
