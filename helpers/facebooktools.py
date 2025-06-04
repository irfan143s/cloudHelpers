import os
import json
import random
import logging
import asyncio

from functools import partial
from helpers.utils import *
from helpers.ddbtools import DDBTools

from libraries import requests

from configuration import GT_PAGE_NAME, EE_PAGE_NAME, keyDictionary, DDB_MONITORING, REGION_OREGON
from resources.api import *
from resources.constants import *
from resources import monitoring
from resources.resourcemapping import page_persona_mapping_dict

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class FacebookTools:

    __ddb_monitoring = None
    __APP_RATE_LIMIT_RETRY_SECONDS = 1800 #30mins

    ##send txt via messenger to id
    def send_message(self, params, headers, page, send_id, msg_txt, messageTagToggle, is_private_reply, personaToggle):
        request = {"recipient":
                       {"id": send_id},
                   "message":
                       {'text': msg_txt}
                   }
        self.__handle_message_tag(messageTagToggle, request)
        self.__handle_private_reply(is_private_reply, request, send_id)
        self.__handle_persona(personaToggle, request, page)
        data = json.dumps(request)
        req = requests.post(GRAPH_API_URL, params=params, headers=headers, data=data)
        
        if req.status_code != 200:
            logger.info(f"Failed to send message. request: {request}")
            logger.info(f"status_code: {req.status_code}, txt: {req.text}")


    ##send response card via messenger to id
    def send_responseCard(self, params, headers, page, send_id, title, subtitle, image_url, personaToggle):
        request = {"recipient": {"id": send_id},
                           "message": {"attachment":
                               {"type":"template",
                                "payload":{
                                    "template_type":"generic",
                                    "elements":[
                                   {
                                    "title": title,
                                    "image_url": image_url,
                                    "subtitle": subtitle
                                  }
                                ]
                              }
                            }
                        }
                   }

        self.__handle_persona(personaToggle,request,page)
        data = json.dumps(request)
        req = requests.post(GRAPH_API_URL, params=params, headers=headers, data=data)
        
        if req.status_code != 200:
            print(req.status_code)
            print(req.text)
    
    def send_carousel(self, params, headers, page, send_id, cardHeaders, buttons, urlState, randomCards, personaToggle):
        cards=[]
        for header, buttonlist in zip(cardHeaders, buttons):
            buttonTemp=[]
            if urlState == False:
                for button in buttonlist:
                    temp={
                        "type": "postback",
                        "title": button[0],
                        "payload": "[menu]" + "." + button[1]
                    }
                    buttonTemp.append(temp)
            else:
                for button in buttonlist:
                    temp={
                        "type": "web_url",
                        "title": button[0],
                        "url": button[1],
                        "webview_height_ratio": "full"
                    }
                    buttonTemp.append(temp)
            temp={
                "title": header[0],
                "subtitle": header[1],
                "image_url": header[2],
                "buttons": buttonTemp
            }
            cards.append(temp)

        if randomCards == True:
            random.shuffle(cards)
        request = {
            "recipient":
                {"id": send_id},
            "message":
                {"attachment":
                    {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": cards,
                        }
                    }
                }
        }

        self.__handle_persona(personaToggle,request,page)
        data = json.dumps(request)
        req = requests.post(GRAPH_API_URL, params=params, headers=headers, data=data)
        
        if req.status_code != 200:
            print(req.status_code)
            print(req.text)
    
    # NIAS 2.0
    def send_option_buttons(self, params, headers, page, send_id, spiel, buttons, urlState, messageTagToggle, is_private_reply, personaToggle):
        tmp_buttons = []

        for button in buttons:
            if urlState:
                temp = {
                    "type": "web_url",
                    "title": button['title'],
                    "url": button['url'],
                    "webview_height_ratio": "full"
                }
            else:
                temp = {
                    "type": "postback",
                    "title": button['title'],
                    "payload": "[option]" + "." + button['optionId']
                }
            
            tmp_buttons.append(temp)

        request = {
            "recipient":{
                "id": send_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "button",
                        "text": spiel,
                        "buttons": tmp_buttons
                    }
                }
            }
        }
        self.__handle_message_tag(messageTagToggle, request)
        self.__handle_persona(personaToggle, request, page) 
        self.__handle_private_reply(is_private_reply, request, send_id)
        data = json.dumps(request)
        req = requests.post(GRAPH_API_URL, params=params, headers=headers, data=data)
        
        if req.status_code != 200:
            print(req.status_code)
            print(req.text)


    def send_carousel_multiple_type(self, params, headers, page, send_id, cardHeaders, buttons, randomCards, messageTagToggle, personaToggle):
        cards=[]
        for header, buttonlist in zip(cardHeaders, buttons):
            buttonTemp=[]
            for button in buttonlist:
                if button[2] == "NORMAL":          
                    temp={
                        "type": "postback",
                        "title": button[0],
                        "payload": "[menu]" + "." + button[1]
                    }
                elif button[2] == "URL":
                    temp={
                        "type": "web_url",
                        "title": button[0],
                        "url": button[1],
                        "webview_height_ratio": "full"
                    }
                buttonTemp.append(temp)

            temp={
                "title": header[0],
                "subtitle": header[1],
                "buttons": buttonTemp
            }
            if header[2].strip():
                temp["image_url"]: header[2]
            cards.append(temp)
        
        if randomCards == True:
            random.shuffle(cards)
        request = {
            "recipient":
                {"id": send_id},
            "message":
                {"attachment":
                    {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": cards,
                        }
                    }
                }
        }
        self.__handle_message_tag(messageTagToggle, request)
        self.__handle_persona(personaToggle, request, page)
        data = json.dumps(request)
        req = requests.post(GRAPH_API_URL, params=params, headers=headers, data=data)
        
        if req.status_code != 200:
            print(req.status_code)
            print(req.text)

    # send response card via messenger to id
    def send_quickresponse(self, params, headers, page, send_id, question, menu, formName, messageTagToggle, is_private_reply, personaToggle):
        _menurender = []
        for menu_item in menu:
            _menurender.append({"content_type": "text","title": menu_item,"payload": str(formName)},)
        request = {"recipient": {"id": send_id},
                           "messaging_type": "RESPONSE",
                           "message": {
                               "text": question,
                               "quick_replies": _menurender ,
                           }}
        self.__handle_message_tag(messageTagToggle, request)
        self.__handle_private_reply(is_private_reply, request, send_id)
        self.__handle_persona(personaToggle,request,page)
        data = json.dumps(request)
        req = requests.post(GRAPH_API_URL, params=params, headers=headers, data=data)
        
        if req.status_code != 200:
            print(req.status_code)
            print(req.text)

    # notification message optin
    def send_notif_message_optin(self, params, headers, page, send_id, title, img_url, frequency, personaToggle):
        payload = {
            "fbId": send_id,
            "pageId": page
        }
        payload = json.dumps(payload)
        request = {
            "recipient": {
                "id": send_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "notification_messages",
                        "image_url": img_url,
                        "title": title,
                        "payload": payload,
                        "notification_messages_frequency": frequency
                    }
                }
            }
        }
        self.__handle_persona(personaToggle,request,page)
        data = json.dumps(request)
        req = requests.post(GRAPH_API_URL, params=params, headers=headers, data=data)
        
        if req.status_code != 200:
            print(req.status_code)
            print(req.text)

    # send recurring notif message
    def send_recurring_notif_message(self, params, headers, page, token, msg_txt, personaToggle):
        request = {
                    "recipient": {"notification_messages_token": token},
                    "message": {'text': msg_txt}
                   }
        self.__handle_persona(personaToggle,request,page)
        data = json.dumps(request)
        req = requests.post(GRAPH_API_URL, params=params, headers=headers, data=data)
        
        if req.status_code != 200:
            logger.info(f"Failed to send message. request: {request}")
            logger.info(f"status_code: {req.status_code}, txt: {req.text}")
        
        return req.status_code

    # send account update carousel
    def send_account_update_carousel(self, params, headers, page, send_id, cardHeaders, buttons, randomCards, personaToggle):
        cards=[]
        for header, buttonlist in zip(cardHeaders, buttons):
            buttonTemp=[]
            for button in buttonlist:
                if button[2] == "NORMAL":          
                    temp={
                        "type": "postback",
                        "title": button[0],
                        "payload": "[menu]" + "." + button[1]
                    }
                elif button[2] == "URL":
                    temp={
                        "type": "web_url",
                        "title": button[0],
                        "url": button[1],
                        "webview_height_ratio": "full"
                    }
                buttonTemp.append(temp)

            temp={
                "title": header[0],
                "subtitle": header[1],
                "image_url": header[2],
                "buttons": buttonTemp
            }
            cards.append(temp)
        
        if randomCards == True:
            random.shuffle(cards)
        request = {

            "recipient":
                {"id": send_id},
            "messaging_type": "MESSAGE_TAG",
            "tag": "ACCOUNT_UPDATE",
            "message":
                {"attachment":
                    {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": cards,
                        }
                    }
                }
        }
        self.__handle_persona(personaToggle,request,page)
        data = json.dumps(request)
        req = requests.post(GRAPH_API_URL, params=params, headers=headers, data=data)
        
        if req.status_code != 200:
            print(req.status_code)
            print(req.text)

    # send ces survey
    def send_ces_survey(self, params, headers, page, send_id, title, sub_title, survey_title, personaToggle):
        request = {
            "recipient": {
                "id": send_id
            },
            "message": {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "customer_feedback",
                        "title": title,
                        "subtitle": sub_title,
                        "button_title": "Give Feedback", 
                        "feedback_screens": [
                            {
                                "questions": [
                                    {
                                        "id": "ceslex",
                                        "type": "ces",
                                        "title": survey_title,
                                        "score_label": "hard_easy",
                                        "score_option": "one_to_seven",
                                        "follow_up": {
                                            "type": "free_form",
                                            "placeholder": "Give additional feedback"
                                        }
                                    }
                                ]
                            }
                        ],
                        "business_privacy": {
                            "url": "https://www.globe.com.ph/privacy-policy.html"
                        },
                        "expires_in_days": 1
                    }
                }
            }
        }
        self.__handle_persona(personaToggle, request, page)
        data = json.dumps(request)
        req = requests.post(GRAPH_API_URL, params=params, headers=headers, data=data)
        
        if req.status_code != 200:
            logger.info(f"Failed to send message. request: {request}")
            logger.info(f"status_code: {req.status_code}, txt: {req.text}")

    # upload files
    def upload_media_type(self, params, headers, page, fileType, fileUrl, isReusable, personaToggle):
        request = {"message": {
                    "attachment": {
                        "type": fileType,
                        "payload": {
                            "url": fileUrl,
                            "is_reusable": isReusable
                        }
                    }
                }
            }

        self.__handle_persona(personaToggle,request,page)
        data = json.dumps(request)
        req = requests.post(GRAPH_API_URL, params=params, headers=headers, data=data)
        
        if req.status_code != 200:
            print(req.status_code)
            print(req.text)

    # send files
    def send_media_type(self, params, headers, page, send_id, fileType, attachmentId, personaToggle):
        request = {"recipient":{
                    "id": send_id
                    },
                    "message": {
                        "attachment": {
                           "type": "template",
                           "payload": {
                                "template_type": "media",
                                "elements": [
                                    {
                                       "media_type": fileType,
                                       "attachment_id": attachmentId 
                                    }
                                ]
                                
                           }
                        }
                    }
                }

        self.__handle_persona(personaToggle,request,page)
        data = json.dumps(request)
        req = requests.post(GRAPH_API_URL, params=params, headers=headers, data=data)
        
        if req.status_code != 200:
            print(req.status_code)
            print(req.text)

    # get current owner of thread
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


    # NIAS 2.0 - get current owner of thread async
    async def get_thread_owner_async(self, channel, psid):
        token = keyDictionary.get(channel)
        params = {
                    "access_token": token,
                    "recipient": psid
                }
        headers = {"Content-Type": "application/json"}
        res = await asyncio.get_running_loop().run_in_executor(None, partial(requests.get, GET_THREAD_OWNER, params=params, headers=headers))
        
        if res.status_code != 200:
            logger.info(f"Failed to get thread owner. status_code: {res.status_code}, txt: {res.text}")
            return None

        res = res.json()
        logger.info(f"get_thread_owner_async result for {psid}: {res}")

        details = {
            "page_id": channel,
            "psid": psid
        }

        if res["data"]:
            details["owner_app_id"] = res['data'][0]['thread_owner']['app_id']
        else:
            details["owner_app_id"] = ""
        return details


    # get name
    def get_name(self, channel, send_id):
        token = keyDictionary.get(channel)
        params = {
                    "access_token": token,
                    "id": send_id
                }
        headers = {"Content-Type": "application/json"}
        req = requests.get(GET_NAME, params=params, headers=headers)
        
        if req.status_code != 200:
            print(req.status_code)
            print(req.text)
            return None

        req = req.json()    
        return req
    
    # add persistent menu
    def add_persistent_menu(self, channel, send_id):
        token = keyDictionary.get(channel)
        params = {
                    "access_token": token
                }
        headers = {"Content-Type": "application/json"}
        data = json.dumps({
            "psid": send_id,
            "persistent_menu": [
                {
                    "locale": "default",
                    "composer_input_disabled": False,
                    "call_to_actions": [
                        {
                            "type": "postback",
                            "title": BUTTON_MY_GLOBE_ACCOUNT,
                            "payload": PAYLOAD_MY_GLOBE_ACCOUNT
                        },
                        {
                            "type": "postback",
                            "title": BUTTON_SHOP_PLANS_OFFERS,
                            "payload": PAYLOAD_SHOP_PLANS_OFFERS
                        }
                    ]
                }
            ]
        })

        req = requests.post(SET_PERSISTENT_MENU, params=params, headers=headers, data=data)

        if req.status_code != 200:
            print("ADD PERSISTENT MENU | FAIL | {} | {}".format(channel,send_id))
        else:
            print("ADD PERSISTENT MENU | SUCCESS | {} | {}".format(channel,send_id))


    # NIAS 2.0 - Delete persistent menu per user
    def delete_persistent_menu(self, channel, send_id):
        token = keyDictionary.get(channel)
        params = {
                    "access_token": token,
                    "psid": send_id,
                    "params": '["persistent_menu"]'
                }
        headers = {"Content-Type": "application/json"}

        try:
            req = requests.delete(SET_PERSISTENT_MENU, params=params, headers=headers)
        except Exception as error:
            logger.error(f"DELETE persistent_menu API error: {get_exception_str(error)}")
            return False

        logger.info(f"DELETE persistent_menu response: {req.json()}")
                
        if req.status_code == 200 and req.json()['result'].upper() ==  "SUCCESS":
            return True
        
        logger.info(f"DELETE persistent_menu FAILED for {send_id}")
        return False


    # NIAS 2.0 - Chech if persistent menu is enabled to a specific user
    def is_persistent_menu_enabled(self, channel, send_id):
        token = keyDictionary.get(channel)
        params = {
            "access_token": token,
            "psid": send_id
        }
        headers = {"Content-Type": "application/json"}

        try:
            req = requests.get(SET_PERSISTENT_MENU, params=params, headers=headers)
        except Exception as error:
            logger.error(f"GET persistent_menu error: {get_exception_str(error)}")
            return True
        
        logger.info(f"GET persistent_menu response: {req.json()}")

        if req.status_code != 200:
            logger.info(f"GET persistent_menu FAILED for {send_id}")
            return True

        for data in req.json()['data']:
            if 'user_level_persistent_menu' in data.keys():
                return True

        return False

    
    def take_control(self, channel, send_id, previousThreadOwner="N/A"):
        data = json.dumps({
            "recipient": {"id": send_id},
            "metadata": "Taking control from secondary app"
        })

        token = keyDictionary.get(channel)
        params = {
                    "access_token": token
                }
        headers = {"Content-Type": "application/json"}

        req = requests.post(HANDOVER_TAKE_URL, params=params, headers=headers, data=data)

        if req.status_code != 200:
            print("TAKE CONTROL | FAIL | {} | {} | {}".format(channel,send_id,previousThreadOwner))
        else:
            print("TAKE CONTROL | SUCCESS | {} | {} | {}".format(channel,send_id,previousThreadOwner))

    def send_media_list(self, params, headers, page, send_id, media_list, personaToggle):
        elements = []

        for media in media_list:
            element = {
                "title": media["media-header"],
                "image_url": media["media-image"]
            }

            elements.append(element)

        request = {
            "recipient":{
                "id": send_id,
            },
            "message":{
                "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements
                }
                }    
            }
        }

        self.__handle_persona(personaToggle,request,page)
        data = json.dumps(request)
        req = requests.post(GRAPH_API_URL, params=params, headers=headers, data=data)
        
        if req.status_code != 200:
            print(req.status_code)
            print(req.text)
    
    def send_media_title_subtitle_carousel(self, params, headers, page, send_id, media_list, personaToggle):	
        elements = []	
        for media in media_list:	
            element = {	
                "title": media["media-header"],	
                "subtitle": media["media-subtitle"],	
                "image_url": media["media-image"]	
            }	
            elements.append(element)	
        request = {	
            "recipient":{	
                "id": send_id,	
            },	
            "message":{	
                "attachment": {	
                "type": "template",	
                "payload": {	
                    "template_type": "generic",	
                    "elements": elements	
                }	
                }    	
            }	
        }	
        self.__handle_persona(personaToggle,request,page)	
        data = json.dumps(request)	
        req = requests.post(GRAPH_API_URL, params=params, headers=headers, data=data)	
        	
        if req.status_code != 200:	
            print(req.status_code)	
            print(req.text)
            
    def __handle_message_tag(self, messageTagToggle, request):
        if messageTagToggle:
            request["messaging_type"] = "MESSAGE_TAG"
            request["tag"] = "ACCOUNT_UPDATE"
                        
    def __handle_private_reply(self, is_private_reply, request, send_id):
        if is_private_reply:
            del request["recipient"]["id"]
            request["recipient"]["comment_id"] = send_id
            
    def __handle_persona(self, personaToggle, request, page):
        if personaToggle:
            if page in page_persona_mapping_dict:
                request["persona_id"] = page_persona_mapping_dict[page]

    def __get_app_rate_limit_reached_timestamp_value(self) -> str:
        current_date_str = get_current_time()
        monit_res = self.__ddb_monitoring.get_item("name", monitoring.APP_RATE_LIMIT_REACHED_TIMESTAMP)
        if not monit_res:
            self.__update_monitoring_value(monitoring.APP_RATE_LIMIT_REACHED_TIMESTAMP, current_date_str)
            return current_date_str
        return monit_res[0]["value"]

    
    def __get_app_rate_limit_status(self) -> str:
        if not self.__ddb_monitoring:
            self.__ddb_monitoring = DDBTools(DDB_MONITORING, REGION_OREGON)

        monit_res = self.__ddb_monitoring.get_item("name", monitoring.APP_RATE_LIMIT_STATUS)

        return monit_res[0]["value"].strip().upper() if monit_res else STATUS_GREEN


    def __is_app_rate_limit_reached(self):
        rate_limit_status = self.__get_app_rate_limit_status()
        limit_reached_timestamp_value = self.__get_app_rate_limit_reached_timestamp_value()
        current_date_str = get_current_time()

        try:
            if not limit_reached_timestamp_value:
                app_rate_limit_reached_timestamp = get_datetime_from_string(current_date_str)

                if rate_limit_status == STATUS_RED:
                    self.__update_monitoring_value(monitoring.APP_RATE_LIMIT_REACHED_TIMESTAMP, current_date_str)
            else:
                app_rate_limit_reached_timestamp = get_datetime_from_string(limit_reached_timestamp_value)
        except Exception as error:
            logger.error(f"Failed converting rate_limit_reached_timestamp {limit_reached_timestamp_value}: {get_exception_str(error)}")
            app_rate_limit_reached_timestamp = get_datetime_from_string(current_date_str)
            self.__update_monitoring_value(monitoring.APP_RATE_LIMIT_REACHED_TIMESTAMP, current_date_str)

        current_date = get_datetime_from_string(current_date_str)
        total_seconds_elapsed = (current_date - app_rate_limit_reached_timestamp).total_seconds()

        logger.info(f"Rate Limit Status: {rate_limit_status}, limit reached: {limit_reached_timestamp_value}, seconds elapsed: {total_seconds_elapsed}")
        
        if rate_limit_status == STATUS_GREEN:
            return False
        elif rate_limit_status == STATUS_RED:
            if total_seconds_elapsed > self.__APP_RATE_LIMIT_RETRY_SECONDS:
                return False
            else:
                return True
        return False


    def __update_monitoring_value(self, name: str, value: str = "") -> None:
        if not self.__ddb_monitoring:
            self.__ddb_monitoring = DDBTools(DDB_MONITORING, REGION_OREGON)

        try:
            self.__ddb_monitoring.update_item("name", name, {"value": value})
        except Exception as error:
            logger.error(f"Failed to update monitoring item: {name}. {get_exception_str(error)}")

    
    def __fb_error_handler(self, fb_response: dict = None) -> None:
        if fb_response == None:
            fb_response = {}

        if "error" in fb_response.keys():
            error_code = fb_response["error"]["code"]
            if error_code == FB_ERROR_CODE_RATE_LIMIT_REACHED:
                self.__update_monitoring_value(monitoring.APP_RATE_LIMIT_REACHED_TIMESTAMP, get_current_time())      
                self.__update_monitoring_value(monitoring.APP_RATE_LIMIT_STATUS, STATUS_RED)


    def __app_rate_limit_success_handler(self) -> None:
        self.__update_monitoring_value(monitoring.APP_RATE_LIMIT_STATUS, STATUS_GREEN)
        self.__update_monitoring_value(monitoring.APP_RATE_LIMIT_REACHED_TIMESTAMP, "")


    def get_ids_for_pages(self, channel: str, send_id: str) -> list:
        try:
            if self.__is_app_rate_limit_reached():
                logger.info(f"App rate limit is already reached. Will not invoke ids_for_pages.")
                return []
        except Exception as error:
            logger.error(f"Failed to check app rate limit monitoring value: {get_exception_str(error)}")

        token = keyDictionary.get(channel)
        params = {"access_token": token}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.get(IDS_FOR_PAGES.format(send_id), params=params, headers=headers)
        except Exception as error:
            logger.error(f"Failed to invoke {IDS_FOR_PAGES}: {get_exception_str(error)}")
            return []

        logger.info(f"ids_for_pages response: {response.json()}")

        try:
            if response.status_code != 200:
                res = response.json()
                self.__fb_error_handler(res)
             
                logger.info(f"ids_for_pages API failed")
                return []
        except Exception as error:
            logger.error(f"Failed to identify error code: {get_exception_str(error)}")
            return []

        self.__app_rate_limit_success_handler()
        return response.json()['data']


    def release_thread(self, channel:str, send_id:str, metadata: str = "") -> bool:
        data = json.dumps({
            "recipient": {"id": send_id},
            "metadata": metadata
        })
        token = keyDictionary.get(channel)
        headers = {"Content-Type": "application/json"}
        params = {
            "access_token": token
        }
        
        try:
            response = requests.post(RELEASE_THREAD_URL, params=params, headers=headers, data=data)
            logger.info(f"release_thread_control response: {response.json()}")
        except Exception as error:
            logger.error(f"Error invoking release_thread_control: {get_exception_str(error)}")
            return False

        if response.status_code != 200:
            logger.info("release_thread_control failed for user: {send_id}")
            return False

        logger.info(f"Successfully released thread for user: {send_id}")
        return True

    def hide_comment(self, params, headers, comment_id):

        params["is_hidden"] = "true"
        try:
            response = requests.post(COMMENT_ID_URL.format(comment_id), params=params, headers=headers)
            logger.info(f"hiding comment id({comment_id})  response: {response.json()}")
        except Exception as error:
            logger.error(f"Error hiding comment id ({comment_id}): {get_exception_str(error)}")
            return False

        if response.status_code != 200:
            logger.info("hiding comment failed, id: {comment_id}")
            return False

        logger.info(f"Successfully hide comment: {comment_id}")
        return True