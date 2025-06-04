import os
import json
import boto3
import time

from datetime import datetime
import dateutil.tz

from configuration import TIMEZONE_PH, REGION

class LogGroupTools:

    def __init__(self):
        self.client = boto3.client('logs',region_name=REGION)
        self.timezone=dateutil.tz.gettz(TIMEZONE_PH)
    def log_parse(self,senderId, lastNumber, lastBrand, source, facebookmessenger, lastIntent, sessionState, subState, channel, lastIntentDate, details, messageText):
        return f"[INFO], {str(datetime.now(tz=self.timezone))}|{senderId}|{lastNumber}|{lastBrand}|{source}|{facebookmessenger}|{lastIntent}|{sessionState}|{subState}|{channel}|{lastIntentDate}|{details}|{messageText}"

    def check_aplication_log_parse(self,senderId,lastNumber,lastBrand,channel,option_chosen,reference_number,name,email_address):
        return f"[CHECK-APPLICATION], {str(datetime.now(tz=self.timezone))}|{senderId}|{lastNumber}|{lastBrand}|{channel}|{option_chosen}|{reference_number}|{name}|{email_address}"

    def put_log(self,logGroupName:str,message:str):
        """[summary]
            creates a log stream for a specific log group
            and adds the message as log in the log stream
        Args:
            logGroupName (str): name of the logGroup
            message (str): log to be added to the log group

        Returns:
            [dict]: {
                'nextSequenceToken': 'string',
                'rejectedLogEventsInfo': {
                    'tooNewLogEventStartIndex': 123,
                    'tooOldLogEventEndIndex': 123,
                    'expiredLogEventEndIndex': 123
                }
            }
        """
        now_time = time.time()
        logStreamName = time.strftime('%d/%b/%Y-') + str(int(round(now_time*1000)))
        self.client.create_log_stream(
            logGroupName=logGroupName,
            logStreamName = logStreamName
        )
        # can be modified to recieve groups of messages
        resp = self.client.put_log_events(
            logGroupName=logGroupName,
            logStreamName=logStreamName,
            logEvents=[
                {
                    'timestamp': int(round(now_time*1000)),
                    'message': message
                }
            ]
        )
        return resp
