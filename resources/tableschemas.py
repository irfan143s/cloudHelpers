from configuration import *

project_fbgie_tags = [
   {
      'Key':'Domain',
      'Value':'OMNI'
   },
   {
      'Key':'Project',
      'Value':'GIE:NIAS2.0'
   },
   {
      'Key':'Project Owner',
      'Value':'ELDRIDGE MYLES TAN'
   },
   {
      'Key':'Project Manager',
      'Value':'RAYMOND LIONG'
   },
   {
      'Key':'Platform Name',
      'Value':'FB CHATBOT FOR GLOBE'
   },
   {
      'Key':'Platform Owner',
      'Value':'XEL ABRAHAM PANLAQUI'
   },
   {
      'Key':'WBS Code or Cost Center for Charging',
      'Value':'OP2-I801'
   },
   {
      'Key':'Application Vendor',
      'Value':'AMDOCS'
   },
   {
      'Key':'Ready For Service Date',
      'Value':'7/13/2021'
   },
   {
      'Key':'System Alias',
      'Value':'FBGIE'
   }
]

employee_care_whitelist_schema = {
    'TableName': DDB_EMPLOYEE_CARE_WHITELIST,
    'AttributeDefinitions': [
        {
            'AttributeName': 'concernNo',
            'AttributeType': 'S'
        }
    ],
    'KeySchema': [
        {
            'AttributeName': 'concernNo',
            'KeyType': 'HASH'
        },
    ],
    'BillingMode': 'PAY_PER_REQUEST',
    'Tags': project_fbgie_tags
}

hamilton_whitelist_schema = {
    'TableName': DDB_HAMILTON_WHITELIST,
    'AttributeDefinitions': [
        {
            'AttributeName': 'concernNo',
            'AttributeType': 'S'
        }
    ],
    'KeySchema': [
        {
            'AttributeName': 'concernNo',
            'KeyType': 'HASH'
        },
    ],
    'BillingMode': 'PAY_PER_REQUEST',
    'Tags': project_fbgie_tags
}

gcash_platinum_whitelist_schema = {
    'TableName': DDB_GCASH_PLATINUM_WHITELIST,
    'AttributeDefinitions': [
        {
            'AttributeName': 'concernNo',
            'AttributeType': 'S'
        }
    ],
    'KeySchema': [
        {
            'AttributeName': 'concernNo',
            'KeyType': 'HASH'
        },
    ],
    'BillingMode': 'PAY_PER_REQUEST',
    'Tags': project_fbgie_tags
}

pending_stuck_order_whitelist_schema = {
    'TableName': DDB_PENDING_STUCK_ORDER_WHITELIST,
    'AttributeDefinitions': [
        {
            'AttributeName': 'serviceId',
            'AttributeType': 'S'
        }
    ],
    'KeySchema': [
        {
            'AttributeName': 'serviceId',
            'KeyType': 'HASH'
        },
    ],
    'BillingMode': 'PAY_PER_REQUEST',
    'Tags': project_fbgie_tags
}

go_fam_whitelist_schema = {
    'TableName': DDB_GO_FAM_WHITELIST,
    'AttributeDefinitions': [
        {
            'AttributeName': 'concernNo',
            'AttributeType': 'S'
        }
    ],
    'KeySchema': [
        {
            'AttributeName': 'concernNo',
            'KeyType': 'HASH'
        },
    ],
    'BillingMode': 'PAY_PER_REQUEST',
    'Tags': project_fbgie_tags
}

raket_whitelist_schema = {
    'TableName': DDB_RAKET_WHITELIST,
    'AttributeDefinitions': [
        {
            'AttributeName': 'concernNo',
            'AttributeType': 'S'
        }
    ],
    'KeySchema': [
        {
            'AttributeName': 'concernNo',
            'KeyType': 'HASH'
        },
    ],
    'BillingMode': 'PAY_PER_REQUEST',
    'Tags': project_fbgie_tags
}

coex_whitelist_schema = {
    'TableName': DDB_COEX_WHITELIST,
    'AttributeDefinitions': [
        {
            'AttributeName': 'accountNo',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'msisdn',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'recordId',
            'AttributeType': 'S'
        }
    ],
    'KeySchema': [
        {
            'AttributeName': 'recordId',
            'KeyType': 'HASH'
        },
    ],
    'BillingMode': 'PAY_PER_REQUEST',
    'GlobalSecondaryIndexes': [
        {
            'IndexName': "msisdn-index",
            'KeySchema': [
                { 'AttributeName': "msisdn", 'KeyType': "HASH" }
            ],
            'Projection': {
                'ProjectionType': "ALL"
            }
        },
        {
            'IndexName': "accountNo-index",
            'KeySchema': [
                { 'AttributeName': "accountNo", 'KeyType': "HASH" }
            ],
            'Projection': {
                'ProjectionType': "ALL"
            }
        }
    ],
    'Tags': project_fbgie_tags
}