from configuration import GT_PAGE_NAME, MYBUSINESS_PAGE_NAME, THEA_PAGE_NAME
from resources.constants import *
from resources.spiels import TRANSFERRING_SPIEL, MYBUSINESS_TRANSFER_SPIEL

class SpielTools:
    def __init__(self):
        self.LOB_DICT = {
            POSTPAID_LOB_NAME:self.postpaid_lob,
            PREPAID_LOB_NAME:self.prepaid_lob,
            BUSINESS_SG_LOB_NAME:self.globe_myBusiness_lob,
            TM_LOB_NAME:self.tm_lob,
            BB_LOB_NAME:self.bb_lob,
            "other":self.other_lob
        }
        self.GET_LOB_DICT ={
            BUSINESS_SG_LOB_NAME:self.globe_myBusiness_lob,
            TM_LOB_NAME:self.tm_lob,
            BUSINESS_EG_LOB_NAME:self.eg_lob,
            PLATINUM_MOBIE_LOB_NAME:self.plat_lob
        }
    def page(self,page):
        if page == GT_PAGE_NAME:
            self.accountsHandled = "Postpaid, Prepaid, and Globe At Home accounts"
        elif page == MYBUSINESS_PAGE_NAME:
            self.accountsHandled = "Globe myBusiness accounts"
        elif page == THEA_PAGE_NAME:
            self.accountsHandled = "Globe Platinum account"
    def postpaid_prepaid_inhouse_lob(self):
        self.lob = "Postpaid, Prepaid and Globe at Home"
        self.pageName = "Globe Telecom"
        self.pageUrl = "https://m.me/globeph"
    def postpaid_lob(self):
        self.lob = "Postpaid"
        self.pageName = "Globe Telecom"
        self.pageUrl = "https://m.me/globeph"
    def prepaid_lob(self):
        self.lob = "Prepaid"
        self.pageName = "Globe Telecom"
        self.pageUrl = "https://m.me/globeph"
    def globe_myBusiness_lob(self):
        self.lob = "Globe myBusiness"
        self.pageName = "Globe myBusiness"
        self.pageUrl = "https://m.me/globemybusiness"
    def tm_lob(self):
        self.lob = "TM"
        self.pageName = "TM Tambayan"
        self.pageUrl = "https://m.me/TMtambayan"
    def bb_lob(self):
        self.lob = "Broadband"
        self.pageName = "Globe At Home"
        self.pageUrl = "https://m.me/globeathome"
    def plat_lob(self):
        self.lob = "Globe Platinum"
        self.pageName = "Thea of Globe Platinum"
        self.pageUrl = "https://m.me/TheaOfGlobePlatinum"
    def eg_lob(self):
        self.lob = "enterprise account"
        self.pageName="Globe Business page"
        self.pageUrl="https://m.me/globebusiness"
    def other_lob(self):
        self.lob = ""
        self.pageName=""
        self.pageUrl=""

    def get_lob_spiel(self,page,lobName):
        self.page(page)
        if lobName in [POSTPAID_LOB_NAME,IN_HOUSE_LOB_NAME ,PREPAID_LOB_NAME,SHP_LOB_NAME]:
            self.postpaid_prepaid_inhouse_lob()
        else:
            self.GET_LOB_DICT.get(lobName,self.other_lob)()
        if self.lob:
            lobSpiel = f"We’d love to assist you but we only have access to {self.accountsHandled}. For {self.lob}, you may send a message to {self.pageName} at {self.pageUrl}"
        else:
            lobSpiel = f"We’d love to assist you but we only have access to {self.accountsHandled}."
        return lobSpiel
        
    def upgrade_platinum_intro_spiel(self,page,lobName):
        self.page(page)
        self.LOB_DICT.get(lobName,self.other_lob)()
        if self.lob:
            if self.lob in [POSTPAID_LOB_NAME, PREPAID_LOB_NAME]:
                return f"For {POSTPAID_LOB_NAME} or {PREPAID_LOB_NAME} accounts, you may send a message at {self.pageName}. {self.pageUrl}"
            else:
                 return f"For {self.lob} accounts, you may send a message at {self.pageName}. {self.pageUrl}"
        else:
            return  "I can only help with your " + self.accountsHandled + "."

    def get_transfer_spiel(self, page):
        if page == GT_PAGE_NAME:
            spiel = TRANSFERRING_SPIEL
            
        elif page == MYBUSINESS_PAGE_NAME:
            spiel = MYBUSINESS_TRANSFER_SPIEL
        
        return spiel


