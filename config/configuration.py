env_lex = 'pd'
env_imrs = 'prd'
prd_toggle = True

dev_preprod_toggle = False

report_env = 'prd'

SS_IMAGE_URL = "https://image.ibb.co/izEr6y/gietemplate.jpg"
MYBUSINESS_SS_IMAGE_URL = "https://i.imgur.com/lgKV1ig.png"
THEA_SS_IMAGE_URL = "https://i.imgur.com/cuhp8vl.jpg"
TIMEZONE_PH = 'Asia/Manila'

GLOBAL_RETRY_THRESHOLD = 3

# S3
BUCKET_NAME = "lexs3pd01"
BATCH_FILE = "batch-updateLambda-globeOneToken.txt"
BATCH_ANONYMOUS_TOKEN_FILE = "batch-updateLambda-globeOneAnonymousToken.txt"
BCP_BATCH_FILE = "batch-updateLambda-bcp.txt"

#Personas
GIE_OF_GLOBE_TELECOM_PERSONA = "328935549320659"
GAH_OF_GLOBE_TELECOM_PERSONA = "418473339778673"
MYBUSINESS_OF_GLOBE_TELECOM_PERSONA = "720640156056743"
TIMMY_OF_TM_TAMBAYAN_PERSONA = "325946596285107"

# Facebook
GIE_OF_GLOBE_PERSONA = "455678601806204"

#PRIMARY_APP_ID = "1538844096254112" - dev
PRIMARY_APP_ID = "405127182864831"
SECONDARY_APP_ID = "678535392161606"
CONNECT_CHAT_APP_ID = "663758912092462"
LIVE_PERSON_APP_ID = "690022217842607"
GAH_APP_ID ='1284332918351398'
# EE_APP_ID = "230103212295439" - Lex WP 2 staging
EE_APP_ID = "891579108428668"

#GT_PAGE_ID = "863978400617100" - dev
GT_PAGE_ID = "30433734747"
MYBUSINESS_PAGE_ID = "98531356317"
THEA_PAGE_ID = "1395480467129397"
TM_PAGE_ID = "479337600141"
# EE_PAGE_ID = "111265681301726" - lex WP 2 staging
EE_PAGE_ID = "106583065110528"
GAH_PAGE_ID = "330276027750236"

GT_PAGE_NAME = "Globe Telecom"
MYBUSINESS_PAGE_NAME = "Globe Business"
GAH_PAGE_NAME = "Globe At Home"
THEA_PAGE_NAME = "Thea of Globe Platinum"
TM_PAGE_NAME = "TM Tambayan"
EE_PAGE_NAME = "Ally"

GLOBE_PAGE_ID = "30433734747"

# Socio
SOCIO_PROFILE_ID_GT = "25174"
SOCIO_PROFILE_ID_MB = "25174"
SOCIO_PROFILE_ID_TP = "25174"
SOCIO_PROFILE_ID_TM = "25174"
SOCIO_PROFILE_ID_GH = "25174"
SOCIO_ORG_ID = "1448"

# Regions
SGP_REGION = "ap-southeast-1"
SYD_REGION = "ap-southeast-2"
REGION = "us-west-2"
REGION_DB = "https://dynamodb.us-west-2.amazonaws.com"

# Tables
DEV_DB = "lex-prd-dev"
MYBUSINESS_DEV_DB = "lex-mybusiness-prd"
THEA_DEV_DB = "lex-platinum-prd"
TM_DEV_DB = "lex-tm-prd"
CMS_DEV_DB = "lex-prd-cms"
CMS_ENDSTATE_DB = 'lex-prd-cms-endstate'
CMS_NIA_DB = "lex-prd-cms-nia"
COUNTERS_DB = "lex-prd-counters"

#whitelist tables
SHOP_VOUCHERS_DB = 'lex-prd-shopVouchers'
BIRTHDAY_TREATS_REDEEMED_DB = 'lex-prd-birthdayRedeemed'
BIRTHDAY_TREATS_WHITELIST_DB = 'lex-prd-birthdayWhitelist'
GCASH_PLATINUM_DB = 'ncd-fbgie-pd-gcashPlatinum'


# dictionaries for mapping resources
ravenOTPDictionary = {
    MYBUSINESS_PAGE_ID: "22881",
    GT_PAGE_ID: "22881",
    THEA_PAGE_ID: "47481",
    TM_PAGE_ID: "22881",
    GAH_PAGE_ID: "22881"
}

pageDictionary = {
    MYBUSINESS_PAGE_ID: MYBUSINESS_PAGE_NAME,
    GT_PAGE_ID: GT_PAGE_NAME,
    THEA_PAGE_ID: THEA_PAGE_NAME,
    TM_PAGE_ID: TM_PAGE_NAME,
    EE_PAGE_ID: EE_PAGE_NAME,
    GAH_PAGE_ID: GAH_PAGE_NAME
}

databaseDictionary = {
    MYBUSINESS_PAGE_ID: MYBUSINESS_DEV_DB,
    GT_PAGE_ID: DEV_DB,
    THEA_PAGE_ID: THEA_DEV_DB,
    TM_PAGE_ID: TM_DEV_DB
}

keyDictionary = {
    # MYBUSINESS_PAGE_ID: 'EAAFwdgXS0b8BACdQ5AvhwQv4iqxzpZA6z35mcaeWUrJDayv0f9wQI06JIqwULUiFDr2HAToFwa6EgjhFuq5Lxmg9ga5P7ErgBd2vzJn0UtYM4xiTyjcPBJX2xizgcvgN291H3hCLDufCjT5ZC1uzuLMGCESiV8kyGXbf2mkwxZBtzdX3hoxOWDkUBVjjyEZD',
    # GT_PAGE_ID: 'EAAFwdgXS0b8BADBRaLZBLPiXFr9qDLFscfAXn2bHYTE8KzAJm5zTND6MZBtTF8Lzh2MrD1MsReLJy13Rhsq54QrLrBNrw45rUPEPEKMYZAaK93O349lRzi6XrTYhZCM8h4gbe5t1cWSTZBlCg8aG1OzXQ4uqPokEm9JPBokSpPKZCUdhHP5OkfRZCy4dIOS1ysZD',
    # THEA_PAGE_ID: 'EAAFwdgXS0b8BAAAKXBZCWXDVZCsiUmviVYSoYx4Y9Sc3hrOrtqf0rKMQ3SeTB7reEio5ZCJZBMwaz8ZBVg3qrZAZAzZA57zc5F4YoB6nQ6hmw8Fa1lcvDAqI58GAhn9MsXVg8hwbZBzITTImWBfsk36PDKz1w70YYVbBOZCDTTJqZCs4gwL0Qej6THvJZAwywWux484FzmPyBZBKgTAZDZD',
    # TM_PAGE_ID: 'EAAFwdgXS0b8BAKZAHfyw8AIxMzVbQvUfAcbCD0AjgRCIQJJoZBmGmlEO134uOFEyTeJ4OS2V6iR5dne6Q0ZAxC86pLO5fcHGBh7u46Xk4urms4TZBo1jhtDgwyBZAxU5E46cYaztTs1scP3J8f82OQlkApax6cprNj0AfvIDmDr13FF7p2ZCrBQngEdfZCORYoZD',
    EE_PAGE_ID: 'DQVJ2QmJ3ZAGdVNXhwVWU3LW5NSGdSdDhiNklsX0Q2Y3ZAIa2IxZAl8yR2p3V0VocEpsZAFFJeHJBNEQxc0xpYkJHM1hvT2ZAhWnRweFIwb0luS1o3RWE4OW5pcWV3VUd1blpPSkJGbVZA2UGFMS0JSZA3BzZA216RUdlQjNGSkFubXBoMFlManRoS1l0UG44aGN6LTdaeXFSN3RRUFdzRFNTeC1XZAkk4WmFfbVo2eVdYQWxWN0J2OVdNTlRod2lXbm9BeC0yQVhJZAjhR',
    # EE_PAGE_ID: 'DQVJzVTE1TV9seEtId2N0cXdXUWU4QU1jRktlQkM4Q2F4VjJMdXVDTDVLSDZApdzNwUGxxVThnczRISUVYanhieDFkbHJxWHhYTWxQUUx5d2MyZAFFwRF96eWNzend5UTdnRG5BSDhMVE9TR3NiYkg2TXRpcG1pRkRqajdzaTd3TFlSNkZApZAGRuWnNDc0ZAqTnZAzYVpGckpVak5YaUxtN2RVcHJfQjlyUFNocllyMzd1Q3hlakRsMzlkX21SaFRUU2JkZA0Y5QThB' - Lex WP 2 staging
    # GAH_PAGE_ID: 'EAAFwdgXS0b8BAAZAsUfWbRGtkSTYMZBQyW2c4YCjS3ISTn9o4HOuAj86Sc3JZAHLFZBBJEmi6v66of4h7Y3T0JY47qeFQustngvipxi3HwJMRBZAcqpPZBQJWhX4xjCBBBHJLkZA2i1ZCjlFgojnHAy1AsEsbgZBxXZAeuHeettTpFfQaZCY1oZAq6AKbAlAtJvSB7TNiuxJF07i0gZDZD',
    
    # NEW TOKENS
    GT_PAGE_ID: 'EAAFwdgXS0b8BAFA9CqVP3QDJpELgPuSSvtKaWWdCZACCvabhdfEDEAltH6JTgGeR4QG4tIov1BUhHjtvjYZA6ccFbXW4YilcHFo9YA3OslRu32nZAyKdRGOEIrmOiNASWRgTPWsHU7RamK1fnDjX9hK2q5HToDrJfuhaUxUmCDNfEQNR7pP',
    MYBUSINESS_PAGE_ID: 'EAAFwdgXS0b8BAFgSvOvpcRSqBr0yTxfZBSUlwGciQfTZAr1ZB4uRZBs7VbH3VZADpCkCAyc9HAVRqU7lPcz4cDINjzEyCSGlAJb0M7m4VtJUtZArUCbI5LyDKCXb3CvL74wHJUyoHpN67gIZCWQ13GEE1EeCZCXYSFdVfIgafZAG5RbDEQsXl9n2P',
    THEA_PAGE_ID: 'EAAFwdgXS0b8BANZCg2NcDWRmSj1dpePH4aVmyED43Dj3lcQqD20LJSzl4nZBTM69oP0uAyc65WMeSC8g6VIAt4gvjxTdByX1iYc0DPxx18l7u8oGDTiYrvFrO5H4WY0FwE5cAOJpheutLseyWPsivvJMrKpApC9IxpWaM4yxMaILIFyefJ',
    GAH_PAGE_ID: 'EAAFwdgXS0b8BAObZAxNazHgOtnh1n7Dyad2hmZCYzDWqxfJ3CAFFQ0fCBmJYmZAJltTuDZBUJshfQbnm88VB0zc1yQtPmFiRow4FRv76FtfnpeksbXFQMfQGOcOoGx9vlYXt6Xsp7tl5ADWvuk7okuzkVvTmPTZAI6ZCk6WTySpETJnRcwYL4U',
    TM_PAGE_ID: 'EAAFwdgXS0b8BAG9ZAaMMIyqcw0MAuDSfz14hdFXCAS5C2k3ZC37oZBtn6OqeBUW0JXhCvkGwyHTeodP3KIpZCAwXvvx96R5ghHS6f6WguIzj6ACAX7ZAfEeENeN8ByFm91SYMwTZA1Pr4VjN403XVRGUUYj4djmXumNnZAAU8zIzFM7JIXDmuFl'
}

SNS = "arn:aws:sns:ap-southeast-1:073504361408:lex-errors-prd"
SNS_SOIC = "arn:aws:sns:ap-southeast-1:073504361408:lex-soic-prd"
SNS_VOLUME_REPORT = "arn:aws:sns:ap-southeast-1:073504361408:lex-volume-reports-prd"

#attachementIDs (IMAGES)
CHICAGO_OPENING_IMAGE = 320969279207484
CHICAGO_COOKIE_GCASH_IMAGE = 725593931317453
CHICAGO_JCO_GCASH_IMAGE = 728622751230958
CHICAGO_COCO_GCASH_IMAGE = 580482579323737

GO_HEALTH_INTRO_IMAGE_THEA = 403289394015952
GO_HEALTH_INTRO_IMAGE_GT = 728664081409950


socioBasket = {
    MYBUSINESS_PAGE_ID: {
        "main": "0200",
        "postpaid" : "0201",
        "prepaid" : "0202",
        "broadband" : "0203",
        "thea_postpaid" : "0204",

        "network_bb_onsite_chat": "9031",
        "network_bb_onsite_call": "9027"
    },
    GT_PAGE_ID: {
        "main": "0100",
        "postpaid" : "0101",
        "prepaid" : "0102",
        "broadband" : "0103",
        "thea_postpaid" : "0104",
        "amax" : "0105",
        "hpw" : "0106",
        "howTos" : "0108",
        "business_sg_postpaid" : "0109",
        "business_sg_broadband" : "0110",
		"broadband_onsite_chat": "210120",
        "broadband_onsite_call": "011",


        # IBR - Intent Based Routing
        "pp_recon_beyond_sla": "310110",
        "bb_recon_beyond_sla": "310115",
        "bb_upsell": "80012",
        "bb_felicity": "80022",
        "bb_cpl": "9033",

        "change_plan_call": "10308",
        "change_plan_chat": "10313",        

        "followup_concern_post": "520110",
        "followup_concern_pre": "520111",
        "followup_concern_tm": "520111",
        "followup_concern_bb": "520112",
        "followup_concern_hpw": "520113",
        "followup_concern_sg": "520114",
        
        "techinician_vist_bb": "530110",
        "techinician_vist_sg": "520115",

        "network_concern_roaming_post": "210114",	
        "network_concern_roaming_pre": "210115",	
        "network_concern_roaming_tm": "210115",

        "report_lost_phone_post": "620110",	
        "report_lost_phone_pre": "620111",	
        "report_lost_phone_tm": "620111",	
        "report_lost_phone_sg": "620112",
		
		"fb_vip": "010",
        "senior_post": "0306",
        "senior_bb": "0310",
        "bb_onboarding":"0112",

        "prepaid_fiber": "80031",
        
        #Facebook Public CLP
        "public_CLP_bb": "00511",
        "public_CLP_post": "100911",
        "public_CLP_pre": "214671",

        "network_bb_onsite_chat": "9029",
        "network_bb_onsite_call": "9025"
    },
    THEA_PAGE_ID: {
        "main": "0300",
        "postpaid" : "0301",
        "prepaid" : "0302",
        "broadband" : "0303",
        "thea_postpaid" : "0304",
        "thea_aspire": "0305"       
    },
    TM_PAGE_ID: {
        "main": "7001",
        "postpaid" : "7002",
        "prepaid" : "7003",
        "broadband" : "7004",
        "thea_postpaid" : "7005",
        "amax" : "7006",
        "hpw" : "7007",
        "howTos" : "7008",
        "business_sg_postpaid" : "7009",
        "business_sg_broadband" : "7010",
        "broadband_onsite_chat": "7019",
        "broadband_onsite_call": "7018",

        # IBR - Intent Based Routing
        "pp_recon_beyond_sla": "8019",
        "bb_recon_beyond_sla": "8018",
        "bb_upsell": "80013",
        "bb_felicity": "80023",
        "bb_cpl": "9035",

        "change_plan_call": "10310",
        "change_plan_chat": "10315",  

        "followup_concern_post": "7011",
        "followup_concern_pre": "7012",
        "followup_concern_tm": "7012",
        "followup_concern_bb": "7013",
        "followup_concern_hpw": "7014",
        "followup_concern_sg": "7015",
        
        "techinician_vist_bb": "7016",
        "techinician_vist_sg": "7017",

        "network_concern_roaming_post": "210114998",	
        "network_concern_roaming_pre": "210115998",	
        "network_concern_roaming_tm": "210115998",

        "report_lost_phone_post": "620110998",	
        "report_lost_phone_pre": "620111998",	
        "report_lost_phone_tm": "620111998",	
        "report_lost_phone_sg": "620112998",
		
		"fb_vip": "014",
        "senior_post": "0308",
        "senior_bb": "0312",
        "bb_onboarding":"0116",

        "prepaid_fiber": "80029",
        
        #Facebook Public CLP
        "public_CLP_bb": "00311",
        "public_CLP_post": "100711",
        "public_CLP_pre": "212679",

        "network_bb_onsite_chat": "9032",
        "network_bb_onsite_call": "9028"
    },
    GAH_PAGE_ID: {	
        "main": "320011",
        "postpaid" : "320012",
        "prepaid" : "320013",
        "broadband" : "320014",
        "thea_postpaid" : "320015",
        "amax" : "320016",
        "hpw" : "320017",
        "howTos" : "320018",
        "business_sg_postpaid" : "320019",
        "business_sg_broadband" : "320020",
        "broadband_onsite_chat": "320029",
        "broadband_onsite_call": "320028",

        # IBR - Intent Based Routing
        "pp_recon_beyond_sla": "9038",
        "bb_recon_beyond_sla": "9037",
        "bb_upsell": "8001",
        "bb_felicity": "8002",
        "bb_cpl": "9034",
        
        "change_plan_call": "10306",
        "change_plan_chat": "10311",

        "followup_concern_post": "320021",
        "followup_concern_pre": "320022",
        "followup_concern_tm": "320022",
        "followup_concern_bb": "320023",
        "followup_concern_hpw": "320024",
        "followup_concern_sg": "320025",
        
        "techinician_vist_bb": "320026",
        "techinician_vist_sg": "320027",

        "network_concern_roaming_post": "320030",	
        "network_concern_roaming_pre": "320031",	
        "network_concern_roaming_tm": "320031",

        "report_lost_phone_post": "320032",	
        "report_lost_phone_pre": "320033",	
        "report_lost_phone_tm": "320033",	
        "report_lost_phone_sg": "320034",
		
		"fb_vip": "013",
        "senior_post": "0307",
        "senior_bb": "0311",
        "bb_onboarding":"0114",

        "prepaid_fiber": "80028",
        
        #Facebook Public CLP
        "public_CLP_bb": "00211",
        "public_CLP_post": "100611",
        "public_CLP_pre": "211678",

        "network_bb_onsite_chat": "9030",
        "network_bb_onsite_call": "9026"
    },
    MYBUSINESS_PAGE_ID: {	
        "main": "70013",
        "postpaid" : "70023",
        "prepaid" : "70033",
        "broadband" : "70043",
        "thea_postpaid" : "70053",
        "amax" : "70063",
        "hpw" : "70073",
        "howTos" : "70083",
        "business_sg_postpaid" : "70093",
        "business_sg_broadband" : "70103",
        "broadband_onsite_chat": "2101203",
        "broadband_onsite_call": "0113",

        # IBR - Intent Based Routing
        "pp_recon_beyond_sla": "7041",
        "bb_recon_beyond_sla": "7040",
        "bb_upsell": "80017",
        "bb_felicity": "80027",
        "bb_cpl": "9036",

        "change_plan_call": "10307",
        "change_plan_chat": "10312",

        "followup_concern_post": "70113",
        "followup_concern_pre": "70123",
        "followup_concern_tm": "70123",
        "followup_concern_bb": "70133",
        "followup_concern_hpw": "70143",
        "followup_concern_sg": "70153",
        
        "techinician_vist_bb": "70163",
        "techinician_vist_sg": "70173",

        "network_concern_roaming_post": "2101149983",	
        "network_concern_roaming_pre": "2101159983",	
        "network_concern_roaming_tm": "2101159983",

        "report_lost_phone_post": "6201109983",	
        "report_lost_phone_pre": "6201119983",	
        "report_lost_phone_tm": "6201119983",	
        "report_lost_phone_sg": "6201129983",
		
		"fb_vip": "015",
        "senior_post": "0309",
        "senior_bb": "0313",
        "bb_onboarding":"0115",

        "prepaid_fiber": "80030",
        
        #Facebook Public CLP
        "public_CLP_bb": "00411",
        "public_CLP_post": "100811",
        "public_CLP_pre": "213670",

        "network_bb_onsite_chat": "9031",
        "network_bb_onsite_call": "9027"
    }
}

#dummy intents
wb_intent_mapping_dict = {
    GAH_PAGE_ID: {
        "BBABSI": "9001",
        "BBTMD" : "9005",
        "BBTP": "9009",
        "HPWABSI": "9013",
        "HPWTMD" : "9017",
        "HPWTP": "9021",
        "PPABSI": "7020",
        "PPTMD": "7024",
        "PPTP": "7028",
        "PRTMD": "7032",
        "PRTP": "7036"
    },
    TM_PAGE_ID: {
        "BBABSI": "9002",
        "BBTMD" : "9006",
        "BBTP": "9010",
        "HPWABSI": "9014",
        "HPWTMD" : "9018",
        "HPWTP": "9022",
        "PPABSI": "7021",
        "PPTMD": "7025",
        "PPTP": "7029",
        "PRTMD": "7033",
        "PRTP": "7037"
    },
    MYBUSINESS_PAGE_ID: {
        "BBABSI": "9003",
        "BBTMD" : "9007",
        "BBTP": "9011",
        "HPWABSI": "9015",
        "HPWTMD" : "9019",
        "HPWTP": "9023",
        "PPABSI": "7022",
        "PPTMD": "7026",
        "PPTP": "7030",
        "PRTMD": "7034",
        "PRTP": "7038"
    },
    GT_PAGE_ID: {
        "BBABSI": "9004",
        "BBTMD" : "9008",
        "BBTP": "9012",
        "HPWABSI": "9016",
        "HPWTMD" : "9020",
        "HPWTP": "9024",
        "PPABSI": "7023",
        "PPTMD": "7027",
        "PPTP": "7031",
        "PRTMD": "7035",
        "PRTP": "7039"
    }
}

VOC_CLIENT_ID = "lex_webfeed_oauth"
VOC_CLIENT_PASSWORD = "8ba2947c62985788853c7c389e70cce2"

REPORT_LOG_GROUP_NAME = 'lex-prd-reportLogGroup'
CHECK_APPLICATION_REPORT_LOG_NAME="lex-prd-check-application-report-logs"

CHECK_APPLICATION_RECIPIENTS = "care@globe.com.ph"

LEX_EDO_INGESTION_TABLE = 'lex-prd-kinesis-edo'


EDO_ROLE_ARN = "arn:aws:iam::638307268311:role/edo-prod-lex-kinesis-producer-role"
STREAM_NAME = "kala-txn-raw-lex"


# ***************************************************************************************************************************
# ********************************************* NIAS 2.0 - Start ************************************************************
# ***************************************************************************************************************************

REGION_OREGON = "us-west-2"
REGION_NORTHERN_VIRGINIA = "us-east-1"
REGION_SYDNEY = "ap-southeast-2"
REGION_SINGAPORE = "ap-southeast-1"

DDB_GT_MAIN = "ncd-fbgie-pd-gie-main"
DDB_GT_HISTORY = "ncd-fbgie-pd-gie-history"
DDB_GT_SESSION = "ncd-fbgie-pd-gie-session"

DDB_EE_MAIN = "ncd-fbgie-pd-ee-main"
DDB_EE_HISTORY = "ncd-fbgie-pd-ee-history"
DDB_EE_SESSION = "ncd-fbgie-pd-ee-session"

DDB_THEA_MAIN = "ncd-fbgie-pd-thea-main"
DDB_THEA_HISTORY = "ncd-fbgie-pd-thea-history"
DDB_THEA_SESSION = "ncd-fbgie-pd-thea-session"

DDB_TM_MAIN = "ncd-fbgie-pd-tm-main"
DDB_TM_HISTORY = "ncd-fbgie-pd-tm-history"
DDB_TM_SESSION = "ncd-fbgie-pd-tm-session"

DDB_MYBIZ_MAIN = "ncd-fbgie-pd-myBiz-main"	
DDB_MYBIZ_HISTORY = "ncd-fbgie-pd-myBiz-history"	
DDB_MYBIZ_SESSION = "ncd-fbgie-pd-myBiz-session"

DDB_GAH_MAIN = "ncd-fbgie-pd-gah-main"	
DDB_GAH_HISTORY = "ncd-fbgie-pd-gah-history"	
DDB_GAH_SESSION = "ncd-fbgie-pd-gah-session"

CMS_NIA_DB = "ncd-fbgie-pd-cms-cardsNia"
CMS_NIA_SPIEL_DB = "ncd-fbgie-pd-cms-spiel"
DDB_EMPLOYEE_CARE_WHITELIST = "ncd-fbgie-pd-employeeCareWhitelist"
DDB_PENDING_STUCK_ORDER_WHITELIST ="ncd-fbgie-pd-stuckPendingOrderWhitelist"
DDB_PLATINUM_WHITELIST = "RCX-PlatinumWhitelist"
DDB_HAMILTON_WHITELIST = "ncd-fbgie-pd-hamiltonWhitelist"
DDB_GCASH_PLATINUM_WHITELIST = "ncd-fbgie-pd-gcashPlatinumWhitelist"
DDB_UPSELL_WHITELIST = "RCX-BBUpsellWhitelist"
DDB_SERVICE_RECOVERY_WHITELIST = "RCX-ServiceRecoveryWhitelist"
DDB_BB_OUTAGE_WHITELIST = "ncd-cnect-pd-bbOutageWhitelist"
DDB_CASE_CREATED = "RCX-caseCreated"

DDB_CUSTOMER_JOURNEY = "ncd-fbgie-pd-customerJourney"
DDB_FACEBOOK_USER_IDENTITY = "ncd-fbgie-pd-facebookUserIdentity"
DDB_LOGS = "ncd-fbgie-pd-logs"
DDB_MONITORING = "ncd-fbgie-pd-monitoring"
DDB_TROUBLESHOOT_LOGS = "ncd-fbgie-pd-troubleshootLog"
DDB_CHECK_OPEN_CASE_REPORT = "ncd-fbgie-pd-checkOpenCaseReport"
DDB_RECURRING_NOTIF_TABLE = "ncd-fbgie-pd-notif-message-token"
DDB_SUBSCRIBER_CROSS_CHANNEL_MATCHING = "ncd-fbgie-pd-subscriberCrossChannelMatching"
DDB_GLOBE_ONE_DETAILS = "ncd-fbgie-pd-globeOneDetails"
DDB_PERCENTAGE = "ncd-fbgie-pd-percentage"
DDB_PLATINUM_UPSELL_WHITELIST = "ncd-cnect-pd-platinumUpsellWhitelist"
DDB_PLATINUM_UPSELL_REPORT = "ncd-cnect-pd-platinumUpsellReport"
DDB_PLATINUM_FREE_THEA_WHITELIST = "ncd-cnect-pd-freeTheaWhitelist"
DDB_CJ_REPEAT_CUSTOMER = "ncd-cnect-pd-repeatCustomer"
DDB_BB_FACILITY_MIGRATION_WHITELIST = "ncd-cnect-pd-BBFacilityMigrationWhitelist"
DDB_UNLOCK_DEVICE_WHITELIST = "ncd-cnect-pd-unlockDeviceWhitelist"
DDB_GO_FAM_WHITELIST = "ncd-fbgie-pd-goFamWhitelist"
DDB_RAKET_WHITELIST = "ncd-fbgie-pd-raketWhitelist"
DDB_SWITCHES = "ncd-fbgie-prd-switches"
DDB_COEX_WHITELIST = "ncd-fbgie-pd-coexWhitelist"
DDB_FACEBOOK_PUBLIC = "ncd-fbgie-pd-facebookPublic"
DDB_LPR_FIRST_TIMER_WHITELIST = "ncd-cnect-pd-lprFirstTimerWhitelist"
DDB_PROACTIVE_RENEWAL_WHITELIST = "ncd-cnect-pd-proActiveRenewalWhitelist"

TIME_SESSION_END = 10 # minutes
OTP_EXPIRY_LIMIT = 300 # seconds

CASE_CREATE_SMS_MESSAGE_ID = "50761"
CHANGE_PLAN_CREATE_CASE_SMS_MESSAGE_ID = "135773"
TERMINATION_CREATE_CASE_SMS_MESSAGE_ID = "135793"
CONFIRM_BOOKING_SMS_MESSAGE_ID = 131453
FAILED_BOOKING_SMS_MESSAGE_ID = 131473

SOCIO_TOKEN = "9Aw10BbD77jTmNpDjpqQz1oJN_o"
LIVE_PERSON_CLIENT_ID = "bb3dfe9f-ffc8-47b9-9096-16905fd8162c"
LIVE_PERSON_CLIENT_SECRET = "v1cgq5t7fek1627fpand7l2vjf"
LIVE_PERSON_SECRET_NAME = "scrt-lex-pd-live-person"


PASS_THREAD_METADATA_LIVE_PERSON = "B4f1PiySEEKt0tQvJ7UNzQ=="
PASS_THREAD_METADATA_SOCIO = "QY3HW7TBTAKE65OZGLA2ES40"
PASS_THREAD_METADATA_SOCIO_OLD = "Passing control now"
PASS_THREAD_METADATA_IDLE_MODE = "new message"
PASS_THREAD_METADATA_BOT_INVALID_THREAD_HANDOVER = "INVALID_THREAD_HANDOVER"



# *************************************
# ********** SWITCHES *****************
# *************************************
SWITCH_FB_PAGES_SINGLE_IDENTITY = "ON"
SWITCH_FB_PAGES_SINGLE_IDENTITY_PAGES = {
    GT_PAGE_ID: "ON",
    THEA_PAGE_ID: "OFF",
    GAH_PAGE_ID: "ON",
    TM_PAGE_ID: "ON",
    MYBUSINESS_PAGE_ID: "ON"
}

SWITCH_MAINTENANCE = "OFF"
SWITCH_MAINTENANCE_PAGES = {
    GT_PAGE_ID: "OFF",
    THEA_PAGE_ID: "OFF",
    GAH_PAGE_ID: "OFF",
    TM_PAGE_ID: "OFF",
    MYBUSINESS_PAGE_ID: "OFF"
}

SWITCH_GFIBER ="ON"

SWITCH_THEA_CONNECT_CHAT = "OFF"
SWITCH_CUSTOMER_VERIFICATION = "ON"


MESSENGER_PAGE_URLS = {
    GT_PAGE_ID: "https://m.me/globeph",
    THEA_PAGE_ID: "https://m.me/TheaOfGlobePlatinum",
    GAH_PAGE_ID: "https://m.me/globeathome",
    MYBUSINESS_PAGE_ID: "https://m.me/globebusiness",
    TM_PAGE_ID: "https://m.me/TMtambayan"
}

CONNECT_CHAT_INTENT_QUEUE_IDS = {
    "fbm_default": "fbm_default", #"FBM_DEFAULT"
    "prepaid_fiber": "prepaid_fiber", #"FBM_DEFAULT" - placeholder
    "onsite_visit_chat": "onsite_visit_chat",
    "onsite_visit_call": "onsite_visit_call",
    "proactive_renewal": "proactive_renewal", 
    THEA_PAGE_ID: {
        "main": "thea_main_connect_chat",
        "broadband" : "thea_broadband_connect_chat",
        "thea_postpaid" : "thea_postpaid_connect_chat",
        "thea_aspire" : "thea_aspire_connect_chat"
    }
}

LIVE_PERSON_INTENT_IDS = {
    "followup-prepaid"              : "followup-prepaid",
    "network-roaming-prepaid"       : "network-roaming-prepaid",
    "prepaid-regular"               : "prepaid-regular",
    "postpaid-regular"              : "postpaid-regular",
    "broadband-regular"             : "broadband-regular",
    "hpw-regular"                   : "hpw-regular",
    "barring-prepaid"               : "barring-prepaid",
    "unlock-device-prepaid"         : "unlock-device-prepaid",
    "followup-postpaid"             : "followup-postpaid",
    "senior-postpaid"               : "senior-postpaid",
    "network-roaming-postpaid"      : "network-roaming-postpaid",
    "lost-phone-sim-postpaid"       : "lost-phone-sim-postpaid",
    "followup-broadband"            : "followup-broadband",
    "senior-broadband"              : "senior-broadband",
    "onboarding-broadband"          : "onboarding-broadband",
    "ofu-chat-broadband"            : "ofu-chat-broadband",
    "ofu-call-brandband"            : "ofu-call-brandband",
    "changeplan-broadband"          : "changeplan-broadband",
    "vip-user"                      : "vip-user",
    "clp-broadband"                 : "clp-broadband",
    "clp-postpaid"                  : "clp-postpaid",
    "clp-prepaid"                   : "clp-prepaid",
    "globe-fiber-prepaid"           : "globe-fiber-prepaid",
    "thea-postpaid"                 : "thea-postpaid",
    "thea-aspire"                   : "thea-aspire",
    "thea-broadband"                : "thea-broadband"
}

LIVE_PERSON_SKILL_INTENT_MAPPING_DICT = {
    "PPABSI"        : "postpaid-reg-absi",
    "PPTMD"         : "postpaid-reg-tmd",
    "PPTP"          : "postpaid-reg-tp",
    "PRTMD"         : "prepaid-reg-tmd",
    "PRTP"          : "prepaid-reg-tp",
    "BBABSI"        : "broadband-reg-absi",
    "BBTMD"         : "broadband-reg-tmd",
    "BBTP"          : "broadband-reg-tp",
    "HPWABSI"       : "hpw-reg-absi",
    "HPWTMD"        : "hpw-reg-tmd",
    "HPWTP"         : "hpw-reg-tp"
}


# HOOP
COEX_HOOP_START = "09:00:00"
COEX_HOOP_END = "18:00:00"

RECONNECTION_HOOP_START = "09:00:00"
RECONNECTION_HOOP_END = "18:00:00"

# ***************************************************************************************************************************
# ********************************************* NIAS 2.0 - End ************************************************************
# ***************************************************************************************************************************
