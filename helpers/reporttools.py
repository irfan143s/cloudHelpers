
import json
import time
class ReportsTools:

    def list_separator(self,index:int,ls:list):
        list_of_list=[]
        while len(ls) > index:
            list_of_list.append(ls[:index])
            ls=ls[index:]
        else:
            if len(ls)!=0:
                list_of_list.append(ls)
        return list_of_list

    def find_item(self,dicts,key,value,ret):
        #finds specific key in list of dicts
        #[{},{},{}...]
        for item in dicts:
            if item[key] == value:
                return item[ret]
        else:
            return None

    def index_letter(self,col):
        #created this method for collumn based index where 1 is A,
        #A,AA,AZ,AAB
        letter = str()
        div = col
        while div:
            (div, mod) = divmod(div-1, 26)
            letter = chr(mod + 65) + letter
        return letter
    def start_query(self,client, query, lambda_names,startTime,endTime):
        try:
            resp = client.start_query(
                logGroupNames=lambda_names,
                startTime=int(startTime.timestamp()),
                endTime=int(endTime.timestamp()),
                queryString= query)
            return resp
        except client.exceptions.LimitExceededException as e:
            time.sleep(1)
            return self.start_query(client, query, lambda_names,startTime,endTime)
        except Exception as e:
            raise Exception(json.dumps({'statusCode':500,'body':e.__str__()}))

    def get_query_results(self,logClient,queryId):
        response= None
        #for waiting while query is ongoing
        while response == None or response['status']=='Running':
            #print('waiting')
            time.sleep(1)
            response = logClient.get_query_results(queryId=queryId['queryId'])
        else:
            print(response)
            return response

    def consolidate_data(self,data):
        consolidated_result = []
        #consolidated the whole row in one dictionary for ease of iteration during search
        #data =[ [{},{},...] , [{},{},...], ... ]
        for aggregated in data:
            #aggregated = [{},{},{}...]
            temp = {}
            for col in aggregated:
                temp[col['field']]= col['value']
            #consolidated_result = [{key:val,key:val,...},{key:val,key:val,...},...]
            consolidated_result.append(temp)
        
        return consolidated_result
