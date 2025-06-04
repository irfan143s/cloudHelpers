import json
import logging

from libraries import requests

from configuration import SOCIO_TOKEN, keyDictionary, SECONDARY_APP_ID, CONNECT_CHAT_APP_ID
from resources.api import HANDOVER_PASS_URL, GET_THREAD_OWNER

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class AgentTools:
    def __init__(self, channel,socio_token=None):
        if socio_token is None:
            socio_token = SOCIO_TOKEN
        self.__socioparams = {"access_token": socio_token}
        token = keyDictionary.get(channel)
        self.__params = {"access_token": token}
        self.__headers = {"Content-Type": "application/json"}

    ##transfer to agent
    def transferToAgent(self, send_id, target_id, metadata):
        data = json.dumps({
            "recipient": {"id": send_id},
            "target_app_id": target_id,
            "metadata": metadata
        })

        req = requests.post(HANDOVER_PASS_URL, params=self.__params, headers=self.__headers, data=data)
        logger.info(f"pass_thread_control response: {req.json()}")

        if req.status_code != 200:
            logger.info("Failed to transfer the thread to agent")
            # logger.info(req.status_code)
            # logger.info(req.text)
            return False
        else:
            logger.info(f"Message Thread was transferred to agent. Fb Id: {send_id}, Target app ID: {target_id}, Metadata: {metadata}")
            return True


    def updateStatus(self, socio_url, page_id, user_id, profile_id, intent_id="None", status="CLOSE"):
        if self.get_thread_owner(page_id, user_id) == SECONDARY_APP_ID and status == "CLOSE":
            logger.info("Thread with SOCIO and attempting to CLOSE SOCIO ticket")
            return

        data = json.dumps({
            "intentId": intent_id,
            "status": status,
            "channelId": page_id,
            "userId": user_id,
            "profileId": profile_id,
            "channel": "51"
        })

        req = requests.post(socio_url, params=self.__socioparams, headers=self.__headers, data=data)
        response = req.json()

        if req.status_code != 200:
            logger.info("SOCIO API CALL UPDATE API | FAIL | " + str(response['code'])  + " | " + str(response['message'])  + " | " +  json.dumps(self.__socioparams) + " | " + json.dumps(self.__headers) + " | " + json.dumps(data))
            return False
        else:
            logger.info("SOCIO API CALL UPDATE API | SUCCESS | " + str(response['code'])  + " | " + json.dumps(self.__socioparams) + " | " + json.dumps(self.__headers) + " | " + json.dumps(data))
            return True

            
    def get_thread_owner(self, channel, send_id):
        token = keyDictionary.get(channel)
        params = {
                    "access_token": token,
                    "recipient": send_id
                }
        headers = {"Content-Type": "application/json"}
        req = requests.get(GET_THREAD_OWNER, params=params, headers=headers)
        
        if req.status_code != 200:
            logger.info(req.status_code)
            logger.info(req.text)
            return None

        req = req.json()
        logger.info(f"get_thread_owner result for {send_id}: {req}") 

        if req["data"]:     
            return req['data'][0]['thread_owner']['app_id']
        else:
            return ""


    #transfer to connect chat agent
    def transfer_to_connect_chat(self, send_id, target_id, metadata):
        data = json.dumps({
            "recipient": {"id": send_id},
            "target_app_id": target_id,
            "metadata": metadata
        })

        req = requests.post(HANDOVER_PASS_URL, params=self.__params, headers=self.__headers, data=data)
        logger.info(f"pass_thread_control response: {req.json()}")

        if req.status_code != 200:
            logger.info("Failed to transfer the thread to Connect Chat")
            # logger.info(req.status_code)
            # logger.info(req.text)
            return False
        else:
            logger.info(f"Message Thread was transferred to Connect Chat. Fb Id: {send_id}, Target app ID: {target_id}, Metadata: {metadata}")
            return True