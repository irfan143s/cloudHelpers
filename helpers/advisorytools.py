import helpers.utils as utils
from helpers.facebooktools import FacebookTools
from helpers.resFormatter import ResFormatter
from helpers.ddbtools import DDBTools

from configuration import *
from resources.aws_lambda import *
from resources.constants import *
from resources.spiels import *
from resources.resourcemapping import *
from helpers.sessiontools import SessionTools
import concurrent.futures
import logging
import json
import boto3
invokeConnect = boto3.client("lambda", region_name=SYD_REGION)
invokeLamdba = boto3.client("lambda", region_name = REGION_OREGON)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class AdvisoryNotice:

    def __init__(self, sender_id, page_id,event):
        self.__page_id = page_id
        self.__sender_id = sender_id
        self.__response_formatter = ResFormatter(page_id)

        self.__event = event
        self.__ddb_client_main = DDBTools(page_ddb_mapping_dict[page_id]['main'], REGION_OREGON)
        self.__init_main_data()
        
        


    def __init_main_data(self):
##    executor = ProcessPoolExecutor(max_workers=3)
        data = self.__ddb_client_main.get_item("fbId", self.__sender_id)[0]
        logger.info(f"data inside advisory {data}")
        if "advisoryPriority"  in data.keys():
            self.__priority = int(data['advisoryPriority'])
        else:
            self.__priority = 0
            self.__update_data("advisoryPriority","0")
        if "advisoryPriority"  in data.keys():
            if data["advisories"] != "String":
                self.__advisories = data["advisories"]
        else:
            self.__advisories = "String"
        self.__state = data['subState']
        self.__session_state = data['sessionState']

        if self.__page_id == GT_PAGE_ID:
            self.__page_name = GT_PAGE_NAME
        elif self.__page_id == MYBUSINESS_PAGE_ID:
            self.__page_name = MYBUSINESS_PAGE_NAME
        elif self.__page_id == THEA_PAGE_ID:
            self.__page_name = THEA_PAGE_NAME
        elif self.__page_id == TM_PAGE_ID:
            self.__page_name = TM_PAGE_NAME
        elif self.__page_id == GAH_PAGE_ID:
            self.__page_name = GAH_PAGE_NAME  

        if self.__state == 'ADVISORY-INITIALIZATION':
            with  concurrent.futures.ThreadPoolExecutor() as executor:
                task1 = executor.submit(self.__api_caller,"1")
                task2 = executor.submit(self.__api_caller,"2")
                task3 = executor.submit(self.__api_caller,"3")
                arrayAdvisories = []
                arrayAdvisories.extend([task1.result(),task2.result(),task3.result()])
                self.__update_data("advisories",arrayAdvisories)
                self.__update_data("sessionState","ADVISORY-PRIORITY-0")

    def __api_caller(self,priority):      
        connectRequest = {
            "pageName": self.__page_name,
            "Details": {
                "ContactData": {
                    "Attributes": {
                        "advisorypriority":priority,
                        "lobAdvisory": "false"
                    },
                    "CustomerEndpoint": {
                        "Address": ""
                    }
                },
                "Parameters": {
                }
            },
            "Name": "Lex"

        }
        logger.info("--------------invoking advisorySettings--------------")
        logger.info(f"Request: {connectRequest}")
        connectResponse = None
        
        try:
            connectResponse = invokeConnect.invoke(FunctionName=ADVISORY_SETTINGS_LAMBDA, InvocationType="RequestResponse", Payload=json.dumps(connectRequest))
            connectResponse = json.loads(connectResponse['Payload'].read().decode())
        except Exception as error:
            logger.info(f"Error invoking advisorySettings: {str(error)}")
            connectResponse = {"status": "error in advisory"}
        logger.info(f"Response advisorySettings: {connectResponse}")
        return connectResponse

    def __advisory_short(self,advisory,priority):
        if self.__state =="ADVISORY-SHORT":
            if "optionId" in self.__event.keys():
                logger.info(f"inside advisory short")
                option_id = self.__event["optionId"]
                self.__update_data("subState","ADVISORY-SHORT-RESET")
                self.__state = "ADVISORY-SHORT-RESET"
                if option_id in [ADVISORY_LONG_YES0,ADVISORY_LONG_YES1,ADVISORY_LONG_YES2]:
                    self.__update_data('sessionState','ADVISORY-PRIORITY-'+str(priority)+'-AGENT')
                    self.__response_formatter.send_message(self.__sender_id, advisory['LongSpiel'])
                    self.__session_state = 'ADVISORY-PRIORITY-'+str(priority)+'-AGENT'
                    self.advisory_processor()
                elif option_id in [ADVISORY_LONG_NO0,ADVISORY_LONG_NO1,ADVISORY_LONG_NO2]:
                    self.__update_data('sessionState','ADVISORY-PRIORITY-'+str(priority)+'-AGENT')
                    self.__session_state = 'ADVISORY-PRIORITY-'+str(priority)+'-AGENT'
                    self.advisory_processor()              
                else:
                    self.__render_advisory_options('short',advisory["ShortSpiel"],priority)
            else:

                self.__response_formatter.send_message(self.__sender_id, UNRECOGNIZE_SPIEL)
                self.__render_advisory_options('short',advisory["ShortSpiel"],priority)
            
        else:
            if advisory["LongFlag"] == "true":
                self.__response_formatter.send_message(self.__sender_id, advisory["ShortSpiel"])
                self.__render_advisory_options('short',advisory["ShortSpiel"],priority)
            else:
                self.__response_formatter.send_message(self.__sender_id, advisory["ShortSpiel"])
                self.__session_state = 'ADVISORY-PRIORITY-'+str(priority)+'-AGENT'
                self.advisory_processor()

    def __advisory_agent(self,advisory,priority):
        logger.info(f"inside advisory agent")
        if self.__state =="ADVISORY-AGENT":
            if "optionId" in self.__event.keys():
                option_id = self.__event["optionId"]
                self.__update_data("subState","ADVISORY-AGENT-RESET")
                self.__state ="ADVISORY-AGENT-RESET" 

                if option_id in [ADVISORY_AGENT_YES0,ADVISORY_AGENT_YES1,ADVISORY_AGENT_YES2]:
                    self.__transfer_to_csr()
                elif option_id in [ADVISORY_AGENT_NO0,ADVISORY_AGENT_NO1,ADVISORY_AGENT_NO2]:    
                    self.__update_data( 'sessionState','ADVISORY-PRIORITY-'+str(priority+1) )
                    self.__update_data('advisoryPriority',str(self.__priority+1))
                    self.__session_state = 'ADVISORY-PRIORITY-'+str(priority+1)
                    self.__priority =self.__priority+1
                    self.advisory_processor()        
                else:
                    logger.info("Invalid input")
                    self.__render_advisory_options('agent',advisory["AgentSpiel"],priority)   
            
        else:
            self.__render_advisory_options('agent',advisory["AgentSpiel"],priority)

    def __transfer_to_csr(self):
        # lob either postpaid or main     
        intent_id = socioBasket[self.__page_id]['main']
        utils.invoke_transfer_to_agent(self.__event, intent_id, {})
    
    def __render_advisory_options(self,method,advisorySpiel,priority):
        if method == "short":
            option = ADVISORY_LONG_OPTIONS_SPIEL     
            spiel = option['spiel']
            self.__update_data("subState","ADVISORY-SHORT")
            self.__update_data('sessionState','ADVISORY-PRIORITY-'+str(priority)+"-SHORT")
        else:
            option = ADVISORY_AGENT_OPTIONS_SPIEL
            spiel = option['spiel'].format(advisorySpiel)
            self.__update_data('sessionState','ADVISORY-PRIORITY-'+str(priority)+"-AGENT")
            self.__update_data("subState","ADVISORY-AGENT")
        logger.info(f"Option spiel buttons: {option['buttons']}")
        buttons = utils.append_string_to_option_ids(option['buttons'], "advisory"+str(priority))
        self.__response_formatter.send_option_buttons(self.__sender_id, spiel, buttons, False)

    def __advisory_exit(self,priority):
        logger.info(f"Entering Advisory Exit")
        if(priority <2): 
            logger.info(f"Current Priority {priority}, looping")
            self.__update_data('advisoryPriority',str(priority+1))
            self.__update_data('sessionState','ADVISORY-PRIORITY-'+str(priority+1))
            self.__session_state = 'ADVISORY-PRIORITY-'+str(priority+1)
            self.__priority= self.__priority +1
            self.advisory_processor()
        else:
            logger.info(f"Last priority done ")
            if self.__page_name == THEA_PAGE_NAME:
                self.__event['sessionState'] = ADVISORY_EXIT_THEA_STATE
                self.__update_data('sessionState',ADVISORY_EXIT_THEA_STATE)                     
                invokeLamdba.invoke(FunctionName=THEA_MENU_LAMBDA,InvocationType="Event", Payload=json.dumps(self.__event))               
                return True
            else:
                self.__event['subState'] = 'ADVISORY-EXIT'
                self.__event['sessionState'] = MAIN_MENU_STATE
                self.__update_data('subState','ADVISORY-EXIT')
                self.__update_data('sessionState',MAIN_MENU_STATE)                      
                invokeLamdba.invoke(FunctionName=MAIN_MENU_LAMBDA,InvocationType="Event", Payload=json.dumps(self.__event))
                return True

    def __update_data(self, item,data):
            item = { 
                item: data 
            }
            self.__ddb_client_main.update_item('fbId', self.__sender_id, item)

    # *******************************************************************************************************************************
    # ********************************************** Public methods *****************************************************************
    # *******************************************************************************************************************************

    def advisory_processor(self):
        priority = self.__priority
        if priority == 3:
            self.__advisory_exit(priority)
        else:
            if self.__session_state.startswith('ADVISORY-PRIORITY-'):
                priority = int(self.__session_state.split("-")[2])        
            advisory = self.__advisories[priority]
            logger.info(f"priority {priority}")
            logger.info(f"session_state {self.__session_state}")
            logger.info(f"checking {advisory}")
            if "AFFlag" in advisory and  advisory["AFFlag"] == "true":
                if "ShortFlag" in advisory and advisory["ShortFlag"] =="true" and "ShortSpiel" in advisory and advisory["ShortSpiel"] and advisory["ShortSpiel"].strip() and (self.__session_state == 'ADVISORY-PRIORITY-'+str(priority) or self.__session_state == 'ADVISORY-PRIORITY-'+str(priority)+'-SHORT'):
                    self.__advisory_short(advisory,priority)
                else:
                    if "AgentFlag" in advisory and advisory["AgentFlag"] == "true" and "AgentSpiel" in advisory and advisory["AgentSpiel"] and advisory["AgentSpiel"].strip() and  (self.__session_state == 'ADVISORY-PRIORITY-'+str(priority) or self.__session_state == 'ADVISORY-PRIORITY-'+str(priority)+'-AGENT'):
                        self.__advisory_agent(advisory,priority)
                    else:
                        self.__advisory_exit(priority)
                        return True

            else:
                logger.info(f"AFF flag doesn't exist or false: {advisory}")
                self.__advisory_exit(priority)
                return True

                    