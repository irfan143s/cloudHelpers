from configuration import env_lex, env_imrs
# Lambda functions

STATE_CHECKER_LAMBDA = f"lex-api-{env_lex}-stateChecker"
OTP_LAMBDA = f"lex-api-{env_lex}-otp"

REGISTRATION_LAMBDA = f"lex-api-{env_lex}-registration"
MENU_LAMBDA = f"lex-api-{env_lex}-menu"
MAIN_MENU_LAMBDA = f"lmb-lex-{env_lex}-menu"
FOLLOW_UP_LAMBDA = f"lex-api-{env_lex}-followUp"
BALANCE_LAMBDA = f"lex-api-{env_lex}-getOutstandingBalance"
DATA_USAGE_LAMBDA = f"lex-api-{env_lex}-getDataUsage"
PLAN_DETAILS_LAMBDA = f"lex-api-{env_lex}-getPlanDetails"
UNBILLED_CHARGES_LAMBDA = f"lex-api-{env_lex}-getUnbilledCharges"
BILL_REQUEST_LAMBDA = f"lex-api-{env_lex}-sendBill"
PAYMENT_OPTIONS_LAMBDA = f"lex-api-{env_lex}-paymentOptions"
TRANSFER_LAMBDA = f"lex-api-{env_lex}-transferToAgent"
# REF_LINK_LAMBDA = f"lex-api-{env_lex}-refLink"
TROUBLESHOOTING_LAMBDA = f"lex-api-{env_lex}-troubleshooting"
JACK_RABBIT_LAMBDA = f"lex-api-{env_lex}-jackRabbit"
ADVISORY_LAMBDA = f"lex-api-{env_lex}-advisory"
CALL_PLAN_DETAILS_LAMBDA = f"lex-api-{env_lex}-callGlobeOnePlanDetails"
CALL_UNBILLED_CHARGES_LAMBDA = f"lex-api-{env_lex}-callGlobeOneUnbilledCharges"
BUY_LOAD_LAMBDA = f"lex-api-{env_lex}-buyLoad"
BUY_LOAD_WEBVIEW_LAMBDA = f"lex-api-{env_lex}-buyLoadWebview"
LANGUAGE_LAMBDA = f"lex-api-{env_lex}-languageOption"
CHECK_RETAILER_USER_LAMBDA = f"lex-api-{env_lex}-checkRetailerUser"
REPORT_ISSUE_LAMBDA = f"lex-api-{env_lex}-reportIssue"
CHICAGO_LAMBDA = f"lex-api-{env_lex}-chicago"
AMAX_FAQS_LAMBDA= f"lex-api-{env_lex}-amaxFaqs"
RENEW_ONE_ACCOUNT_LAMBDA= f"lex-api-{env_lex}-renewOneAccount"
CONTRACT_END_DATE_LAMBDA = f"lex-api-{env_lex}-getContractEndDate"
OVERDUE_LAMBDA = f"lex-api-{env_lex}-getOverdueBalance"
SUB_DETAILS_LAMBDA = f"lex-api-{env_lex}-callGlobeOneSubscriberDetails"
RENEW_MY_PLAN_LAMBDA = f"lex-api-{env_lex}-renewPlan"
INSTALLMENT_PAYMENT_LAMBDA = f"lex-api-{env_lex}-installmentPayment"
VOUCHER_LAMBDA = f"lex-api-{env_lex}-voucher"
RECONNECT_LINE_LAMBDA = f"lex-api-{env_lex}-reconnectMyLine"
CAMPAIGN_TEMPLATE_LAMDBA = f"lex-api-{env_lex}-campaignTemplate"
VOC_LAMDBA = f"lex-api-{env_lex}-voc"
VOC_COUNTER_LAMDBA = f"lex-api-{env_lex}-vocCounter"
VOC_LAMBDA_ARN = F"arn:aws:lambda:us-west-2:073504361408:function:lex-api-{env_lex}-voc"
CHANGE_PLAN_LAMDBA = f"lex-api-{env_lex}-changePlan"
RENEW_MY_PLAN_ADVISORY_LAMBDA = f"lex-api-{env_lex}-renewPlanAdvisory"

# External Lambdas from Connect
MAIN_CONNECT_LAMBDA = f"imrs-api-{env_imrs}-ConnectMain"
UNBILLED_CONNECT_LAMBDA = "imrs-api-prd-getUnbilledCharges"
SMS_CONNECT_LAMBDA = "imrs-api-prd-publishSMSThroughRaven"
SUBSCRIBER_PRODUCTS_CONNECT_LAMBDA = "imrs-api-prd-getSubscriberProducts"
DATA_USAGE_CONNECT_LAMBDA = "imrs-api-prd-retrieveSubscriberUsages"
OUTSTANDING_CONNECT_LAMBDA = "imrs-api-prd-OutstandingBalanceAPI"
CONTRACT_END_CONNECT_LAMBDA = "imrs-api-prd-contractEndDate"
DISCONNECTION_CONNECT_LAMBDA = f"imrs-api-{env_imrs}-Reconnection"
BB_DISCONNECT_CONNECT_LAMBDA = f"imrs-api-{env_imrs}-bbDisconnectLineDetails"
SEND_BILL_CONNECT_LAMBDA = "imrs-api-prd-sendBillLink"
PREPAID_BALANCE_LAMBDA = "imrs-api-prd-balanceInquiry"
REWARDS_CONNECT_LAMBDA = "imrs-api-prd-getRewards"
JACK_RABBIT_CONNECT_LAMBDA = f"imrs-api-{env_imrs}-checkJackrabbitWhitelist"
ADVISORY_CONNECT_LAMBDA = f"imrs-api-{env_imrs}-CheckAdvisoryWhitelist"
AMAX_TRANSACTION_HISTORY_LAMBDA = f"lex-api-{env_lex}-transactionHistory"
SHEET_APPEND_LAMBDA = f"lex-api-{env_lex}-sheetAppend"
UPGRADE_PLATINUM_LAMBDA = f"lex-api-{env_lex}-upgradePlatinum"
SEND_REPORTS_LAMBDA = f"lex-api-{env_lex}-sendReportsEmail"
GO_HEALTH_LAMBDA = f"lex-api-{env_lex}-goHealth"
# GAH Lambdas
TRANSFER_TO_GAH_LAMBDA = f"lex-api-{env_lex}-transferToGAH"
SHOP_VOUCHER_LAMBDA = f"lex-api-{env_lex}-shopVoucher"
REPORT_SPAM_LAMBDA = f"lex-api-{env_lex}-reportSpam"
BIRTHDAY_TREATS_LAMBDA = f"lex-api-{env_lex}-birthdayTreats"
REG_UPGRADE_PLAT_INTENT = "reg upgrade plat"
OVERDUE_CONNECT_LAMBDA = "imrs-api-prd-overdueBalanceAPI"
RECONNECT_LINE_LAMBDA = f"lex-api-{env_lex}-reconnectMyLine"
CONNECT_BARRING_LAMBDA = f"imrs-api-{env_imrs}-retrieveAccountBarringInfo"
CREATE_CASE_LAMBDA = f"imrs-api-{env_imrs}-createMYBSSCase"

# Chicago V2
CHICAGO_V2_LAMBDA = f"lex-api-{env_lex}-chicagoV2"
# NIA Lambdas
SUBMENU_CHECKER_LAMBDA = f"lex-api-{env_lex}-subMenuChecker"
SUBMENU_REPORT_A_PROBLEM_LAMBDA = f"lex-api-{env_lex}-submenuReportAProblem"
SUBMENU_OTHER_REQUESTS_LAMBDA = f"lex-api-{env_lex}-submenuOtherRequests"
SUBMENU_ACCOUNT_INFORMATION_LAMBDA = f"lex-api-{env_lex}-submenuAccountInformation"

GET_ACCOUNT_NUMBER_LAMBDA = f"lex-api-{env_lex}-getAccountNumber"
GET_REWARDS_LAMBDA = f"lex-api-{env_lex}-getRewards"
TERMINATE_LINE_LAMBDA = f"lex-api-{env_lex}-terminateLine"
OTHER_GLOBE_ACCOUNT_LAMBDA = f"lex-api-{env_lex}-otherGlobeAccount"
GCASH_CONCERN_LAMBDA = f"lex-api-{env_lex}-gcashConcern"

# Know Contract End Date
CONTRACT_END_DATE_LAMBDA = f"lex-api-{env_lex}-knowContractEndDate"
# Check Application Status
CHECK_APPLICATION_STATUS_LAMBDA = f"lex-api-{env_lex}-checkApplicationStatus"

APPLY_NEW_LINE_LAMBDA = f"lex-api-{env_lex}-applyNewLine"

# Ingestion Lambdas
EDO_PUSH_TO_KINESIS_LAMBDA = f"lex-stream-{env_lex}-pushToKinesis"

# NIAS 2.0
NIAS_STATE_CHECKER_LAMBDA = f"lmb-lex-{env_lex}-gie-stateHandler"
EE_STATE_CHECKER_LAMBDA = f"lmb-lex-{env_lex}-ee-stateHandler"
REF_LINK_LAMBDA = f"lmb-lex-{env_lex}-refLink"
REF_LINK_FLOW_LAMBDA = f"lmb-lex-{env_lex}-refLinkFlow"
DPN_LAMBDA = f"lmb-lex-{env_lex}-dpn"
TRANSFER_TO_AGENT_LAMBDA = f"lmb-lex-{env_lex}-transferToAgent"
ACTIVATE_SIM_LAMBDA = f"lmb-lex-{env_lex}-activateSim"
ACTIVATE_FREEBIES_LAMBDA = f"lmb-lex-{env_lex}-activateFreebies"
NETWORK_CONCERN_LAMBDA = f"lmb-lex-{env_lex}-networkConcern"
LOSTPHONE_OR_SIM_LAMBDA = f"lmb-lex-{env_lex}-lostPhoneOrSim"
SPAM_OR_SCAM_LAMBDA = f"lmb-lex-{env_lex}-spamOrScam"
FOLLOWUP_LAMBDA = f"lmb-lex-{env_lex}-followUp"
HOW_TOS_LAMBDA = f"lmb-lex-{env_lex}-howTos"
SESSION_HANDLER_LAMBDA = f"lmb-lex-{env_lex}-sessionStreamHandler"
SESSION_HANDLER_EE_LAMBDA = f"lmb-lex-{env_lex}-ee-sessionStreamHandler"
SESSION_HANDLER_TM_LAMBDA = f"lmb-lex-{env_lex}-tm-sessionStreamHandler"
CHECK_APPLICATION_LAMBDA = f"lmb-lex-{env_lex}-checkApplication"
FOLLOWUP_CONCERN_LAMBDA = f"lmb-lex-{env_lex}-followUpConcern"
TECHNICIAN_VISIT_LAMBDA = f"lmb-lex-{env_lex}-technicianVisit"
ACCOUNT_REQUESTS_LAMBDA = f"lmb-lex-{env_lex}-accountRequests"
TRANSFER_OWNERSHIP_LAMBDA = f"lmb-lex-{env_lex}-transferOwnership"
REPLACE_RETURN_DEVICE_LAMBDA = f"lmb-lex-{env_lex}-replaceReturnDevice"
ACCOUNT_OTHERS_LAMBDA = f"lmb-lex-{env_lex}-accountOthers"
ACCOUNT_FOLLOWUP_LAMBDA = f"lmb-lex-{env_lex}-accountFollowUp"
BILLS_AND_PAYMENTS_LAMBDA = f"lmb-lex-{env_lex}-billsAndPayments"
MODIFY_OR_TERMINATE_LAMBDA = f"lmb-lex-{env_lex}-modifyOrTerminate"
RECONNECT_MY_LINE_LAMBDA = f"lmb-lex-{env_lex}-reconnectMyLine"
RENEW_PLAN_LAMBDA = f"lmb-lex-{env_lex}-renewPlan"
APPLY_NEW_LINE_LAMBDA = f"lmb-lex-{env_lex}-applyNewLine"
BUY_LOAD_OR_PROMO_LAMBDA = f"lmb-lex-{env_lex}-buyLoadOrPromo"
UNLOCK_DEVICE_LAMBDA = f"lmb-lex-{env_lex}-unlockDevice"
PORT_NUMBER_LAMBDA = f"lmb-lex-{env_lex}-portNumber"
LOAD_PROMOS_AND_REWARDS_LAMBDA= f"lmb-lex-{env_lex}-loadPromosAndRewards"
PUBLISH_SMS_THROUGH_RAVEN_LAMBDA = f"imrs-api-{env_imrs}-publishSMSThroughRaven"
FORM_TO_MAIL_LAMBDA = f"lmb-lex-{env_lex}-formToMail"
SEND_EMAIL_FTM_LAMBDA = f"lmb-lex-{env_lex}-sendEmailFTM"
EMPLOYEE_CARE_LAMBDA = f"lmb-lex-{env_lex}-employeeCare"
GCASH_CONCERNS_LAMBDA = f"lmb-lex-{env_lex}-gcashConcerns"
CHECK_BALANCE_LAMBDA = f"lmb-lex-{env_lex}-checkBalance"
CONCIERGE_LAMBDA = f"lmb-lex-{env_lex}-concierge"
THEA_GCASH_PLATINUM_LAMBDA = f"lmb-lex-{env_lex}-gcashPlatinum"
THEA_GCASH_PLATINUM_NOTIFICATION_LAMBDA = f"lmb-lex-{env_lex}-gcashPlatinumNotification"
FB_PUBLIC_FTM_LAMBDA = f"lmb-lex-{env_lex}-facebookPublic-connectedToAgent"
FB_PUBLIC_EXTRACT_LAMBDA = f"lmb-lex-{env_lex}-facebookPublic-extractFBPublicReport"
REGISTER_SIM_LAMBDA = f"lmb-lex-{env_lex}-registerSim"
FAQ_SIM_LAMBDA = f"lmb-lex-{env_lex}-faq"
ISSUE_WITH_SIM_LAMBDA = f"lmb-lex-{env_lex}-issueWithSim"
QUEUE_PERCENT_LAMBDA = f"lmb-lex-{env_lex}-getDistributionQueue"
QUEUE_PERCENT_EXTRACT_LAMBDA = f"lmb-lex-{env_lex}-queueForecastExtract"
GLOBE_ONE_CONCERNS_LAMBDA = f"lmb-lex-{env_lex}-globeOneConcerns"
CUSTOMER_VERIFICATION_LAMBDA = f"lmb-lex-{env_lex}-customerVerification"

# NIAS 2.0 NEW IVR LAMBDAS
GET_SPECIFIC_CASE_DETAILS_LAMBDA = f"lmb-cnect-{env_lex}-getSpecificCaseDetailsbyMsisdn"
BROADBAND_OUTAGE_LAMBDA = f"lmb-cnect-{env_lex}-bbOutage"
GET_BB_DEVICE_DIAGNOSTIC_DETAILS_LAMBDA = f"lmb-cnect-{env_lex}-getBroadbandDeviceDiagnosticDetailsByAccountIdApi"
GET_BILLING_LIST_LAMBDA = f"lmb-cnect-{env_lex}-GetBillingList"
GET_CEM_SUGGESTION_LAMBDA = f"lmb-cnect-{env_lex}-GetCEMSuggestion"
GET_CEM_SUGGESTIONS_LAMBDA = f"lmb-cnect-{env_lex}-getCEMSuggestions"
CHAT_UPDATE_SESSION_STATUS = f"lmb-cnect-{env_lex}-chat-updateSessionStatus"
SEARCH_APPOINTMENT_SLOT_LAMBDA = f"lmb-cnect-{env_lex}-searchAppointmentSlot"
CONFIRM_APPOINTMENT_SLOT_API_LAMBDA = f"lmb-cnect-{env_lex}-confirmAppointmentSlotApi"
SEARCH_ORDER_API_LAMBDA = f"lmb-cnect-{env_lex}-searchOrderApi"
UPDATE_CASE_DETAILS_API = f"lmb-cnect-{env_lex}-updateCaseDetailsApi"
GET_CUSTOMER_INFO_API_LAMBDA = f"lmb-cnect-{env_lex}-getCustomerInfoApi"
GET_ASSIGNED_PRODUCTS_API_LAMBDA = f"lmb-cnect-{env_lex}-getAssignedProductsApi"
GET_OUTSTANDING_BALANCE_BY_ACCOUNT_ID_API = f"lmb-cnect-{env_lex}-getOutstandingBalanceByAccountIdApi"
GET_OUTSTANDING_BALANCE_BY_MSISDN_API = f"lmb-cnect-{env_lex}-getOutstandingBalanceByMsisdnApi"
FRAUD_TAGGING_API_LAMBDA = f"lmb-cnect-{env_lex}-retrieveSubscriberDetailsByMsisdnApi"
SEND_EMAIL = f"lmb-lex-{env_lex}-sendEmail"

#NIAS 2.0 IVR LAMBDAS
CHECK_ONSITE_VISIT_LAMBDA = f"imrs-api-{env_imrs}-checkOnsiteVisit"
GET_CUSTOMER_PROFILE_INFO_LAMBDA = f"imrs-api-{env_imrs}-getCustomerProfileInfo"
RETRIEVE_ACCOUNT_BARRING_INFO_LAMBDA = f"imrs-api-{env_imrs}-retrieveAccountBarringInfo"
CHECK_SERVICE_RECOVERY_WHITELIST_LAMBDA = f"imrs-api-{env_imrs}-checkServiceRecoveryWhitelist"
GET_CUSTOMER_INFO_LAMBDA = f"imrs-api-{env_imrs}-GetCustomerInfo"
CHECK_KQI_WHITELIST_LAMBDA = f"imrs-api-{env_imrs}-checkKQIWhitelist"
GET_FUP_STATUS_LAMBDA = f"imrs-api-{env_imrs}-getFUPStatus"
BBAPP_FORM_TO_MAIL_LAMBDA = f"imrs-api-{env_imrs}-bbAppRpaFormToMail"
BBAPP_CHECKER_LAMBDA = f"imrs-api-{env_imrs}-bbTroubleshootData"
GET_CASE_DETAILS_LAMBDA = f"imrs-api-{env_imrs}-getCaseDetailsbyMsisdn"
CHECK_OPEN_CASE_DETAILS_LAMBDA = f"imrs-api-{env_imrs}-checkOpenCaseDetails"
CHECK_CLOSE_CASE_DETAILS_LAMBDA = f"imrs-api-{env_imrs}-checkCloseCaseDetails"
PROCESS_CASE_DETAILS_LAMBDA = f"imrs-api-{env_imrs}-processCaseDetailsbyCaseId"
GET_CASE_BY_MSISDN_LAMBDA = f"lmb-cnect-{env_lex}-getCaseByMsisdn"
CHECK_RECONNECTION_REQUEST_LAMBDA = f"imrs-api-{env_imrs}-checkReconRequest"
SAVE_RECONNECTION_REQUEST_LAMBDA = f"imrs-api-{env_imrs}-saveReconnectionRqst"
PUBLISH_SMS_THROUGH_RAVEN_IVRLESS_LAMBDA = f"imrs-api-{env_imrs}-publishSMSThroughRavenIVRless"
GET_DETAILS_BY_ATTRIBUTES_LAMBDA =  f"imrs-api-{env_imrs}-GetDetailsByAttributes"
GET_OUTSTANDING_BALANCE_BY_MSISDN_LAMBDA = f"imrs-api-{env_imrs}-OutstandingBalanceAPI"
GET_ACTIVE_PRODUCTS_LAMBDA = f"imrs-api-{env_imrs}-contractEndDate"
GET_CUSTOMER_LOCATION_LAMBDA = f"imrs-api-{env_imrs}-getCustomerLocationData"
LOG_MOBILE_NETWORK_ISSUE = f"lmb-cnect-{env_lex}-logMobileNetworkIssue"
CHAT_TO_CALL_LAMBDA = f"lmb-lex-{env_lex}-chatToCall"
GET_RESOURCE_INFO_LAMBDA = f"lmb-cnect-{env_lex}-getResourceInfo"
ADVISORY_SETTINGS_LAMBDA = f"imrs-api-{env_imrs}-advisorySettingsJson"
SUBSCRIBER_MYBSS_CASE_INFO_LAMBDA = f"lmb-cnect-{env_lex}-getSubscriberMybssCaseInfo"
PREPAID_FIBER_LAMBDA = f"lmb-cnect-{env_lex}-prepaidFiber"
PROACTIVE_RENEWAL_LAMBDA = f"lmb-lex-{env_lex}-proActiveRenewal"
ROAMING_LAMBDA = f"lmb-lex-{env_lex}-roaming"
GET_RECON_OUTSTANDING_BALANCE_BY_MSISDN_LAMBDA = f"lmb-cnect-{env_lex}-getOutstandingBalanceByMsisdn"
GET_RECON_OUTSTANDING_BALANCE_BY_ACCT_ID_LAMBDA = f"lmb-cnect-{env_lex}-getOutstandingBalanceByAccountId"

#NIAS 2.0 THEA
THEA_MENU_LAMBDA = f"lmb-lex-{env_lex}-thea-menu"
SESSION_HANDLER_THEA_LAMBDA = f"lmb-lex-{env_lex}-thea-sessionStreamHandler"
CAMPAIGNS_LAMBDA = f"lmb-lex-{env_lex}-campaigns"
THEA_BIRTHDAY_TREATS_LAMBDA = f"lmb-lex-{env_lex}-birthdayTreats"
THEA_RENEW_PLAN_LAMBDA = f"lmb-lex-{env_lex}-renewPlanReflink"
THEA_PLATINUM_UPGRADE_LAMBDA = f"lmb-lex-{env_lex}-platinumUpgrade"

#NIAS 2.0 MY BUSINESS
SESSION_HANDLER_MYBIZ_LAMBDA = f"lmb-lex-{env_lex}-myBiz-sessionStreamHandler"
MYBUSINESS_REGISTERING_LAMBDA = f"lmb-lex-{env_lex}-myBiz-registering"
MYBUSINESS_MANAGING_LAMBDA = f"lmb-lex-{env_lex}-myBiz-managing"

#NIAS 2.0 GAH
SESSION_HANDLER_GAH_LAMBDA = f"lmb-lex-{env_lex}-gah-sessionStreamHandler"