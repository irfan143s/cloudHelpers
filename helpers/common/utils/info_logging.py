from __future__ import annotations

import logging

from helpers.common.features.subscriber_cross_channel_matching import SubscriberCrossChannelMatching

from resources.common.enums.cx_channels import CxChannels

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def subscriber_cross_channel_matching(cx_channel: CxChannels, args=None) -> None:
    if args == None or not args:
        return

    args = {
        "account_no": args.get("accountNo", ""),
        "msisdn": args.get("msisdn", ""),
        "channel_id": args.get("channelId", ""),
        "user_id": args.get("userId", ""),
        "identity_key": args.get("identityKey", ""),
    }

    try:
        SubscriberCrossChannelMatching(cx_channel).update_matching(**args)
    except Exception as error:
        logger.error(f"Error updating matching: {error}")
