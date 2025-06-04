LOGS_TTL_DAYS = 180

LOG_TYPE_SINGLE_IDENTITY_CROSSING_USER = "single-identity-crossing-user"
LOG_TYPE_FRAUD_URLS = "fraud-urls"

LOG_TYPES_REQUIRED_FIELDS = {
    LOG_TYPE_SINGLE_IDENTITY_CROSSING_USER: [
        "fbName",
        "currentPsid",
        "currentPageId",
        "currentPageEntity",
        "activePsid",
        "activePageId",
        "activePageEntity"
    ],
    LOG_TYPE_FRAUD_URLS: [
        "psid",
        "pageId",
        "urls"
    ]
}
