from __future__ import annotations

import logging

from helpers.ddbtools import DDBTools

import configuration as configs

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ddb_switches = None

def is_switched_off(**kwargs) -> bool:
    global ddb_switches

    name = kwargs.get("name", "").strip()

    if not ddb_switches:
        ddb_switches = DDBTools(configs.DDB_SWITCHES, configs.REGION_OREGON)

    try:   
        result = ddb_switches.get_item("name", name)
    except Exception as e:
        logger.error(f"Error retrieving switch: ${e}")
        return False
    

    logger.info(f"switch result for {name}: {result}")

    if result:
        value = result[0].get("value", "").strip()
        if value.upper() == "OFF":
            return True
        
    return False