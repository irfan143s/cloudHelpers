# NIAS 2.0 - HISAMS
import boto3
import logging

from boto3.dynamodb.conditions import Key, Attr

from helpers.utils import *

from resources.tableschemas import *                                                                                                                                                                                              

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DDBTools:

    __WAITER_CONFIG = {
        'Delay': 20,
        'MaxAttempts': 30
    } # 10 mins

    def __init__(self, table_name=None, region=None):
        if not region:
            raise ValueError('Invalid region:', region)
        if not table_name:
            raise ValueError('Invalid table_name:', table_name)

        self.__table_name = table_name
        self.__region = region
        self.__client = boto3.client("dynamodb", region_name = region) 
        self.__connector = boto3.resource("dynamodb", region_name = region)
        self.__table = self.__connector.Table(table_name)

        
    def put_item(self, item={}):
        try:
            return self.__table.put_item(Item = item)
        except Exception as error:
            logger.error(f"put_item error: {get_exception_str(error)}")
            return {}


    def get_item(self, key_column, value):
        try:
            data = self.__table.query(KeyConditionExpression=Key(key_column).eq((value)))
            return (data['Items'])
        except Exception as error:
            logger.error(f"Query error: {get_exception_str(error)}")
            return []

    def get_all(self, limit,  last_evaluated_key):
        logger.info("Retrieving all items")
        query_params = {"Limit": limit}
        if last_evaluated_key:
            query_params["ExclusiveStartKey"] = last_evaluated_key
        try:
            return self.__table.scan(**query_params)
        except Exception as error:
            logger.error(f"Query error: {get_exception_str(error)}")
            return []  

    # def get_item_by_index(self, key_column, value, index_name):
    #     query_kwargs = {
    #         'KeyConditionExpression': Key(key_column).eq(value),
    #         'IndexName': index_name
    #     }

    #     try:
    #         data = self.__table.query(**query_kwargs)
    #         return (data['Items'])
    #     except Exception as error:
    #         logger.error(f"Query error: {get_exception_str(error)}")
    #         return []


    def get_item_by_index(self, key_column, value, index_name, **kwargs):
        filter_expression = kwargs.get("filter_expression", {})
        result_items = []

        query_kwargs = {
            'KeyConditionExpression': Key(key_column).eq(value),
            'IndexName': index_name
        }

        if filter_expression:
            is_valid_filter_expression = True if self.__is_valid_filter_expression(filter_expression) else False
            if is_valid_filter_expression:
                query_kwargs["FilterExpression"] = self.__get_constructed_filter_expresion(filter_expression)

        while True: 
            try:
                data = self.__table.query(**query_kwargs)
                result_items.extend(data['Items'])
                
                if 'LastEvaluatedKey' in data:
                    query_kwargs['ExclusiveStartKey'] = data['LastEvaluatedKey']
                else:
                    break
            except Exception as error:
                logger.error(f"Query error: {get_exception_str(error)}")
                return result_items
        
        return result_items


    def __is_valid_filter_expression(self, filter_expression):
        if not isinstance(filter_expression, dict):
            logger.info(f"filter_expression passed is not a dict.")
            return False     

        attribute = filter_expression.get("attribute", "")
        condition = filter_expression.get("condition", "").lower()
        value = filter_expression.get("value", "")

        if not attribute or not condition or not value:
            logger.info("Empty required params")
            return False

        if condition not in ["eq", "gt", "lt"]:
            logger.info("Invalid condition")
            return False

        return True


    def __get_constructed_filter_expresion(self, filter_expression):
        attribute = filter_expression.get("attribute", "")
        condition = filter_expression.get("condition", "").lower()
        value = filter_expression.get("value", "")

        if condition == "eq":
            return Attr(attribute).eq(value)
        elif condition == "lt":
            return Attr(attribute).lt(value)
        elif condition == "gt":
            return Attr(attribute).gt(value)

    
    def get_item_consistently(self, key_column, value):
        data = self.__table.query(KeyConditionExpression = Key(key_column).eq((value)), ConsistentRead = True)
        return (data['Items'])


    def get_item_with_sort(self, pk, pk_value, sk, sk_value):
        data = self.__table.query(KeyConditionExpression = Key(pk).eq(pk_value) & Key(sk).eq(sk_value))
        return (data['Items'])


    def delete_item(self, key_object={}):
        return self.__table.delete_item(Key = key_object)


    def delete_item_attribute(self, key_name, key_value, column_name):
        key = {}
        key[key_name] = key_value
        update_expression = "remove " + str(column_name)

        return self.__table.update_item(Key = key, UpdateExpression = update_expression)


    def update_item(self, key_name, key_value, items={}):
        key = {}
        key[key_name] = key_value
        update_expression = "set "
        expression_attribute_names = {}
        expression_attribute_values = {}

        for k, v in items.items():
            update_expression = update_expression + f"#{str(k)} " + f"= :{str(k)}, "
            expression_attribute_names[f"#{str(k)}"] = k
            expression_attribute_values[f":{str(k)}"] = v

        return self.__table.update_item(
            Key = key,
            UpdateExpression = update_expression.strip().strip(","),
            ExpressionAttributeNames = expression_attribute_names,
            ExpressionAttributeValues =  expression_attribute_values          
        )


    def update_item_if_primary_key_exist(self, key_name, key_value, items={}):
        key = {}
        key[key_name] = key_value
        update_expression = "set "
        expression_attribute_names = {}
        expression_attribute_values = {}

        for k, v in items.items():
            update_expression = update_expression + f"#{str(k)} " + f"= :{str(k)}, "
            expression_attribute_names[f"#{str(k)}"] = k
            expression_attribute_values[f":{str(k)}"] = v
            
        expression_attribute_values[f":{str(key_name)}"] = key_value
        
        try:
            return self.__table.update_item(
                Key = key,
                UpdateExpression = update_expression.strip().strip(","),
                ConditionExpression= f'{key_name} = :{key_name}',
                ExpressionAttributeNames = expression_attribute_names,
                ExpressionAttributeValues =  expression_attribute_values 
            )
        except self.__client.exceptions.ConditionalCheckFailedException:
            logger.info(f"Can't update item since main data is missing")
            return
        except Exception as error:
            logger.info(f"Update Item Error (if primary key exist): {get_exception_str(error)}")
            return


    def update_map(self, key_name, key_value, map_name, items = {}):
        key = {}
        key[key_name] = key_value
        update_expression = "set "
        expression_attribute_names = {f"#{str(map_name)}": str(map_name) }
        expression_attribute_values = {}

        for k, v in items.items():
            update_expression = update_expression + f"#{str(map_name)}.#{str(k)} " + f"= :{str(k)}, "
            expression_attribute_names[f"#{str(k)}"] = k
            expression_attribute_values[f":{str(k)}"] = v

        return self.__table.update_item(
            Key = key,
            UpdateExpression = update_expression.strip().strip(","),
            ExpressionAttributeNames = expression_attribute_names,
            ExpressionAttributeValues =  expression_attribute_values          
        )
    
    
    def is_table_exists(self):
        try:
            self.__client.describe_table(TableName=self.__table_name)
        except self.__client.exceptions.ResourceNotFoundException:
            return False
        except Exception as error:
            raise Exception(error)
        
        return True


    def create_table(self, **params):
        args = {}
        args['TableName'] = self.__table_name
        args['KeySchema'] = params['KeySchema']
        args['AttributeDefinitions'] = params['AttributeDefinitions']
        args['BillingMode'] = params['BillingMode']
        args['Tags'] = params['Tags'] if 'Tags' in params.keys() else project_fbgie_tags

        if 'GlobalSecondaryIndexes' in params.keys():
            args['GlobalSecondaryIndexes'] = params['GlobalSecondaryIndexes']
        
        try:
            self.__client.create_table(**args)
            waiter = self.__client.get_waiter('table_exists')
            waiter.wait(TableName = self.__table_name)
        except Exception as error:
            logger.info(f"Create table parameter: {args}")
            raise Exception(error)

    
    def delete_table(self):
        try:
            self.__client.delete_table(TableName = self.__table_name)
            waiter = self.__client.get_waiter('table_not_exists')
            waiter.wait(TableName = self.__table_name, WaiterConfig = self.__WAITER_CONFIG)
        except Exception as error:
            raise Exception(error)


    def put_batch_items(self, items={}, overwrite_pk=None, overwrite_sk=None):
        overwrite_keys = []
        if overwrite_pk:
            overwrite_keys.append(overwrite_pk)

        if overwrite_sk:
            overwrite_keys.append(overwrite_sk)

        try:
            with self.__table.batch_writer(overwrite_by_pkeys = overwrite_keys) as writer:
                for item in items:
                    writer.put_item(Item = item)
            logger.info(f"Successfully loaded data into table {self.__table_name}")
        except Exception as error:
            raise Exception(error)
