import os
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr
from datetime import date, datetime, timedelta, timezone
import dateutil.tz

from configuration import TIMEZONE_PH

from botocore.exceptions import ClientError

class DbTools:
    _user_session = {}
    # Constructor info
    
    def __init__(self, region, tableName=None):
        self.__connector=boto3.resource("dynamodb", region_name=region)
        if tableName!=None:
            self.__table=self.getTable(tableName)
            self.timezone=dateutil.tz.gettz(TIMEZONE_PH)
            # print("created access to "+tableName)
        # print("dynamodb object created")


    def _updateStates(self, sessionState, subState):
        self._user_session.update({
            "sessionState": sessionState, "subState": subState})

        return self._user_session


    def _updateItem(self, columnName, value):
        self._user_session.update({str(columnName): value})
        return self._user_session


    def _addMap(self, mapName):
        self._user_session.update({str(mapName): {}})
        return self._user_session


    def _updateMap(self, mapName, fieldName, value):
        self._user_session[str(mapName)].update({str(fieldName): value})
        return self._user_session


    def _updateNumber(self, lastNumber ,lastBrand, registeredNumbers):
        self._user_session.update({
            "lastNumber": lastNumber,
            "lastBrand": lastBrand,
            "registeredNumbers": registeredNumbers
        })
        return self._user_session


    def _updateIntent(self, fbId, intent):
        time=str(datetime.now(tz=self.timezone))
        self._user_session.update({
            "lastIntent": intent,
            "lastIntentDate": time
        })
        return self._user_session


    def _addRegisteredNumberLob(self, lob):
        self._user_session["otherRegisteredNumber"].update({
            str(lob): {}})

        return self._user_session


    def _addRegisteredNumberMap(self, lob, number):
        self._user_session["otherRegisteredNumber"][str(lob)]\
        .update({str(number): {}})

        return self._user_session


    def _updateRegisteredNumberMap(self, lob, number, field, value):
        self._user_session["otherRegisteredNumber"][str(lob)][str(number)]\
        .update({str(field): value})
        
        return self._user_session


    def _removeAttribute(self, attribute):
        try:
            del self._user_session[attribute]
        except KeyError:
            pass
        
        return self._user_session

    def _add_transaction_start_date(self, event, sessionState):
        timezone = dateutil.tz.gettz(TIMEZONE_PH)
        now = datetime.now(tz=timezone)
        now = now.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        if 'transaction_start_date' not in event:
            self._addMap("transaction_start_date")
        self._updateMap("transaction_start_date", sessionState, now)

        return now

    #handle restoration of resend, retry, and state
    def _stateReset(self, state):
        self._updateStates(state, "0")
        self._updateItem("resend", "0")
        self._updateItem("retry", "0")
        self._updateItem("unrecognizedRetry", "0")


    def _saveSession(self):
        return self.__table.put_item(Item=self._user_session)
    def getTable(self, tableName):
        return(self.__connector.Table(tableName))
        
        
    def getRowEquals(self, tableColumn, tableValue):
        row=self.__table.query(KeyConditionExpression=Key(tableColumn).eq((tableValue)))
        return(row)

    def getRowEqualsWithSort(self, partitionKey, partitionValue, sortKey, sortValue):
        row=self.__table.query(KeyConditionExpression=Key(partitionKey).eq(partitionValue) & Key(sortKey).eq(sortValue))
        return(row)
        
    def getSessionState(self, fbId):
        row=self.getRowEquals("fbId", fbId)
        session=row['Items'][0]['sessionState']
        return(session)
        
    def getSubState(self, fbId):
        row=self.getRowEquals("fbId", fbId)
        sub=row['Items'][0]['subState']
        return(sub)
    
    def getMobileNumber(self, fbId):
        row=self.getRowEquals("fbId", fbId)
        sub=row['Items'][0]['MobileNumber']
        return(sub)
        
    def addItem(self, fbId, fbName, channel, sessionState, subState,lastBrand,lastNumber, educationalDate, socio , otp , 
                lastOtp,registeredNumber,retry,resend, lastIntent, lastIntentDate, unrecognizedRetry, 
	            inSession, jrDate, advisory1Date, advisory2Date, advisory3Date, newUserDate, registeredDate) :        
        item={
            "fbId": fbId,
            "fbName": fbName,
            "channel": channel,
            "sessionState":sessionState,
            "subState":subState,
            "lastBrand":lastBrand,
            "lastNumber":lastNumber,
            "educationalDate":educationalDate,
            "socio":socio,
            "otp":otp,
            "lastOtp":lastOtp,
            "registeredNumbers":{},
            "retry":retry,
            "resend":resend,
            "lastIntent":lastIntent,
            "lastIntentDate":lastIntentDate,
            "unrecognizedRetry":unrecognizedRetry,
            "inSession":inSession,
            "jrDate": jrDate,
            "advisory1Date": advisory1Date,
            "advisory2Date": advisory2Date,
            "advisory3Date": advisory3Date,
            "newUserDate": newUserDate,
            "registeredDate": registeredDate
        }
        return self.__table.put_item(Item=item)
    
    def updateItem(self, fbId, columnName, value):
        return self.__table.update_item(
            Key={
                'fbId': fbId
            },
            UpdateExpression="set "+str(columnName)+"= :s",
            ExpressionAttributeValues={
              ':s': value,
              },
        )

    def deleteItem(self, fbId, columnName):
        return self.__table.update_item(
            Key={
                'fbId': fbId
            },
            UpdateExpression="remove "+str(columnName)
        )
    
    def addMap(self, fbId, mapName):
        return self.__table.update_item(
            Key={
                'fbId': fbId
            },
            UpdateExpression="set " + f"#{str(mapName)}" + "= :s",
            ExpressionAttributeNames={
                f"#{str(mapName)}": str(mapName),
            },
            ExpressionAttributeValues={
              ':s': {},
             },
        )

    def updateMap(self, fbId, mapName, fieldName, value):
        return self.__table.update_item(
            Key={
                'fbId': fbId
            },
            UpdateExpression="set " + f"#{str(mapName)}.#{str(fieldName)}" + "= :s",
            ExpressionAttributeNames={
                f"#{str(mapName)}": str(mapName),
                f"#{str(fieldName)}": str(fieldName)
            },
            ExpressionAttributeValues={
              ':s': value,
             },
        )
    
    def addRegisteredNumberLob(self,fbId,lob):
          expresssion_lob = str(lob).replace(" ","")
          print(expresssion_lob)
          return self.__table.update_item(
            Key = {
                'fbId':fbId
            },
            UpdateExpression="set "+ f"otherRegisteredNumber.#{expresssion_lob} = :s",
            ExpressionAttributeNames={
                f"#{expresssion_lob}":str(lob)
            },
            ExpressionAttributeValues={
                ':s':{},
            }
        )

    def addRegisteredNumberMap(self,fbId,lob,number):
        expresssion_lob = str(lob).replace(" ","")
        return self.__table.update_item(
            Key = {
                'fbId':fbId
            },
            UpdateExpression="set "+ f"otherRegisteredNumber.#{expresssion_lob}.#{str(number)} = :s",
            ExpressionAttributeNames={
                f"#{expresssion_lob}":str(lob),
                f"#{str(number)}":str(number)
            },
            ExpressionAttributeValues={
                ':s':{},
            }
        )

    def updateRegisteredNumberMap(self,fbId,lob,number,field,value):
        expresssion_lob = str(lob).replace(" ","")
        expression_field= str(field).replace(" ","")
        return self.__table.update_item(
            Key = {
                'fbId':fbId
            },
            UpdateExpression="set "+ f"otherRegisteredNumber.#{expresssion_lob}.#{str(number)}.#{str(expression_field)} = :s",
            ExpressionAttributeNames={
                f"#{expresssion_lob}":str(lob),
                f"#{str(number)}":str(number),
                f"#{expression_field}":str(field)
            },
            ExpressionAttributeValues={
                ':s':value,
            }
        )

    
    def updateStates(self, fbId, sessionState, subState):
        return self.__table.update_item(
            Key={
                'fbId': fbId
            },
            UpdateExpression="set sessionState = :s, subState = :ss",
            ExpressionAttributeValues={
              ':s': sessionState,
              ':ss': subState
              },
        )

    def updateNumber(self, fbId, lastNumber ,lastBrand, registeredNumbers):
        return self.__table.update_item(
            Key={
                'fbId': fbId
            },
            UpdateExpression="set lastNumber = :n, lastBrand = :b , registeredNumbers = :r",
            ExpressionAttributeValues={
              ':n': lastNumber,
              ':b': lastBrand,
              ':r': registeredNumbers
              },
        )

    def updateIntent(self, fbId, intent):
        time=str(datetime.now(tz=self.timezone))
        return self.__table.update_item(
            Key={
                'fbId': fbId
            },
            UpdateExpression="set lastIntent = :s, lastIntentDate = :ss",
            ExpressionAttributeValues={
              ':s': intent,
              ':ss': time
              },
        )
    # Constructor info
    
    def __init__(self, region, tableName=None):
        self.__connector=boto3.resource("dynamodb", region_name=region)
        if tableName!=None:
            self.__table=self.getTable(tableName)
            self.timezone=dateutil.tz.gettz(TIMEZONE_PH)
            # print("created access to "+tableName)
        # print("dynamodb object created")

    #handle restoration of resend, retry, and state
    def stateReset(self, senderId, state):
        self.updateStates(senderId, state, "0")
        self.updateItem(senderId, "resend", "0")                
        self.updateItem(senderId, "retry", "0")
        self.updateItem(senderId, "unrecognizedRetry", "0")

    # logs

    # get count of new users
    def getNewUserCount(self,fromDate=None,toDate=None,days=7):
        fe = Key('newUserDate').between(str(fromDate),str(toDate))

        scan_kwargs = {
            'FilterExpression': fe
        }
        
        done = False
        start_key = None
        count = 0

        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = self.__table.scan(**scan_kwargs)
            count =  count + response["Count"]
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

        return count
    
    # get count of new users
    def getRegisteredCount(self,fromDate=None,toDate=None,days=7):
        fe = Key('registeredDate').between(str(fromDate),str(toDate))

        scan_kwargs = {
            'FilterExpression': fe
        }
        
        done = False
        start_key = None
        count = 0

        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = self.__table.scan(**scan_kwargs)
            count =  count + response["Count"]
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

        return count
    
    # get registered users
    def getRegisteredUsers(self,fromDate=None,toDate=None,days=7):
        fe = Key('registeredDate').between(str(fromDate),str(toDate))

        scan_kwargs = {
            'FilterExpression': fe
        }
        
        done = False
        start_key = None
        responseItems = {}
        responseItems["Items"] = []

        while not done:
            if start_key:
                scan_kwargs['ExclusiveStartKey'] = start_key
            response = self.__table.scan(**scan_kwargs)
            responseItems["Items"] = responseItems["Items"] + response["Items"]
            start_key = response.get('LastEvaluatedKey', None)
            done = start_key is None

        return responseItems

    def updateCMSRow(self, spielKey, spiel):
        response=self.__table.update_item(
            Key={
                'spielKey':spielKey,
            },
            UpdateExpression="SET timeChanged= :var1, spiel= :var2",
            ExpressionAttributeValues={
                ':var1': str(datetime.now()),
                ':var2': spiel
            },
            ReturnValues="ALL_OLD"
        )
        return response

    def removeAttribute(self,fbId,attribute):
        self.__table.update_item(
            Key={
                'fbId': fbId
            },
            UpdateExpression = f'REMOVE {attribute}'
        )

    def remove_map_attributes(self,fbId,maps,attributes:list=[]):
        """[method to delete map attributes and attributes in dynamodb]
        Args:
            fbId ([string]): 123128936
            maps ([Dictionary]): {
                'buyload':['paymentId','amount']
            }
            attributes([list]): ['flag','temporary_attribute']
        """
        expression_list=[]

        for map_name,map_attributes in maps.items():
            for map_attribute in map_attributes:
                expression_list.append(f"{map_name}.{map_attribute}")
        if attributes:
            expression_list.extend(attributes)
                
        self.__table.update_item(
            Key={
                'fbId': fbId
            },
            UpdateExpression = 'REMOVE '+", ".join(expression_list)
        )        

    def add_transaction_start_date(self, fbId, event, sessionState):
        timezone = dateutil.tz.gettz(TIMEZONE_PH)
        now = datetime.now(tz=timezone)
        now = now.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        if 'transaction_start_date' not in event:
            self.addMap(fbId,"transaction_start_date")
        self.updateMap(fbId, "transaction_start_date", sessionState, now)

        return now