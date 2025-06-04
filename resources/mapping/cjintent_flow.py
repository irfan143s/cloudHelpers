#NIAS 2.0
from resources.cj import * 
from resources.aws_lambda import *
from resources.states import *


cj_intent_flow_mapping_dict = {
    CJ_NETWORK_CONCERN : {'sessionState':NETWORK_CONCERN_STATE,'subState':'DPN','lambda':NETWORK_CONCERN_LAMBDA},
    CJ_LOAD_PROMO_REWARDS : {'sessionState':LOAD_PROMOS_AND_REWARDS_STATE,'subState':'0','lambda':LOAD_PROMOS_AND_REWARDS_LAMBDA},
    CJ_BILL_AND_PAYMENTS : {'sessionState':BILLS_AND_PAYMENTS_STATE,'subState':'0','lambda':BILLS_AND_PAYMENTS_LAMBDA},
    CJ_RECONNECT_MY_LINE : {'sessionState':RECONNECT_MY_LINE_STATE,'subState':'DPN','lambda':RECONNECT_MY_LINE_LAMBDA},
    CJ_MODIFY_OR_TERMINATE : {'sessionState':MODIFY_OR_TERMINATE_STATE,'subState':'0','lambda':MODIFY_OR_TERMINATE_LAMBDA},
    CJ_CHECK_BALANCE : {'sessionState':CHECK_BALANCE_STATE,'subState':'INIT','lambda':CHECK_BALANCE_LAMBDA},
    CJ_CHECK_APPLICATION :{'sessionState':CHECK_APPLICATION_STATE,'subState':'0','lambda':CHECK_APPLICATION_LAMBDA},
    CJ_FOLLOWUP_A_CONCERN : {'sessionState':FOLLOWUP_CONCERN_STATE,'subState':'0','lambda':FOLLOWUP_CONCERN_LAMBDA},
    CJ_TECHNICIAN_VISIT : {'sessionState':TECHNICIAN_VISIT_STATE,'subState':'0','lambda':TECHNICIAN_VISIT_LAMBDA},
    CJ_RENEW_MY_PLAN : {'sessionState':RENEW_PLAN_STATE,'subState':'DPN','lambda':RENEW_PLAN_LAMBDA},
    CJ_APPLY_FOR_A_NEW_LINE : {'sessionState':APPLY_NEW_LINE_STATE,'subState':'0','lambda':APPLY_NEW_LINE_LAMBDA},
    CJ_BUY_LOAD_OR_PROMOS : {'sessionState':BUY_LOAD_OR_PROMO_STATE,'subState':'0','lambda':BUY_LOAD_OR_PROMO_LAMBDA},
    CJ_ACTIVATE_SIM : {'sessionState':ACTIVATE_SIM_STATE,'subState':'0','lambda':ACTIVATE_SIM_LAMBDA},
    CJ_ACTIVATE_FREEBIES : {'sessionState':ACTIVATE_FREEBIES_STATE,'subState':'0','lambda':ACTIVATE_FREEBIES_LAMBDA},
    CJ_HOW_TO : {'sessionState':HOW_TOS_STATE,'subState':'DPN','lambda':HOW_TOS_LAMBDA},
    CJ_REPORT_SPAM_OR_SCAM : {'sessionState':SPAM_OR_SCAM_STATE,'subState':'DPN','lambda':SPAM_OR_SCAM_LAMBDA},
    CJ_REPORT_LOST_PHONE_OR_SIM : {'sessionState':LOSTPHONE_OR_SIM_STATE,'subState':'DPN','lambda':LOSTPHONE_OR_SIM_LAMBDA},
    CJ_REPORT_GCASH_CONCERN : {'sessionState':GCASH_CONCERNS_STATE,'subState':'INIT','lambda':GCASH_CONCERNS_LAMBDA}
} 

