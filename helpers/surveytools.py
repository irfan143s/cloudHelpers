import logging

from datetime import datetime

from configuration import REGION_OREGON, DDB_CUSTOMER_JOURNEY, pageDictionary, MYBUSINESS_PAGE_NAME, GT_PAGE_NAME, GAH_PAGE_NAME, TM_PAGE_NAME

from helpers.utils import get_current_time, get_exception_str, close_socio_ticket
from helpers.resFormatter import ResFormatter
from helpers.ddbtools import DDBTools

from resources.spiels import CES_DEFAULT_TITLE, CES_DEFAULT_SURVEY_TITLE, CES_DEFAULT_SUB_TITLE, CES_THANK_YOU_RESPONSE
from resources.resourcemapping import page_name_mapping_dict
from resources.constants import SESSION_STATUS_TICKET_CLOSURE

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def ces_survey_response_handler(res, feedback, db_main, sender_id, session):
    db_cj = DDBTools(DDB_CUSTOMER_JOURNEY, REGION_OREGON)
    feedback_score = feedback[0]['questions']['ceslex']['payload']
    feedback_comment = feedback[0]['questions']['ceslex']['follow_up']['payload']
    feedback_timestamp = get_current_time()
    last_session_id = session.get_last_session_id()

    # save to db
    try:
        db_main.updateItem(sender_id, 'lastSurveyDate', feedback_timestamp)
        db_cj.update_item('sessionId', last_session_id, {
            "feedbackScore": feedback_score,
            "feedback": feedback_comment,
            "feedbackTimestamp": feedback_timestamp
        })
        res.send_message(sender_id, CES_THANK_YOU_RESPONSE)
        session.update_status(SESSION_STATUS_TICKET_CLOSURE)
    except Exception as error:
        logger.error(f"Error in saving feedback data: {get_exception_str(error)}")

def ces_survey_sender_handler(last_survey_date, sender_id, page_id):
    if pageDictionary[page_id] in [MYBUSINESS_PAGE_NAME, GT_PAGE_NAME, GAH_PAGE_NAME, TM_PAGE_NAME]:
        if last_survey_date not in [" ", "String", None]:
            fmt = '%Y-%m-%dT%H:%M:%S'
            last_surveyed_date = datetime.strptime(last_survey_date[0:19], fmt)
            current_time = get_current_time()
            #date_diff = current_time - last_surveyed_date
            date_diff = datetime.strptime(current_time, fmt) - last_surveyed_date

            # check if last surveyed date is greater than 30 days
            if date_diff.days > 30:
                send_survey(sender_id, page_id)
        else:
            send_survey(sender_id, page_id)
    return

def send_survey(sender_id, page_id):
    logger.info("Sending CES Survey")
    res = ResFormatter(page_id)
    page_name = page_name_mapping_dict[page_id]
    title = CES_DEFAULT_TITLE
    survey_title = CES_DEFAULT_SURVEY_TITLE
    res.send_ces_survey(sender_id, title, CES_DEFAULT_SUB_TITLE, survey_title)

    return

