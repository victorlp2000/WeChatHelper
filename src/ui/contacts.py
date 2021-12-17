#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
import time
import pywinauto
from ui.comm import UI_Comm
from ui.add_member import Dlg_AddMember
from ui.open_dialog import UI_OpenDialog
from helper.utils import Utils
from helper.my_logging import *

logger = getMyLogger(__name__)

class UI_Contacts:
    def click_contacts_button(win):
        # click "Contacts Button"
        button = win.child_window(title='Contacts', control_type='Button')
        if button.exists():
            UI_Comm.click_control(button)
            return button
        logger.warning('did not find "Contacts" button')
        return None

    def get_contacts_list(win):
        list = win.child_window(title='Contacts', control_type='List')
        if list.exists() == False:
            logger.warning('did not find "Contacts" button')
            return None
        return list

    # return array of contacts or None
    def get_contacts(win, types, picks=None):
        # press contacts menu
        if UI_Contacts.click_contacts_button(win) == None:
            return None
        # set focus on list
        list = UI_Contacts.get_contacts_list(win)
        UI_Comm.click_control(list)
        # goto top of the list
        list.type_keys('^{HOME}')
        # list_control = list.wrapper_object()
        # print(dir(list.wrapper_object()))
        # input('wait...')
        contacts = []
        saved_groups = []
        last_info = {}
        category = 'Initial'

        while True:
            items = list.children(control_type='ListItem')
            for i in range(len(items)):
                if items[i].is_selected():
                    if i > 0 and items[i-1].window_text() == '':
                        category = items[i-1].children()[0].children()[0].window_text()
                        logger.info('category: "%s"', category)
                    if category == 'Saved Groups':
                        saved_groups.append({'name':items[i].window_text()})

            if category in ['Initial', 'New Friends', 'Official Accounts', 'Saved Groups']:
                list.type_keys('{DOWN}')
                continue

            if types['contacts'] != True:
                break

            info = UI_Contacts.get_contact_info(win)
            if info != None:
                if info == last_info:
                    break
                if picks == '*':
                    contacts.append(info)
                else:
                    data = {}
                    data['name'] = info['name']
                    if 'WeChatID' in info:
                        data['WeChatID'] = info['WeChatID']
                    contacts.append(data)
                last_info = info
            list.type_keys('{DOWN}')
        return {'contacts':contacts, 'saved_groups':saved_groups}

    def get_contact_info(win):
        id = win.child_window(title='WeChat ID', control_type='Text')
        if not id.exists():
            return None
        info = {}
        id_pane = id.parent().parent()

        header = id_pane.parent().children()[0]
        title = header.children()[0].children()[0].children(control_type='Edit')[0]
        picture = header.children(control_type='Button')[0]

        info['name'] = title.window_text()
        info['img'] = picture.capture_as_image()

        panes = id_pane.children(control_type='Pane')
        for pane in panes:
            name = pane.children(control_type='Text')
            value = pane.children(control_type='Edit')
            if len(name) > 0 and len(value) > 0:
                info[name[0].window_text().replace(' ', '')] = value[0].window_text()

        # print(info)
        return info
