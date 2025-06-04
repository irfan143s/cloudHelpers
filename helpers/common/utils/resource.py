# NIAS 2.0
from __future__ import annotations

import logging

from resources.common.constants.case_details import case_details

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_case_details(**kwargs) -> dict:

    type = kwargs.get("type", "")
    brand = kwargs.get("brand", "default")

    case_details_result = case_details.get(type, {}).get(brand, {})
    return case_details_result