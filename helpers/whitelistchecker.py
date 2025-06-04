
# NIAS 2.0
import logging

from configuration import *

from helpers.ddbtools import DDBTools

from resources.resourcemapping import *

import resources.constants as constants

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def is_employee_care_whitelisted(concern_no):
    ddb_empl_care_wl = DDBTools(DDB_EMPLOYEE_CARE_WHITELIST, REGION_OREGON)
    result = ddb_empl_care_wl.get_item('concernNo', concern_no.strip())
    if result:
        return True
        
    return False

def is_platinum_gcash_whitelisted(concern_no):
    ddb_platinum_gcash_wl = DDBTools(DDB_GCASH_PLATINUM_WHITELIST, REGION_OREGON)
    result = ddb_platinum_gcash_wl.get_item('concernNo', concern_no.strip())
    if result:
        return True
        
    return False

def is_pending_stuck_order_whitelisted(service_id):
    ddb_pending_stuck_order_wl = DDBTools(DDB_PENDING_STUCK_ORDER_WHITELIST, REGION_OREGON)
    result = ddb_pending_stuck_order_wl.get_item('serviceId', service_id.strip())
    if result:
        return True
        
    return False

def is_platinum_whitelisted(concern_no):
    ddb_platinum_wl = DDBTools(DDB_PLATINUM_WHITELIST, REGION_SYDNEY)
    result = ddb_platinum_wl.get_item('msisdn', concern_no.strip())
    if result:
        return True
        
    return False

def is_hamilton_whitelisted(concern_no):
    ddb_hamilton_wl = DDBTools(DDB_HAMILTON_WHITELIST, REGION_OREGON)
    result = ddb_hamilton_wl.get_item('concernNo', concern_no.strip())
    if result:
        return True
        
    return False

def is_birthday_code_whitelisted(concern_no, coupon_code):
    ddb_birthday_code_wl = DDBTools(BIRTHDAY_TREATS_WHITELIST_DB, REGION_OREGON)
    result = ddb_birthday_code_wl.get_item('MSISDN', concern_no.strip())
    if result and result[0]["Coupon Code"] == coupon_code:
        return True
        
    return False

def is_birthday_code_redeemed(concern_no):
    ddb_birthday_code_redeemed = DDBTools(BIRTHDAY_TREATS_REDEEMED_DB, REGION_OREGON)
    result = ddb_birthday_code_redeemed.get_item('MSISDN', concern_no.strip())
    if result:
        return True
        
    return False

def is_bb_upsell_whitelisted(account_num):
    ddb_bb_upsell_whitelisted = DDBTools(DDB_UPSELL_WHITELIST, REGION_SYDNEY)
    result = ddb_bb_upsell_whitelisted.get_item('cust_ac_no', account_num.strip())
    if result:
        return result[0]
        
    return result

def is_caif_whitelisted(account_num):
    ddb_caif_whitelisted = DDBTools(DDB_SERVICE_RECOVERY_WHITELIST, REGION_SYDNEY)
    result = ddb_caif_whitelisted.get_item('account_no', account_num.strip())

    if result:
        logger.info(f"account num {account_num}")
        logger.info(f"caif fetched data {result}")
        if "cohort" in result[0]:
            if str(result[0]['cohort']).upper() == "CAIF" and str(result[0]['caif_base']) == "1":
                return True
        
    return False

def is_bb_outage_whitelisted(cabinet_id):
    bb_outage_whitelisted = DDBTools(DDB_BB_OUTAGE_WHITELIST, REGION_SYDNEY)
    result = bb_outage_whitelisted.get_item('cabinetId', cabinet_id.strip())
    if result:
        return result
        
    return result

def is_recurring_notif_opted(fb_id, page_id):
    recurring_notif_table = DDBTools(DDB_RECURRING_NOTIF_TABLE, REGION_OREGON)
    result = recurring_notif_table.get_item('fbId', fb_id.strip())

    if result:
        logger.info(f"fbId {fb_id}")
        logger.info(f"recurring notif fetched data {result}")
        if result and result[0]["pageId"] == page_id:
            return result
        
    return False

def is_platinum_upsell_whitelisted(msisdn):
    ddb_platinum_upsell_wl = DDBTools(DDB_PLATINUM_UPSELL_WHITELIST, REGION_SYDNEY)
    result = ddb_platinum_upsell_wl.get_item('msisdn', msisdn.strip())
    if result:
        if result[0]["segment_name"] in [constants.THEA_PLATINUM_OLD_PHONE_TRAVEL, constants.THEA_PLATINUM_OLD_PHONE_SHOPPING, constants.THEA_PLATINUM_OLD_PHONE_RESTAURANT, constants.THEA_PLATINUM_NEW_PHONE_SHOPPING]:
            return result
        
    return False

def is_free_thea_whitelisted(msisdn):
    ddb_free_thea_wl = DDBTools(DDB_PLATINUM_FREE_THEA_WHITELIST, REGION_SYDNEY)
    result = ddb_free_thea_wl.get_item('msisdn', msisdn.strip())
    if result:
        logger.info(f"free_thea_whitelisted -> {msisdn}")
        return True
        
    return False

def is_upsell_offer_availed(msisdn):
    ddb_upsell_report = DDBTools(DDB_PLATINUM_UPSELL_REPORT, REGION_SYDNEY)
    result = ddb_upsell_report.get_item('msisdn', msisdn.strip())
    if result:
        if result[0]["plan_summary_offer1"] == 'Upgrade' or result[0]["plan_summary_offer2"] == 'Upgrade':
            logger.info(f"upsell_offer_availed -> {msisdn}")
            return True
        
    return False

def is_lpr_first_timer_whitelisted(msisdn):
    ddb_lpr_first_timer = DDBTools(DDB_LPR_FIRST_TIMER_WHITELIST, REGION_SYDNEY)
    result = ddb_lpr_first_timer.get_item('msisdn', msisdn.strip())
    if result:
        logger.info(f"is_lpr_first_timer_whitelisted -> {msisdn} -> True")
        return True

    logger.info(f"is_lpr_first_timer_whitelisted -> {msisdn} -> False")    
    return False

def is_proactive_renewal_whitelisted(msisdn):
    ddb_proactive_renewal_wl = DDBTools(DDB_PROACTIVE_RENEWAL_WHITELIST, REGION_SYDNEY)
    result = ddb_proactive_renewal_wl.get_item('msisdn', msisdn.strip())
    if result:
        if result[0]["whitelist_status"] == 'Success':
            logger.info(f"proactive_renewal_whitelisted -> {msisdn}")
            return True
        
    return False

def is_bb_facility_migration_whitelisted(account_num):
    ddb_bb_facility_migration_wl = DDBTools(DDB_BB_FACILITY_MIGRATION_WHITELIST, REGION_SYDNEY)
    result = ddb_bb_facility_migration_wl.get_item('account_num', account_num.strip())
    if result:
        return True
        
    return False


def is_unlock_device_whitelisted(device_imei):
    ddb_bb_facility_migration_wl = DDBTools(DDB_UNLOCK_DEVICE_WHITELIST, REGION_SYDNEY)
    result = ddb_bb_facility_migration_wl.get_item('device_imei', device_imei.strip())
    if result:
        return True, result
        
    return False, result

def is_go_fam_whitelisted(concern_no):
    ddb_go_fam_wl = DDBTools(DDB_GO_FAM_WHITELIST, REGION_OREGON)
    result = ddb_go_fam_wl.get_item('concernNo', concern_no.strip())
    if result:
        logger.info(f"is_go_fam_whitelisted -> {concern_no} -> True")
        return True
        
    return False

def is_raket_whitelisted(concern_no):
    ddb_raket_wl = DDBTools(DDB_RAKET_WHITELIST, REGION_OREGON)
    result = ddb_raket_wl.get_item('concernNo', concern_no.strip())
    if result:
        logger.info(f"is_raket_whitelisted -> {concern_no} -> True")
        return True
        
    return False

def is_coex_whitelisted_by_account_no(account_no):
    ddb_coex_wl = DDBTools(DDB_COEX_WHITELIST, REGION_OREGON)
    result = ddb_coex_wl.get_item_by_index('accountNo', account_no.strip(), "accountNo-index")
    if result:
        logger.info(f"is_coex_whitelisted -> {account_no} -> True")
        return True
        
    return False

def is_coex_whitelisted_by_msisdn(msisdn):
    ddb_coex_wl = DDBTools(DDB_COEX_WHITELIST, REGION_OREGON)
    result = ddb_coex_wl.get_item_by_index('msisdn', msisdn.strip(), "msisdn-index")
    if result:
        logger.info(f"is_coex_whitelisted -> {msisdn} -> True")
        return True
        
    return False