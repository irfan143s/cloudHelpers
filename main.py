import json
import logging
from flask import jsonify, Request
import functions_framework  # GCP Cloud Functions helper

# ────────────────────────────────────────────────────────────────────────
# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

@functions_framework.http
def dialogflow_fb_webhook(request: Request):
    """
    A Dialogflow CX webhook that:
      1. Logs the incoming request from Dialogflow CX.
      2. Extracts the Facebook payload from event["payload"]["data"].
      3. Echoes that FB payload back as the fulfillment response so Messenger shows it.
    """

    # 1) Log the raw HTTP body for inspection
    raw_body = request.get_data(as_text=True)
    logger.info(f"[dialogflow_fb_webhook] Raw request: {raw_body}")

    # 2) Parse JSON
    try:
        event = request.get_json(silent=True) or {}
        logger.info(f"[dialogflow_fb_webhook] Parsed JSON: {json.dumps(event)}")
    except Exception as e:
        logger.error(f"[dialogflow_fb_webhook] Failed to parse JSON: {e}")
        return jsonify({"fulfillment_response": {"messages": []}})

    # 3) Extract the Facebook Messenger data under event["payload"]["data"]
    fb_data = event.get("payload", {}).get("data", {})
    if not fb_data:
        logger.error("[dialogflow_fb_webhook] No FB data found under payload.data")
        return jsonify({"fulfillment_response": {"messages": []}})

    # 4) Log the extracted FB data
    logger.info(f"[dialogflow_fb_webhook] Extracted FB data: {json.dumps(fb_data)}")

    # 5) Build a text string of the FB data to send back
    #    Here we stringify the entire fb_data object.
    echo_text = json.dumps(fb_data)

    # 6) Construct the Dialogflow CX fulfillment response
    response_payload = {
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": [echo_text]
                    }
                }
            ]
        }
    }

    logger.info(f"[dialogflow_fb_webhook] Response payload: {json.dumps(response_payload)}")
    return jsonify(response_payload)