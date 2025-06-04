import os
import boto3

from resources.spiels import OTHER_GLOBE_ACCOUNT_CHOSE_SPIEL,OTHER_GLOBE_ACCOUNT_GAH_SPIEL
from resources.constants import REG_OTHER_GLOBE_ACCOUNT_INTENT
class RegistrationTools:

    def revertNumberAndLob(self,dynamodb,event):
        if 'numberCache' in event:
            phoneNumberMap = event['registeredNumbers']
            number = event['numberCache']['number']
            lob = event['numberCache']['lob']
            event['lastNumber']=number
            event['lastBrand']=lob
            dynamodb.updateNumber(event['fbId'], (number), lob, phoneNumberMap)
        dynamodb.updateItem(event['fbId'], "lastIntent", REG_OTHER_GLOBE_ACCOUNT_INTENT)
        event['lastIntent']=REG_OTHER_GLOBE_ACCOUNT_INTENT
    def getChooseSpiel(self,lastNumber):
        if len(lastNumber)==9:
            numberType='account'
            number=lastNumber
        else:
            numberType='mobile'
            number = '0'+lastNumber
        
        return OTHER_GLOBE_ACCOUNT_CHOSE_SPIEL.format(numberType,number)

    def getGahSpiel(self,lastNumber):
        if len(lastNumber)!=9:
            lastNumber = '0'+lastNumber
            
        return OTHER_GLOBE_ACCOUNT_GAH_SPIEL.format(lastNumber)

    def removeRetailerAttribs(self,dynamodb,event):
        if 'languageOption' in event:
            dynamodb.removeAttribute(event['fbId'],'languageOption')
            event.pop('languageOption')
        if 'isRetailer' in event:
            dynamodb.removeAttribute(event['fbId'],'isRetailer')
            event.pop('isRetailer')

    def update_numberCache(self,dynamodb,event):
        if 'numberCache' in event:
            dynamodb.updateMap(event['fbId'],'numberCache','number',event['lastNumber'])
            dynamodb.updateMap(event['fbId'],'numberCache','lob',event['lastBrand'])
            event['numberCache']['number']=event['lastNumber']
            event['numberCache']['lob']=event['lastBrand']
    
    # def register_number(self,dynamodb,event,time):
    #     if 'otherRegisteredNumber' in event:
    #         senderId=event['fbId']
    #         lastNumber=event['lastNumber']
    #         lastBrand=event['lastBrand']
    #         if event['lastBrand'] not in event['otherRegisteredNumber']:
    #             dynamodb.addRegisteredNumberLob(senderId,lastBrand)
    #         dynamodb.addRegisteredNumberMap(senderId,lastBrand,lastNumber)
    #         dynamodb.updateRegisteredNumberMap(senderId,lastBrand,lastNumber,'registeredDate',time)