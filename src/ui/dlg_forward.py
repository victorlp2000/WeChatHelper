#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
from ui.comm import UI_Comm
from helper.my_logging import *
import pywinauto

logger = getMyLogger(__name__)

class Dlg_Forward:
    def get_forward_dlg(win):
        dlg = win.child_window(title='WeChat', control_type='Window')
        if not dlg.exists():
            logger.warning('did not see forward popup')
            return None
        return dlg

    # returns number of selected
    def add_member(dlg, name, id=None):
        r = False
        if id != None:
            r = Dlg_Forward.search_unique(dlg, id)
        if r == False:
            r = Dlg_Forward.search_unique(dlg, name)
        if r == True:
            logger.info('select forward: "%s"', name)
        else:
            logger.warning('could not find "%s:%s"', name, id)
        return r

    def search_unique(dlg, text):
        # put name in 'Search Edit' field
        edit = dlg.child_window(title='Search', control_type='Edit')

        edit.draw_outline()
        edit.set_focus()
        edit.type_keys('^A{BACKSPACE}')
        UI_Comm.send_text(edit, text)

        # if the name exists, it must have only 1 candidate and 1 selected
        n1 = Dlg_Forward.number_candidate(dlg)
        # print(n1)
        # input('wait...')
        if n1 != 1:
            edit.type_keys('{ENTER}')   # de-select
        return n1 == 1

    def click_send(dlg):
        button = dlg.window(title='Send', control_type='Button')
        UI_Comm.click_control(button)

    def click_cancel(dlg):
        button = dlg.window(title='Cancel', control_type='Button')
        UI_Comm.click_control(button)

    def number_candidate(dlg):
        pane = dlg.children()[1].children()[0]
        list = pane.children(control_type='List')
        print('list:', len(list))
        if len(list) != 1:
            return 0
        # number of items under 'Contacts'
        items = list[0].children()
        start = False
        n = 0
        for item in items:
            # 'pywinauto.controls.uia_controls.ListItemWrapper'
            if type(item) is pywinauto.controls.uiawrapper.UIAWrapper:
                category = item.children()[0].window_text()
                if category == 'Contacts' or category == 'Group Chats':
                    start = True
                else:
                    start = False
                continue
            if start:
                n += 1
        print('n:', n)
        return n

    def number_selected(dlg):
        pane = dlg.children()[1].children()[2]
        list = pane.children(control_type='List')
        if len(list) != 1:
            return 0
        items = list[0].children(control_type='ListItem')
        return len(items)
