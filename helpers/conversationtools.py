import os, time
import logging
import datetime
import dateutil.tz

from configuration import TIMEZONE_PH

class ConversationTools:
    def __init__(self):
        self.timezone=dateutil.tz.gettz(TIMEZONE_PH)
        logging.basicConfig(level = logging.INFO)
        self.logger = logging.getLogger()
        # self.logger.handlers[0].setFormatter(logging.Formatter(fmt='[{levelname}], {message}', datefmt="%m-%d-%Y,%H:%M:%S.%z",style='{'))
        self.logger.setLevel(logging.INFO)
    
    def log(self, senderId, lastNumber, lastBrand, source, lastIntent,  message):
        self.logger.info(str(datetime.datetime.now(tz=self.timezone))+"|"+senderId +"|"+lastNumber+"|"+lastBrand+"|"+source+"|FACEBOOK MESSENGER|"+lastIntent+"|"+message)

    def log_report(self, senderId, lastNumber, lastBrand, source, lastIntent, sessionState, subState, channel, lastIntentDate, details, message):
        self.logger.info(str(datetime.datetime.now(tz=self.timezone))+"|"+senderId +"|"+lastNumber+"|"+lastBrand+"|"+source+"|FACEBOOK MESSENGER|"+lastIntent+"|"
        + sessionState + "|" + subState + "|" + channel + "|" + lastIntentDate + "|" + details + "|" + message)

    def log_payment_status(self, senderId, mobileNumber, lobName, numberType, denomination, paymentMethod, paymentStatus, paymentId, AMAXstatus, AMAXId, details):
        self.logger.info(str(datetime.datetime.now(tz=self.timezone))+"|"+senderId +"|"+mobileNumber+"|"+ lobName + "|" +numberType +"|"+denomination+"|"+paymentMethod+"|"
        + paymentStatus + "|" + paymentId + "|" + AMAXstatus + "|" + AMAXId + "|" + details)

    def log_thea_DonateToFrontliners(self, mobileNumber, selectedBeneficiary, giftItem, numberOfTreats, recurringUser, noteName, details="Thea donate to frontliners"):
        self.logger.info(str(datetime.datetime.now(tz=self.timezone))+"|"+mobileNumber +"|"+selectedBeneficiary+"|"+ giftItem + "|" + numberOfTreats + "|" + recurringUser + "|" + noteName + "|" + details)
        
    def missed_intent(self, senderId, message):
        self.logger.info(str(datetime.datetime.now(tz=self.timezone)) + "|" + senderId + "|MISSED|" + message)

    def cms_log(self, spielKey, spiel):
        self.logger.info(str(datetime.datetime.now(tz=self.timezone)) + "|" + spielKey + "|" + spiel)