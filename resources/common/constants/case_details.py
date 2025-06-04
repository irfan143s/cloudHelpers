import resources.constants as constants

case_details = {
    "recon-pymt-not-reflected-on-channel-globe": {
        constants.POSTPAID_LOB_NAME: {
            "title"     : "SNS_Reconnection Request",
            "queue"     : "CCM IVR RECON CSR PTI",
            "lvl1"      : "CXP-SELF-SERVICE",
            "lvl2"      : "RESUME",
            "lvl3"      : "REQUESTED VIA WEB",
            "lvl4"      : "N/A",
            "lvl5"      : "N/A",
            "reason"    : "reconnect my line",
            "notes"     : "n/a",
            "sla"       : "48 hours"
        },
        constants.BB_LOB_NAME: {
            "title"     : "FBMLEX_RESUME-GI",
            "queue"     : "CCM IVR RECON CSR PTI",
            "lvl1"      : "WIRELINE_WIRELINE",
            "lvl2"      : "WAO_OTHER ACCOUNT RELATED REQUESTS",
            "lvl3"      : "OTHERS",
            "lvl4"      : "OTHERS",
            "lvl5"      : "ENDORSED TO SUPPORT GROUP FOR HANDLING",
            "reason"    : "reconnect my line",
            "notes"     : "n/a",
            "sla"       : "48 hours"
        },
        "default": {}
    },
    "recon-pymt-not-reflected-on-channel-banks": {
        constants.POSTPAID_LOB_NAME: {
            "title"     : "SNS_Reconnection Request",
            "queue"     : "CCM IVR RECON CSR PTI",
            "lvl1"      : "CXP-SELF-SERVICE",
            "lvl2"      : "RESUME",
            "lvl3"      : "REQUESTED VIA WEB",
            "lvl4"      : "N/A",
            "lvl5"      : "N/A",
            "reason"    : "reconnect my line",
            "notes"     : "n/a",
            "sla"       : "48 hours"
        },
        constants.BB_LOB_NAME: {
            "title"     : "FBMLEX_RESUME-GI",
            "queue"     : "CCM IVR RECON CSR PTI",
            "lvl1"      : "WIRELINE_WIRELINE",
            "lvl2"      : "WAO_OTHER ACCOUNT RELATED REQUESTS",
            "lvl3"      : "OTHERS",
            "lvl4"      : "OTHERS",
            "lvl5"      : "ENDORSED TO SUPPORT GROUP FOR HANDLING",
            "reason"    : "reconnect my line",
            "notes"     : "n/a",
            "sla"       : "48 hours"
        },
        "default": {}
    },
    "recon-pymt-not-reflected-on-channel-others": {
        constants.POSTPAID_LOB_NAME: {
            "title"     : "SNS_Reconnection Request",
            "queue"     : "CCM IVR RECON CSR PTI",
            "lvl1"      : "CXP-SELF-SERVICE",
            "lvl2"      : "RESUME",
            "lvl3"      : "REQUESTED VIA WEB",
            "lvl4"      : "N/A",
            "lvl5"      : "N/A",
            "reason"    : "reconnect my line",
            "notes"     : "n/a",
            "sla"       : "48 hours"
        },
        constants.BB_LOB_NAME: {
            "title"     : "FBMLEX_RESUME-GI",
            "queue"     : "CCM IVR RECON CSR PTI",
            "lvl1"      : "WIRELINE_WIRELINE",
            "lvl2"      : "WAO_OTHER ACCOUNT RELATED REQUESTS",
            "lvl3"      : "OTHERS",
            "lvl4"      : "OTHERS",
            "lvl5"      : "ENDORSED TO SUPPORT GROUP FOR HANDLING",
            "reason"    : "reconnect my line",
            "notes"     : "n/a",
            "sla"       : "48 hours"
        },
        "default": {}
    },
    "recon-pymt-not-reflected": {
        constants.POSTPAID_LOB_NAME: {
            "title"     : "FBM MOBILE POSTPAID RECONNECTION REQUEST WITH UPP",
            "queue"     : "BCM Unposted Paymt-CONS",
            "lvl1"      : "GHP_GLOBE POSTPAID",
            "lvl2"      : "GBC_BILLING RELATED COMPLAINT",
            "lvl3"      : "PAYMENT RELATED",
            "lvl4"      : "UNPOSTED PAYMENT",
            "lvl5"      : "ENDORSED TO BILLING FOR PROCESSING",
            "reason"    : "reconnection",
            "notes"     : "n/a",
            "sla"       : "3 days"
        },
        constants.BB_LOB_NAME: {
            "title"     : "FBM BROADBAND RECONNECTION REQUEST WITH UPP",
            "queue"     : "BCM Unposted Paymt-CONS",
            "lvl1"      : "WIRELINE_WIRELINE",
            "lvl2"      : "WBC_BILLING RELATED COMPLAINT",
            "lvl3"      : "PAYMENT RELATED",
            "lvl4"      : "UNPOSTED PAYMENT_CONS",
            "lvl5"      : "ENDORSED TO BILLING FOR PROCESSING",
            "reason"    : "reconnection",
            "notes"     : "n/a",
            "sla"       : "3 days"
        },
        "default": {}
    },
    "recon-pymt-posted-but-no-connection": {
        constants.POSTPAID_LOB_NAME: {
            "title"     : "FBM MOBILE POSTPAID RECONNECTION REQUEST",
            "lvl1"      : "GHP_GLOBE POSTPAID",
            "lvl2"      : "GAM_ACCOUNT RELATED MODIFICATION",
            "lvl3"      : "ACCOUNT STATUS",
            "lvl4"      : "RESUME REQUEST",
            "lvl5"      : "ENDORSED TO SUPPORT GROUP FOR HANDLING",
            "reason"    : "n/a",
            "notes"     : "reconnection",
            "queue"     : "AP ROB PALAWAN APRVR",
            "sla"       : "2 hours"
        },
	    constants.BB_LOB_NAME: {
            "title"     : "FBM BROADBAND POSTPAID RECONNECTION REQUEST",
            "lvl1"      : "WIRELINE_WIRELINE",
            "lvl2"      : "WAM_ACCOUNT RELATED MODIFICATION",
            "lvl3"      : "ACCOUNT STATUS",
            "lvl4"      : "RESUME REQUEST",
            "lvl5"      : "ENDORSED TO SUPPORT GROUP FOR HANDLING",
            "reason"    : "n/a",
            "notes"     : "reconnection",
            "queue"     : "SF WIRELINE RECONNECTION",
            "sla"       : "4 hours"
        },
	    "default": {}
    },
    "recon-td-due-to-out-of-country": {
        constants.POSTPAID_LOB_NAME: {
            "title"     : "FBM SI TD RECONNECTION RQST OUT OF THE COUNTRY",
            "queue"     : "TP Wireless Tier2",
            "lvl1"      : "GHP_GLOBE POSTPAID",
            "lvl2"      : "GAM_ACCOUNT RELATED MODIFICATION",
            "lvl3"      : "ACCOUNT STATUS",
            "lvl4"      : "RESUME REQUEST",
            "lvl5"      : "ENDORSED TO SUPPORT GROUP FOR HANDLING",
            "reason"    : "reconnection",
            "notes"     : "n/a",
            "sla"       : "24 hours"
        },
        constants.BB_LOB_NAME: {
            "title"     : "FBM SI TD RECONNECTION RQST",
            "queue"     : "CNX Wireline Chat2Call",
            # "queue"     : "CCM FEEDBACK WIRELINE", # for testing only
            "lvl1"      : "WIRELINE_WIRELINE",
            "lvl2"      : "WAM_ACCOUNT RELATED MODIFICATION",
            "lvl3"      : "ACCOUNT STATUS",
            "lvl4"      : "RESUME REQUEST",
            "lvl5"      : "ENDORSED TO SUPPORT GROUP FOR HANDLING",
            "reason"    : "reconnection",
            "notes"     : "n/a",
            "sla"       : "24 hours"
        },
        "default": {}
    },
    "td-due-to-out-of-country": {
        constants.POSTPAID_LOB_NAME: {
            "title"     : "FBM SI TD RECONNECTION RQST OUT OF THE COUNTRY",
            "queue"     : "TP Wireless Tier2",
            "lvl1"      : "GHP_GLOBE POSTPAID",
            "lvl2"      : "GAM_ACCOUNT RELATED MODIFICATION",
            "lvl3"      : "ACCOUNT STATUS",
            "lvl4"      : "RESUME REQUEST",
            "lvl5"      : "ENDORSED TO SUPPORT GROUP FOR HANDLING",
            "reason"    : "reconnection",
            "notes"     : "n/a",
            "sla"       : "24 hours"
        },
        constants.BB_LOB_NAME: {
            "title"     : "FBM SI TD RECONNECTION RQST OUT OF THE COUNTRY",
            "queue"     : "CNX Wireline Chat2Call",
            # "queue"     : "CCM FEEDBACK WIRELINE", # for testing on dev only
            "lvl1"      : "WIRELINE_WIRELINE",
            "lvl2"      : "WAM_ACCOUNT RELATED MODIFICATION",
            "lvl3"      : "ACCOUNT STATUS",
            "lvl4"      : "RESUME REQUEST",
            "lvl5"      : "ENDORSED TO SUPPORT GROUP FOR HANDLING",
            "reason"    : "reconnection",
            "notes"     : "n/a",
            "sla"       : "24 hours"
        },
        "default": {}
    },
    "get-globe-at-home": {
        constants.PLATINUM_MOBIE_LOB_NAME: {
            "title"     : "Globe Fiber BB_Callback Request",
            "queue"     : "CS PAM SUPPORT",
            "lvl1"      : "APPLICATION PROCESS",
            "lvl2"      : "AAV_VERIFICATION",
            "lvl3"      : "ADDITIONAL ACCOUNT",
            "lvl4"      : "BROADBAND",
            "lvl5"      : "ENDORSED TO OM",
            "reason"    : "get globe at home",
            "notes"     : "n/a",
            "sla"       : "3 days"
        },
        "default": {}
    },
    "check-application-renewal-online": {
        constants.POSTPAID_LOB_NAME: {
            "title"     : "LEX_Renewal Online",
            "queue"     : "CBS QA",
            "lvl1"      : "GHP_GLOBE POSTPAID",
            "lvl2"      : "GRC_RECONTRACTING RELATED",
            "lvl3"      : "OTHER RECONTRACTING RELATED CONCERN",
            "lvl4"      : "OTHERS",
            "lvl5"      : "ENDORSED TO SUPPORT GROUP FOR HANDLING",
            "reason"    : "check application",
            "notes"     : "n/a",
            "sla"       : "48 hours"
        },
        "default": {}
    },
    "check-application-renewal-store-with-ref-no": {
        constants.POSTPAID_LOB_NAME: {
            "title"     : "LEX_Renewal Easy Hub",
            "queue"     : "CBS QA",
            "lvl1"      : "GHP_GLOBE POSTPAID",
            "lvl2"      : "GRC_RECONTRACTING RELATED",
            "lvl3"      : "OTHER RECONTRACTING RELATED CONCERN",
            "lvl4"      : "OTHERS",
            "lvl5"      : "ENDORSED TO SUPPORT GROUP FOR HANDLING",
            "reason"    : "check application",
            "notes"     : "n/a",
            "sla"       : "48 hours"
        },
        "default": {}
    },
    "check-application-renewal-store-without-ref-no": {
        constants.POSTPAID_LOB_NAME: {
            "title"     : "LEX_Renewal Globe Stores",
            "queue"     : "CBS Sales Ordering",
            "lvl1"      : "GHP_GLOBE POSTPAID",
            "lvl2"      : "GRC_RECONTRACTING RELATED",
            "lvl3"      : "OTHER RECONTRACTING RELATED CONCERN",
            "lvl4"      : "OTHERS",
            "lvl5"      : "ENDORSED TO SUPPORT GROUP FOR HANDLING",
            "reason"    : "check application",
            "notes"     : "n/a",
            "sla"       : "48 hours"
        },
        "default": {}
    },
    "network-concern-no-internet": {
        constants.BB_LOB_NAME: {
            "title"     : "FBM_FOR ONSITE REPAIR_NO INTERNET NO DIAL TONE",
            "queue"     : "Wireline IROC CFT",
            "lvl1"      : "TT_TROUBLE TICKET",
            "lvl2"      : "WTB-VOICE AND DATA RELATED",
            "lvl3"      : "NO VOICE NO DATA",
            "lvl4"      : "NO INTERNET NO DIAL TONE",
            "lvl5"      : "ENDORSED TO CFS",
            "reason"    : "Onsite Visit",
            "notes"     : "n/a",
            "sla"       : "48 hours",
            "issuestartdate": "true"
        },
        "default": {}
    },
    "network-concern-slow-internet": {
        constants.BB_LOB_NAME: {
            "title"     : "FBM_FOR ONSITE REPAIR_ACROSS ALL SITES",
            "queue"     : "Wireline IROC CFT",
            "lvl1"      : "TT_TROUBLE TICKET",
            "lvl2"      : "WTC_CONNECTION RELATED",
            "lvl3"      : "SLOW BROWSING",
            "lvl4"      : "ACROSS ALL SITES",
            "lvl5"      : "ENDORSED TO CFS",
            "reason"    : "Onsite Visit",
            "notes"     : "n/a",
            "sla"       : "48 hours",
            "issuestartdate": "true"
        },
        "default": {}
    },
    "network-concern-no-landline": {
        constants.BB_LOB_NAME: {
            "title"     : "FBM_FOR ONSITE REPAIR_UPON HANDSET PICK UP",
            "queue"     : "Wireline IROC CFT",
            "lvl1"      : "TT_TROUBLE TICKET",
            "lvl2"      : "WTV_VOICE RELATED",
            "lvl3"      : "NO DIAL / BUSY TONE",
            "lvl4"      : "UPON HANDSET PICK  UP",
            "lvl5"      : "ENDORSED TO CFS",
            "reason"    : "Onsite Visit",
            "notes"     : "n/a",
            "sla"       : "48 hours",
            "issuestartdate": "true"
        },
        "default": {}
    },
    "network-concern-prolonged-outage": {
        constants.BB_LOB_NAME: {
            "title"     : "PART OF PROLONG OUTAGE",
            "queue"     : "CARE_MANAGER_TM",
            "lvl1"      : "WIRELINE_WIRELINE",
            "lvl2"      : "WDR_DEVICE & NETWORK RELATED COMPLAINT",
            "lvl3"      : "OUTAGE REPORT",
            "lvl4"      : "NO CONNECTION",
            "lvl5"      : "ENDORSED TO IROC",
            "reason"    : "",
            "notes"     : "n/a",
            "sla"       : "48 hours"
        },
        "default": {}
    },
    "network-concern-open-order": {
        constants.BB_LOB_NAME: {
            "title"     : "FBM_FOR ONSITE REPAIR_ WITH OPEN ORDER",
            "queue"     : "TP Wireline Tier2",
            "lvl1"      : "WIRELINE_WIRELINE",
            "lvl2"      : "WDR_DEVICE & NETWORK RELATED COMPLAINT",
            "lvl3"      : "REPAIR",
            "lvl4"      : "OTHERS",
            "lvl5"      : "ENDORSED TO IROC",
            "reason"    : "Onsite Visit",
            "notes"     : "n/a",
            "sla"       : "48 hours"
        },
        "default": {}
    },
    "unreflected-payment": {
        constants.POSTPAID_LOB_NAME: {
            "title"     : "FBM MOBILE POSTPAID UPP REQUEST",
            "queue"     : "BCM Unposted Paymt-CONS",
            "lvl1"      : "GHP_GLOBE POSTPAID",
            "lvl2"      : "GBC_BILLING RELATED COMPLAINT",
            "lvl3"      : "PAYMENT RELATED",
            "lvl4"      : "UNPOSTED PAYMENT",
            "lvl5"      : "ENDORSED TO BILLING FOR PROCESSING",
            "reason"    : "billing",
            "notes"     : "n/a",
            "sla"       : "3 days"
        },
        constants.BB_LOB_NAME: {
            "title"     : "FBM BROADBAND UPP REQUEST",
            "queue"     : "BCM Unposted Paymt-CONS",
            "lvl1"      : "WIRELINE_WIRELINE",
            "lvl2"      : "WBC_BILLING RELATED COMPLAINT",
            "lvl3"      : "PAYMENT RELATED",
            "lvl4"      : "UNPOSTED PAYMENT_CONS",
            "lvl5"      : "ENDORSED TO BILLING FOR PROCESSING",
            "reason"    : "billing",
            "notes"     : "n/a",
            "sla"       : "3 days"
        },
        "default": {}
    }
}