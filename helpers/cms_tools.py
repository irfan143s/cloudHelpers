import os
import json
from helpers.dbtools import DbTools
from configuration import CMS_NIA_DB, REGION, CMS_ENDSTATE_DB
from helpers.tools import error_handling

class CMSTools:
    def __init__(self):
        try:
            self.__cmsTable = DbTools(REGION, CMS_NIA_DB)

        # CMS DB Table not found
        except Exception as error:
            print(f"{CMS_NIA_DB} CMS DB not found.")

            errorString = str(error.__class__.__name__) + "\n" + str(error) + "\n"
            print(errorString)

    def getMenuCarousel(self, spiel_key, lob, mustReconnect=False, hasVoucher=False, isRetailer=False):
            try:
                cms_item = self.__cmsTable.getRowEqualsWithSort('spiel-key', spiel_key, "lob", lob)['Items'][0]

                try:
                    cms_cards_arrange = sorted(cms_item['cards-arrange'].items())
                    cms_cards_toggle = cms_item['cards-toggle']

                    cards = []
                    for _, card_name in  cms_cards_arrange:
                        # Hide Reconnect card if not viable for Reconnect
                        if card_name == "reconnect-my-line" and not mustReconnect:
                            continue
                    
                        # Hide Voucher card if not viable for Voucher
                        elif card_name == "special-offers" and not hasVoucher:
                            continue

                        # Hide Reconnect card if not Retailer
                        elif card_name == "my-amax-wallet" and not isRetailer:
                            continue

                        elif cms_cards_toggle[card_name]:
                            cards.append(card_name)

                    return cards

                # Card data and/or toggles not found
                except Exception as error:
                    print (f"CMS Items for {lob} cannot be found.")
                    
                    errorString = str(error.__class__.__name__) + "\n" + str(error) + "\n"
                    print(errorString)

            # Spiel Key and LOB not found
            except Exception as error:
                print(f"{spiel_key} CMS toggle for {lob} cannot be found. Please double check.")

                errorString = str(error.__class__.__name__) + "\n" + str(error) + "\n"
                print(errorString)

    def getMenuCards(self, lob, cards, language=None, isRetailer=False):
        headers, buttons = [], []
        for card in cards:
            try:
                cms_item = self.__cmsTable.getRowEqualsWithSort('spiel-key', card, "lob", lob)['Items'][0]

                cms_buttons_arrange = sorted(cms_item['buttons-arrange'].items())
                cms_buttons_toggle = cms_item['buttons-toggle']
                cms_buttons_spiels = cms_item["buttons-spiels"]

                button_set = []
                for _, button in cms_buttons_arrange:
                    # Hide Buy load button if Retailer and card is My Prepaid Account
                    if isRetailer and card == "my-prepaid-account" and button == "buy-load":
                        continue

                    elif cms_buttons_toggle[button]:
                        button_set.append(cms_buttons_spiels[button])

                # Get card Header, Subtitle and Image if button set isn't empty
                if button_set:
                    try:
                        if language and isinstance(cms_item['card-subtitle'], dict):
                            subtitle = cms_item['card-subtitle'][language]
                        else:
                            subtitle = cms_item['card-subtitle']

                        image = cms_item['card-image']
                    except:
                        subtitle = ''
                        image = ''

                    # Add card's header
                    headers.append([cms_item['card-header'], subtitle, image])

                    buttons.append(button_set)

            # Button data and toggle snot found
            except Exception as error:
                print(f"{card} toggle for {lob} cannot be found. Please double check.")

                errorString = str(error.__class__.__name__) + "\n" + str(error) + "\n"
                print(errorString)
            
        return headers, buttons

    def isEnabled(self, spiel_key, lob, cms_type="intent", flow=""):
        try:
            cms_item = self.__cmsTable.getRowEqualsWithSort('spiel-key', spiel_key, "lob", lob)['Items'][0]
            print(cms_item)
            if cms_type == "intent":
                print(type(cms_item["intent-toggle"]))
                return cms_item["intent-toggle"]

            elif cms_type == "flow":
                return cms_item["flows-toggle"][flow]

            else:
                return False

        # Intent/Flow toggle not found
        except Exception as error:
            if cms_type == "intent":
                print(f"{spiel_key} toggle for {lob} not found.")

            elif cms_type == "flow":
                print(f"{flow} flow togge for {lob} not found in {spiel_key}.")

            errorString = str(error.__class__.__name__) + "\n" + str(error) + "\n"
            print(errorString)

            return False
        
    def getFlowItem(self, spiel_key, lob, item=""):
        '''
        Accepted values in item:
            flow-spiels
            flow-images
            flow-responses
            flow-cards
        '''

        try:
            cms_item = self.__cmsTable.getRowEqualsWithSort('spiel-key', spiel_key, "lob", lob)['Items'][0]

            if item in ["flow-responses", "media-list"]:
                item_list = []

                items_arrange = sorted(cms_item[item + "-arrange"].items())
                items_toggle = cms_item[item + "-toggle"]
                items = cms_item[item]

                for _, item in items_arrange:
                    print(item)
                    if items_toggle[item]:
                        item_list.append(items[item])

                return item_list

            elif item:
                return cms_item[item]

            else:
                return cms_item

        # CMS toggle not found
        except Exception as error:
            print(f"{spiel_key} {item} for {lob} not found.")

            errorString = str(error.__class__.__name__) + "\n" + str(error) + "\n"
            print(errorString)

            return None
        
    
def getCmsItems(spiel_key, lob, res, convo, event, invokeLambda, senderId, lastNumber, lastIntent):
    try:
        # CMS_NIA_DB = lex-dev-cms-trial
        dbCmsEndstate = DbTools(REGION, CMS_ENDSTATE_DB)
        
        try:
            cms_item = dbCmsEndstate.getRowEqualsWithSort("spiel_key", spiel_key, "LOB", lob)["Items"][0]

            return cms_item
        except:
            print(f"{spiel_key} for {lob} cannot be found. Please double check and try again.")
            error_handling(res, convo, event, invokeLambda, senderId, lastNumber, lob, lastIntent, None)
    except:
        print(f"Error connect to {CMS_NIA_DB} CMS DB.")
        error_handling(res, convo, event, invokeLambda, senderId, lastNumber, lob, lastIntent, None)
