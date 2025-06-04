from datetime import datetime, timedelta

from resources.spiel.reward_spiels import OFFER_DATE
from resources.spiels import (
    SESSION_END_SPIEL,
    SESSION_END_REWARDS_SPIEL
)


def get_configured_closing_spiel():
    curr_date = datetime.utcnow() + timedelta(hours=8)
    year = str(curr_date.year)
    month = str(curr_date.month).zfill(2)
    day = str(curr_date.day).zfill(2)

    spiel = SESSION_END_SPIEL
    if year in OFFER_DATE:
        if month in OFFER_DATE[year]:
            if OFFER_DATE[year][month][day] is not None and isinstance(OFFER_DATE[year][month][day], dict):
                spiel = f"""{SESSION_END_SPIEL}{SESSION_END_REWARDS_SPIEL.format(OFFER_DATE[year][month][day]['offer-2'], 
                        OFFER_DATE[year][month][day]['offer-3'], OFFER_DATE[year][month][day]['offer-1'])}"""
            elif OFFER_DATE[year][month][day] is not None:
                spiel = f"{SESSION_END_SPIEL}{SESSION_END_REWARDS_SPIEL}"
    return spiel
