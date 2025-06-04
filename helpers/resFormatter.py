from configuration import pageDictionary, keyDictionary
from helpers.facebooktools import FacebookTools

class ResFormatter:

    def __init__(self, channel):
        self.__page = pageDictionary.get(channel)
        token = keyDictionary.get(channel)
        self.__params = {"access_token": token}
        self.__headers = {"Content-Type": "application/json"}
        self.__page_id = channel

    # regular messages
    def send_message(self, send_id, msg_txt, messageTagToggle = False, is_private_reply = False, personaToggle=True):
        if self.__page in pageDictionary.values():
            fbTools = FacebookTools()
            fbTools.send_message(self.__params, self.__headers, self.__page, send_id, msg_txt, messageTagToggle, is_private_reply, personaToggle)

    # cards
    def send_responseCard(self, send_id, title, subtitle, image_url, personaToggle=True):
        if self.__page in pageDictionary.values():
            fbTools = FacebookTools()
            fbTools.send_responseCard(self.__params, self.__headers, self.__page, send_id, title, subtitle, image_url, personaToggle)

    # menus
    def send_quickresponse(self, send_id, question, menu, formName, messageTagToggle = False, is_private_reply = False, personaToggle=True):
        if self.__page in pageDictionary.values():
            fbTools = FacebookTools()
            fbTools.send_quickresponse(self.__params, self.__headers, self.__page, send_id, question, menu, formName, messageTagToggle, is_private_reply, personaToggle)
    
    # carousel
    def send_carousel(self, send_id, headers, buttons, urlState, randomCards = False, personaToggle=True):
        if self.__page in pageDictionary.values():
            fbTools = FacebookTools()
            fbTools.send_carousel(self.__params, self.__headers, self.__page, send_id, headers, buttons, urlState, randomCards, personaToggle)

    # NIAS 2.0
    def send_option_buttons(self, send_id, spiel, buttons, urlState, messageTagToggle = False, is_private_reply = False, personaToggle=True):
        if self.__page in pageDictionary.values():
            fbTools = FacebookTools()
            fbTools.send_option_buttons(self.__params, self.__headers, self.__page, send_id, spiel, buttons, urlState, messageTagToggle, is_private_reply, personaToggle)

    # notification message optin
    def send_notif_message_optin(self, send_id, title, img_url, frequency, personaToggle=True):
        if self.__page in pageDictionary.values():
            fbTools = FacebookTools()
            fbTools.send_notif_message_optin(self.__params, self.__headers, self.__page_id, send_id, title, img_url, frequency,personaToggle)

    # send recurring notif message
    def send_recurring_notif_message(self, token, msg_txt, personaToggle=True):
        if self.__page in pageDictionary.values():
            fbTools = FacebookTools()
            return fbTools.send_recurring_notif_message(self.__params, self.__headers, self.__page, token, msg_txt, personaToggle)
        
    # send account update carousel
    def send_account_update_carousel(self, send_id, headers, buttons, randomCards = False, personaToggle=True):
        if self.__page in pageDictionary.values():
            fbTools = FacebookTools()
            fbTools.send_account_update_carousel(self.__params, self.__headers, self.__page, send_id, headers, buttons, randomCards, personaToggle)
    
    # send ces survey
    def send_ces_survey(self, send_id, title, sub_title, survey_title, personaToggle=True):
        if self.__page in pageDictionary.values():
            fbTools = FacebookTools()
            fbTools.send_ces_survey(self.__params, self.__headers, self.__page, send_id, title, sub_title, survey_title, personaToggle)
 
    #carousel
    def send_carousel_multiple_type(self, send_id, headers, buttons, randomCards = False, messageTagToggle = False, personaToggle=True):
        if self.__page in pageDictionary.values():
            fbTools = FacebookTools()
            fbTools.send_carousel_multiple_type(self.__params, self.__headers, self.__page, send_id, headers, buttons, randomCards, messageTagToggle, personaToggle)

    # media
    def send_media_type(self, send_id, fileType, attachmentId, personaToggle=True):
        if self.__page in pageDictionary.values():
            fbTools = FacebookTools()
            fbTools.send_media_type(self.__params, self.__headers, self.__page, send_id, fileType, attachmentId, personaToggle)

    # Media List
    def send_media_list(self, send_id, media_list, personaToggle=True):
        if self.__page in pageDictionary.values():
            fbTools = FacebookTools()
            fbTools.send_media_list(self.__params, self.__headers, self.__page, send_id, media_list, personaToggle)
    
    # media button
    def send_media_button(self, send_id, attachmentId, buttonData, personaToggle=True):
        if self.__page in pageDictionary.values():
            fbTools = FacebookTools()
            fbTools.send_media_button(self.__params, self.__headers, self.__page, send_id, attachmentId, buttonData, personaToggle)
    
    #offer details carousel
    def send_media_title_subtitle_carousel(self, send_id, media_list, personaToggle=True):
        if self.__page in pageDictionary.values():
            fbTools = FacebookTools()
            fbTools.send_media_title_subtitle_carousel(self.__params, self.__headers, self.__page, send_id, media_list, personaToggle)

    def hide_comment(self, comment_id):
        if self.__page in pageDictionary.values():
            fbTools = FacebookTools()
            fbTools.hide_comment(self.__params, self.__headers, comment_id)