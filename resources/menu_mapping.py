# NIAS 2.0
import resources.menus as menus
import resources.states as states

menu_to_session_state_map = {
    menus.MENU_RECON_ISSUE_WITH_MY_BILL                         : states.RECONNECT_MY_LINE_STATE,
    menus.MENU_RECON_PAYMENT_NOT_REFLECTED                      : states.RECONNECT_MY_LINE_STATE,
    menus.MENU_RECON_ISSUE_WITH_MY_BILL                         : states.RECONNECT_MY_LINE_STATE,
    menus.MENU_RECON_ISSUE_WITH_MY_PYMT_CHANNEL                 : states.RECONNECT_MY_LINE_STATE,
    menus.MENU_RECON_PYMT_NOT_REFLECTED_CHANNEL_GLOBE_APPS      : states.RECONNECT_MY_LINE_STATE,
    menus.MENU_RECON_PYMT_NOT_REFLECTED_CHANNEL_BANKS           : states.RECONNECT_MY_LINE_STATE,
    menus.MENU_RECON_PYMT_NOT_REFLECTED_CHANNEL_OTHERS          : states.RECONNECT_MY_LINE_STATE,
    menus.MENU_RECON_TD_LOST_PHONE_OR_SIM                       : states.RECONNECT_MY_LINE_STATE,
    menus.MENU_RECON_TD_OUT_OF_COUNTRY                          : states.RECONNECT_MY_LINE_STATE,

    menus.MENU_UNLOCK_DEVICE_PHONE_BRAND_SAMSUNG                : states.UNLOCK_DEVICE_STATE,   
    menus.MENU_UNLOCK_DEVICE_PHONE_BRAND_APPLE                  : states.UNLOCK_DEVICE_STATE,   
    menus.MENU_UNLOCK_DEVICE_PHONE_BRAND_OTHERS                 : states.UNLOCK_DEVICE_STATE 
}
