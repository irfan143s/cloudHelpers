CONNECT_LMB_REQUEST = {
    "Details": {
        "ContactData": {
            "Attributes": {
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

LEX_BOT_PAYLOAD = {
    "dialogAction": {
        "type": "Close",
        "fulfillmentState": "Fulfilled",
        "message":{
            "contentType": "PlainText",
            "content": "Default message"
        }
    }
}