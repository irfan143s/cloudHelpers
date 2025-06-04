import os
import json
import boto3
import logging

from helpers.tools import keys_exist, find_item

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class LexTools:
    def __init__(self,userId, registered=True):
        self._bot = boto3.client('lex-runtime')

        if registered:
            self._botName=os.environ['bot_name']
            self._botAlias=os.environ['bot_alias']
        else:
            self._botAlias=os.environ['unregistered_bot_alias']
            self._botName=os.environ["unregistered_bot_name"]
        
        self._id=userId
        logger.info("created lex bot instance.")
        
    def get_message(self,lex_event):
        messagelist=[] 
        if keys_exist(lex_event, ['message']):
            message=lex_event['message']
            if "{\"messages\":" in message: 
                messages=json.loads(message)['messages']
                logger.info(message)
                for msg in messages:
                    messagelist.append(msg['value'])
            else:
                messagelist.append(message)
        return messagelist
            
    def get_state(self,lex_event):
        if keys_exist(lex_event,['dialogState']):
            state=lex_event['dialogState']
            return state
        else:
            return "error"
    
    def send_intent(self,intent, sessionAttributes={}, requestAttributes={}):
        response = self._bot.post_text(
            botName=self._botName,
            botAlias=self._botAlias,
            userId=self._id,
            sessionAttributes=sessionAttributes,
            requestAttributes=requestAttributes,
            inputText=intent
        )

        logger.info(f"lex response: {response}")
        return response
