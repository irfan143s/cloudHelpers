from __future__ import annotations

import time
import json
import logging
from libraries import requests

from resources.common.enums.cx_channels import CxChannels
from resources.common.enums.cx_agent_platforms import CxAgentPlatforms

import resources.api as apis
import configuration as configs

logger = logging.getLogger()
logger.setLevel(logging.INFO)

MAX_LIVE_PERSON_ATTEMPT = 3


class AgentHelper:

    def __init__(self, cx_agent_platform: CxAgentPlatforms, cx_channel: CxChannels):
        self.__cx_channel = cx_channel
        self.__cx_agent_platform = cx_agent_platform

    def handover_to_an_agent_app(self, **kwargs) -> bool:
        logger.info(f"handover_to_an_agent_app() -> kwargs={kwargs}")

        REQUIRED_PARAMS = ["psid", "page_id"]
        for param in REQUIRED_PARAMS:
            if not kwargs.get(param):
                self._log_error("fb", {}, type="pass_thread_control:failed:validation", info=f"{param} is required!", params={**kwargs})
                return False
            
        psid = kwargs.get("psid", "")
        page_id = kwargs.get("page_id", "")
        meta_data = kwargs.get("meta_data", {})

        if meta_data and not isinstance(meta_data, dict):
            logger.info(f"meta_data:dict is required")
            return False

        if self.__cx_agent_platform == CxAgentPlatforms.CONNECT:
            app_id = configs.CONNECT_CHAT_APP_ID
        elif self.__cx_agent_platform == CxAgentPlatforms.LIVE_PERSON:
            app_id = configs.LIVE_PERSON_APP_ID
        else:
            app_id = configs.SECONDARY_APP_ID

        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "access_token": configs.keyDictionary.get(page_id)
        }
        data = {
            "recipient": {
                "id": psid
            },
            "target_app_id": app_id,
            "metadata": meta_data
        }

        log_object = {
            "psid": psid,
            "page_id": page_id,
            "headers": headers,
            "params": params,
            "payload": data
        }
        self._log_info("fb", log_object, type="pass_thread_control:init")

        try:
            response = requests.post(apis.HANDOVER_PASS_URL, params=params, headers=headers, data=json.dumps(data))

            try:
                response_data = response.json()
            except Exception as error:
                response_data = response.text

            if response.status_code != 200:
                self._log_error("fb", log_object, type="pass_thread_control:failed", info="Failed due to API response!", status_code=response.status_code, response=response_data)
                return False
            
            self._log_info("fb", log_object, type="pass_thread_control:succeeded", status_code=response.status_code, response=response_data)
            return True
        except Exception as e:
            self._log_error("fb", log_object, type="pass_thread_control:failed", info=f"Failed due to error: {e}")
            return False
    

    def fb_update_socio_status(self, **kwargs) -> bool:
        logger.info(f"fb_update_socio_status() -> kwargs={kwargs}")

        REQUIRED_PARAMS = ["psid", "page_id", "intent_id", "status", "profile_id", "socio_update_api"]
        for param in REQUIRED_PARAMS:
            if not kwargs.get(param):
                self._log_info("socio", {}, type="socio:failed:validation", info=f"{param} is required!", params={**kwargs})
                return False
            
        psid = kwargs.get("psid", "")
        page_id = kwargs.get("page_id", "")
        intent_id = kwargs.get("intent_id", "")
        status = kwargs.get("status", "")
        profile_id = kwargs.get("profile_id", "")
        socio_update_api_url = kwargs.get("socio_update_api", "")
        socio_channel = kwargs.get("socio_channel", "51")
        socio_token = configs.SOCIO_TOKEN

        socio_params = {
            "access_token": socio_token
        }
        socio_headers = {
            "Content-Type": "application/json"
        }

        data = {
            "intentId": intent_id,
            "status": status,
            "channelId": page_id,
            "userId": psid,
            "profileId": profile_id,
            "channel": socio_channel
        }

        log_object = {
            "type": "socio:init",
            "psid": psid,
            "page_id": page_id,
            "headers": socio_headers,
            "param": socio_params,
            "payload": data
        }
        self._log_info("socio", log_object)

        try:
            response = requests.post(socio_update_api_url, params=socio_params, headers=socio_headers, data=json.dumps(data))
            try:
                response_data = response.json()
            except Exception as error:
                response_data = response.text
                
            if response.status_code not in [200, 202]:            
                self._log_error("socio", log_object, type="socio:failed", info="Failed due to API response!", status_code=response.status_code, response=response_data)
                return False
            
            self._log_info("socio", log_object, type="socio:succeeded", status_code=response.status_code, response=response_data)
            return True
        except Exception as e:
            self._log_error("socio", log_object, type="socio:failed", info=f"Failed due to error: {e}")
            return False


    def invoke_live_person(self, **kwargs) -> bool:
        logger.info(f"invoke_live_person() -> kwargs={kwargs}")

        REQUIRED_PARAMS = ["psid"]
        for param in REQUIRED_PARAMS:
            if not kwargs.get(param):
                self._log_info("lp", {}, type="liveperson:failed:validation", info=f"{param} is required!", params={**kwargs})
                return False
            
        psid = kwargs.get("psid", "")
        support_intent = kwargs.get("support_intent", "")
        live_person_token = self.get_live_person_token()        
        params = {}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f'Bearer {live_person_token}'
        }
        data = {
            "timestamp": 0,
            "headers": [],
            "payload": {
                "psid": psid,
                "intent": support_intent
            }
        }

        for attempt in range(MAX_LIVE_PERSON_ATTEMPT):
            log_object = {
                "type": "liveperson:init",
                "psid": psid,
                "headers": headers,
                "payload": data
            }
            self._log_info("lp", log_object)

            try:
                response = requests.post(apis.LIVE_PERSON_URL, params=params, headers=headers, data=json.dumps(data))
                try:
                    response_data = response.json()
                except Exception as error:
                    response_data = response.text

                if response.status_code not in [200, 202]:
                    if attempt < (MAX_LIVE_PERSON_ATTEMPT - 1):
                        time.sleep(2 ** attempt)
                        self._log_info("lp", log_object, type="liveperson:failed:retry", info="Failed due to API response!", code=response.status_code, response=response_data, attempt=attempt)
                        continue
                    else:
                        self._log_error("lp", log_object, type="liveperson:failed", info="Maxed attempt. Failed due to API response!", status_code=response.status_code, response=response_data)
                        return False
                
                self._log_info("lp", log_object, type="liveperson:succeeded", status_code=response.status_code, response=response_data)
                return True
            except Exception as e:
                if attempt < (MAX_LIVE_PERSON_ATTEMPT - 1):
                    time.sleep(2 ** attempt)
                    self._log_info("lp", log_object, type="liveperson:failed:retry", info=f"Failed due to error: {e}", attempt=attempt)
                    continue
                else:
                    self._log_error("lp", log_object, type="liveperson:failed", info=f"Maxed attempt. Failed due to error: {e}")
                    return False
        return False           


    def get_live_person_token(self) -> str:
        params = {}
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = f'client_id={configs.LIVE_PERSON_CLIENT_ID}&client_secret={configs.LIVE_PERSON_CLIENT_SECRET}&grant_type=client_credentials'

        for attempt in range(MAX_LIVE_PERSON_ATTEMPT):
            log_object = {
                "type": "liveperson-token:init",
                "headers": headers,
                "payload": payload
            }
            self._log_info("lp", log_object)

            try:
                response = requests.post(apis.LIVE_PERSON_TOKEN_URL, params=params, headers=headers, data=payload)
                try:
                    response_data = response.json()
                except Exception as error:
                    response_data = response.text

                if response.status_code not in [200, 202]:
                    if attempt < (MAX_LIVE_PERSON_ATTEMPT - 1):
                        time.sleep(2 ** attempt)
                        self._log_info("lp", log_object, type="liveperson-token:failed:retry", info="Failed due to API response!", status_code=response.status_code, response=response_data, attempt=attempt)
                        continue
                    else:
                        self._log_error("lp", log_object, type="liveperson-token:failed", info="Maxed attempt. Failed due to API response!", status_code=response.status_code, response=response_data)
                        return ""

                self._log_info("lp", log_object, type="liveperson-token:succeeded", status_code=response.status_code, response=response_data)
                return response_data.get('access_token')
            except Exception as e:
                if attempt < (MAX_LIVE_PERSON_ATTEMPT - 1):
                    time.sleep(2 ** attempt)
                    self._log_info("lp", log_object, type="liveperson-token:failed:retry", info=f"Failed due to error: {e}", attempt=attempt)
                    continue
                else:
                    self._log_error("lp", log_object, type="liveperson-token:failed", info=f"Maxed attempt. Failed due to error: {e}")
                    return ""
        return ""

        
    def _log_info(self, platform, log_object, **kwargs) -> None:
        self._log("i", platform, log_object, **kwargs)

    
    def _log_error(self, platform, log_object, **kwargs) -> None:
        self._log("e", platform, log_object, **kwargs)


    def _log(self, log_type, platform, log_object, **kwargs) -> None:
        log_object.update(**kwargs)

        if platform=="lp":
            log_str = f"[[ liveperson ]]: {log_object}"
        elif platform=="fb":
            log_str = f"[[ facebook ]]: {log_object}"
        elif platform=="socio":
            log_str = f"[[ socio ]]: {log_object}"
        else:
           log_str = f"[[ generic ]]: {log_object}"

        if log_type.lower() == "e":
            logger.error(log_str)
        else:
            logger.info(log_str)