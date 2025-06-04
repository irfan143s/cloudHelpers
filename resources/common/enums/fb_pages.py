from enum import Enum

import configuration as configs

class FbPages(Enum):

    GLOBE_TELECOM = configs.GT_PAGE_NAME
    THEA_OF_GLOBE_PLATINUM = configs.THEA_PAGE_NAME
    GLOBE_AT_HOME = configs.GAH_PAGE_NAME
    GLOBE_BUSINESS = configs.MYBUSINESS_PAGE_NAME
    TM_TAMBAYAN = configs.TM_PAGE_NAME

    GLOBE_TELECOM_PAGE_ID = configs.GT_PAGE_ID
    THEA_OF_GLOBE_PLATINUM_PAGE_ID = configs.THEA_PAGE_ID
    GLOBE_AT_HOME_PAGE_ID = configs.GAH_PAGE_ID
    GLOBE_BUSINESS_PAGE_ID = configs.MYBUSINESS_PAGE_ID
    TM_TAMBAYAN_PAGE_ID = configs.TM_PAGE_ID

    # def __str__(self):
    #     return str(self.value)