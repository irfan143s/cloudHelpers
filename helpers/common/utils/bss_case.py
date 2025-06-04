from __future__ import annotations

import logging

from helpers.common.db.ddb_case_created import CaseCreatedDdb


import configuration as configs

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def has_account_no_has_case_request_in_db_within_hours_and_titles(**kwargs) -> bool:
    account_no = kwargs.get("account_no", "")
    hours = kwargs.get("hours", 7)
    case_titles = kwargs.get("case_titles", [])

    case_create_ddb = CaseCreatedDdb()

    case_list = case_create_ddb.get_data_within_hours_by_account_no(hours=hours, account_no=account_no)
    if not case_list:
        return False
    
    logger.info(f"case_list retrieved: {case_list}")
    fitlered_case_list =[item for item in case_list if item.get("Title", "") in case_titles]
    sorted_case_list = sorted(fitlered_case_list, key=lambda x: x["DateOfRequest"], reverse=True)

    return bool(sorted_case_list)


def has_subscriber_no_has_case_request_in_db_within_hours_and_titles(**kwargs) -> bool:
    subscriber_no = kwargs.get("subscriber_no", "")
    hours = kwargs.get("hours", 7)
    case_titles = kwargs.get("case_titles", [])

    case_create_ddb = CaseCreatedDdb()

    case_list = case_create_ddb.get_data_within_hours_by_subscriber_no(hours=hours, subscriber_no=subscriber_no)
    if not case_list:
        return False
    
    filtered_case_list = [item for item in case_list if item["title"] in case_titles]
    sorted_case_list = sorted(filtered_case_list, key=lambda x: x["DateOfRequest"], reverse=True)

    return bool(sorted_case_list)
