########################### Personal Identifiable Information ########################################
PII_PASS_THRESHOLD = 1
PII_FAIL_THRESHOLD = 2
pii_questions = {
    'EMAIL_ADDRESS' : {'question': 'What is your current email address where your monthly Globe bills are sent?\n\n(e.g. johndoe123@gmail.com)','crmMapping':'email'},
    'MOTHERS_MAIDEN_NAME' : {'question': 'What\'s your mother\'s complete maiden name?\n\n(Your mother\'s full name before getting married)','crmMapping':'motherMaiden'},
    'BILLING_OR_INSTALLATION_ADDRESS' : {'question': 'If your concern is regarding your mobile number, please provide the registered billing address of your Globe Postpaid plan. This is the address indicated in your bill.\n\nIf it\'s for your broadband account, please provide the home address where your Globe at Home broadband plan is currently installed.','crmMapping':'billingOrInstallationAddress'},
}

################################## Account Information ###############################################
AI_PASS_THRESHOLD = 3
AI_FAIL_THRESHOLD = 2
ai_questions = {
    'MOBILE_OR_BROADBAND_PLAN' : {'question': 'Please enter your concerned Mobile or Broadband plan\'s Monthly fee.(ex. 1499 for plan 1499)\n\nYou can view this using the GlobeOne app.','crmMapping':'planAmount'},
    'RECENTLY_PAID_AMOUNT' : {'question': 'What was the amount you most recently paid for your plan?\n\nThis can be found using the GlobeOne app by tapping on "My Transactions" > "Bills Payments".\n\n Enter the amount without the centavos (ex. 1299).','crmMapping':'lastBill'},
    'PAYMENT_CHANNEL_USED' : {'question': 'What payment channel did you last pay your plan in?\n\nThis can be found using the GlobeOne app by tapping on "My Transactions" > "Bills Payments".','crmMapping':'paymentChannel'}
}