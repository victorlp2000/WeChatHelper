#
# Written By:   Weiping Liu
# Created:      Jul 20, 2021
#
import time
import pywinauto
from ui.comm import UI_Comm
from ui.add_member import Dlg_AddMember
from ui.open_dialog import UI_OpenDialog
from helper.utils import Utils
from helper.my_logging import *

logger = getMyLogger(__name__)

# this is a popup window in case of click member in group member listing
class UI_WeChatPane:
    def get_member_info(win, member=None):
        # open member card window
        # pane = win.child_window(title='WeChat', control_type='Pane', found_index=0)
        # if not pane.exists() and member != None:
            # open member card
        # logger.info('click member...')
        if member != None:
            UI_Comm.click_control(member)

        retry = 5
        while retry > 0:
            retry -= 1
            pane = win.child_window(title='WeChat', control_type='Pane', found_index=0)
            if pane.exists():
                break
        # logger.info('got pane')
        if retry <= 0:
            logger.warning('did not find member card pane')
            return None

        # pane.print_control_identifiers(filename='id.txt')

        info = {}
        pane4c = pane.children()[1].children()[0].children()
        pane5c = pane4c[0].children()
        pane6c = pane5c[0].children()
        info['name'] = pane6c[0].children()[0].window_text()
        # logger.info('got name')
        if len(pane6c) > 1:
            pane8c = pane6c[1].children()
            id_name = pane8c[0].window_text()
            id_value = pane8c[1].window_text()
            info[id_name.replace(' ','').replace(':','')] = id_value
        # logger.info('got id')

        if True:   # disable image and others
            img = pane5c[1].capture_as_image()
            info['img'] = img

            # logger.info('got img')
            pane10c = pane4c[2].children()
            for c in pane10c:
                item = c.children()
                n = item[0].window_text()
                v = item[1].window_text()
                info[n] = v

        # logger.info('esc')
        pane.type_keys('{ESC}')     # close popup card
        return info

    def chat_to(win):
        pane = win.child_window(title='WeChat', control_type='Pane')
        button = pane.child_window(title='Messages', control_type='Button')
        UI_Comm.click_control(button)

    # following version runs much slower
    def get_member_info_0(win):
        pane = win.child_window(title='WeChat', control_type='Pane')
        if not pane.exists():
            logger.warning('did not find member card pane')
            return None
        # pane.print_control_identifiers(filename='id.txt')

        # get number of TEXT controls
        n = 1
        try:
            fields = pane.child_window(control_type='Text')
            fields.exists()
        except pywinauto.findwindows.ElementAmbiguousError as e:
            n = int(str(e).split()[2])         # There are N elements

        name = pane.child_window(control_type='Edit', found_index=0)
        info = {'name': name.window_text()}

        # get picture
        p = pane.child_window(control_type='Button', found_index=0)
        if p.exists():
            info['img'] = p.capture_as_image()

        for index in range(n):
            field = pane.child_window(control_type='Text', found_index=index)
            if not field.exists():
                break
            name = field.window_text()
            if name != '':
                value = field.parent().children()[1].window_text()
                info[name.replace(' ', '').replace(':', '')] = value

        pane.type_keys('{ESC}')     # close popup card
        return info

'''
child_window(title="WeChat", control_type="Pane")
   |
   | Pane - ''    (L855, T119, R1191, B448)
   | ['Pane2', 'WeChat ID: Pane', 'WeChat ID: Pane0', 'WeChat ID: Pane1']
   |
   | Pane - ''    (L875, T139, R1171, B428)
   | ['Pane3', 'WeChat ID: Pane2']
   |    |
   |    | Pane - ''    (L875, T139, R1171, B428)
   |    | ['Pane4', 'WeChat ID: Pane3']
   |    |    |
   |    |    | Pane - ''    (L875, T139, R1171, B255)
   |    |    | ['Pane5', 'WeChat ID: Pane4']
   |    |    |    |
   |    |    |    | Pane - ''    (L907, T171, R1079, B255)
   |    |    |    | ['Pane6', 'WeChat ID: Pane5']
   |    |    |    |    |
   |    |    |    |    | Pane - ''    (L907, T171, R1079, B195)
   |    |    |    |    | ['Pane7']
   |    |    |    |    |    |
   |    |    |    |    |    | Edit - '競芬姐'    (L907, T171, R961, B195)
   |    |    |    |    |    | ['Edit', 'Edit0', 'Edit1']
   |    |    |    |    |    | child_window(title="競芬姐", control_type="Edit")
   |    |    |    |    |    |
   |    |    |    |    |    | Static - ''    (L963, T174, R981, B192)
   |    |    |    |    |    | ['Static', 'Static0', 'Static1']
   |    |    |    |    |
   |    |    |    |    | Pane - ''    (L907, T200, R1079, B220)
   |    |    |    |    | ['Pane8', 'WeChat ID: Pane6']
   |    |    |    |    |    |
   |    |    |    |    |    | Static - 'WeChat ID: '    (L907, T200, R986, B224)
   |    |    |    |    |    | ['Static2', 'WeChat ID: ', 'WeChat ID: Static']
   |    |    |    |    |    | child_window(title="WeChat ID: ", control_type="Text")
   |    |    |    |    |    |
   |    |    |    |    |    | Edit - 'chingfenjie'    (L986, T200, R1062, B220)
   |    |    |    |    |    | ['Edit2', 'WeChat ID: Edit']
   |    |    |    |    |    | child_window(title="chingfenjie", control_type="Edit")
   |    |    |    |
   |    |    |    | Button - '競芬姐'    (L1079, T169, R1139, B229)
   |    |    |    | ['競芬姐Button', 'Button', '競芬姐', 'Button0', 'Button1']
   |    |    |    | child_window(title="競芬姐", control_type="Button")
   |    |    |
   |    |    | Pane - ''    (L907, T255, R1139, B256)
   |    |    | ['Pane9', 'WeChat ID: Pane7']
   |    |    |
   |    |    | Pane - ''    (L907, T272, R1171, B353)
   |    |    | ['Pane10', 'AliasPane', 'AliasPane0', 'AliasPane1']
   |    |    |    |
   |    |    |    | Pane - ''    (L907, T272, R1171, B296)
   |    |    |    | ['Pane11', 'AliasPane2']
   |    |    |    |    |
   |    |    |    |    | Static - 'Alias'    (L907, T273, R957, B295)
   |    |    |    |    | ['Static3', 'AliasStatic', 'Alias']
   |    |    |    |    | child_window(title="Alias", control_type="Text")
   |    |    |    |    |
   |    |    |    |    | Button - 'Tap to add note'    (L965, T274, R1079, B294)
   |    |    |    |    | ['Tap to add noteButton', 'Button2', 'Tap to add note']
   |    |    |    |    | child_window(title="Tap to add note", control_type="Button")
   |    |    |    |
   |    |    |    | Pane - ''    (L907, T299, R1171, B323)
   |    |    |    | ['Pane12', 'AliasPane3']
   |    |    |    |    |
   |    |    |    |    | Static - 'Region'    (L907, T300, R957, B322)
   |    |    |    |    | ['Region', 'Static4', 'RegionStatic']
   |    |    |    |    | child_window(title="Region", control_type="Text")
   |    |    |    |    |
   |    |    |    |    | Edit - 'United States'    (L967, T299, R1056, B323)
   |    |    |    |    | ['Edit3', 'RegionEdit']
   |    |    |    |    | child_window(title="United States", control_type="Edit")
   |    |    |    |
   |    |    |    | Pane - ''    (L907, T326, R1171, B350)
   |    |    |    | ['Pane13', 'RegionPane']
   |    |    |    |    |
   |    |    |    |    | Static - 'From'    (L907, T327, R957, B349)
   |    |    |    |    | ['From', 'Static5', 'FromStatic']
   |    |    |    |    | child_window(title="From", control_type="Text")
   |    |    |    |    |
   |    |    |    |    | Edit - 'Group chat'    (L967, T326, R1042, B350)
   |    |    |    |    | ['Edit4', 'FromEdit']
   |    |    |    |    | child_window(title="Group chat", control_type="Edit")
   |    |    |
   |    |    | Pane - ''    (L875, T373, R1171, B401)
   |    |    | ['Pane14', 'FromPane', 'FromPane0', 'FromPane1']
   |    |    |    |
   |    |    |    | Pane - ''    (L875, T373, R1069, B401)
   |    |    |    | ['Pane15', 'FromPane2']
   |    |    |    |
   |    |    |    | Button - 'Share Contact Card'    (L1069, T373, R1097, B401)
   |    |    |    | ['Button3', 'Share Contact CardButton', 'Share Contact Card']
   |    |    |    | child_window(title="Share Contact Card", control_type="Button")
   |    |    |    |
   |    |    |    | Button - 'Messages'    (L1111, T373, R1139, B401)
   |    |    |    | ['MessagesButton', 'Messages', 'Button4']
   |    |    |    | child_window(title="Messages", control_type="Button")
'''
