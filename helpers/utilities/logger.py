# NIAS 2.0
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def log_execution_time(start: float, end: float, msg: str = "") -> None:
    total = (end - start) * 1000
    logger.info(f"<<[EXECUTION TRACKER]>> {msg} took: {total}ms")
