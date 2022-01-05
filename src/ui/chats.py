#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
import time
import pywinauto
from ui.user import UI_User
from ui.comm import UI_Comm
from ui.add_member import Dlg_AddMember
from ui.open_dialog import UI_OpenDialog
from ui.dlg_forward import Dlg_Forward
from helper.utils import Utils
from helper.my_logging import *

logger = getMyLogger(__name__)

class UI_Chats:
    def click_chats_button(win):
        # click "Chats Button"
        button = win.child_window(title=u'Chats', control_type='Button')
        if button.exists():
            UI_Comm.click_control(button)
            return button
        return None

    def chat_to(win, member):
        # if there is no name, chat to self
        if member == None:
            return UI_User.chat_to(win)

        logger.info('chat_to "%s<%s>"', member['name'], member['WeChatID'])
        # search from chat name list
        if ('WeChatID' in member) and (not member['WeChatID'].startswith('wxid_')):
            if UI_Chats.search_name(win, member, True) == True:
                if UI_Chats.verify_title(win, member['name']) == True:
                    return True

        if UI_Chats.search_name(win, member, False) == True:
            if UI_Chats.verify_title(win, member['name']) == True:
                return True

        return False


    # retuns the last message
    def get_last_msg(win, member):
        if not UI_Chats.chat_to(win, member):
            return None

        text = None
        # find '消息' List
        list = win.child_window(title=u'消息', control_type='List')
        items = list.children(control_type='ListItem')
        if len(items) > 0:
            text = items[-1].window_text()
        return text

    def select_item(win, item):
        one_by_one = win.child_window(title='One-by-One Forward', control_type='Text')
        # scroll item into view

        if one_by_one.exists():
            UI_Comm.click_control(item)
        else:
            # item [text, link, photo,]
            #   pane
            #       pane    (fill)
            #       pane    (body)
            #       button  (sender)
            body = item.children()[0].children()[1]
            UI_Comm.click_control(body, button='right')
            select = win.child_window(title="Select...", control_type="MenuItem")
            UI_Comm.click_control(select)
        # win.print_control_identifiers(filename='tt2.txt')
        # input('wwwwww')

    def select_last_sention_msgs(win):
        msgs = 0
        if UI_Chats.chat_to(win, None) == False:
            return msgs
        list = win.child_window(title=u'消息', control_type='List')
        items = list.children(control_type='ListItem')
        # select last section of messages
        last = len(items)
        limit = 5  # max number of forward msgs
        while last > 0 and limit > 0:
            last -= 1
            limit -= 1
            item = items[last]
            t = Utils.format_time_tag(item.window_text(), warning=False)
            if t != None:
                break
            # scroll item into view
            rect = list.rectangle()
            while item.rectangle().top < rect.top:     # in view top
                UI_Comm.mouse_scroll(list, 1)  # content down

            itop = item.rectangle().top
            while itop > (rect.bottom+rect.top)/2:
                UI_Comm.mouse_scroll(list, -1)
                if itop == item.rectangle().top:
                    break
                itop = item.rectangle().top

            UI_Chats.select_item(win, item)
            msgs += 1
        return msgs

    def forward_one_by_one(win):
        forward = win.child_window(title='One-by-One Forward', control_type='Text')
        button = forward.parent().children()[0]
        UI_Comm.click_control(button)

    def forward_msgs(win, category, contacts, index):
        if UI_Chats.select_last_sention_msgs(win) == 0:
            return index
        UI_Chats.forward_one_by_one(win)
        dlg = Dlg_Forward.get_forward_dlg(win)
        if dlg == None:
            return index
        while index < len(contacts):
            contact = contacts[index]
            name = contact['name']
            if 'WeChatID' in contact:
                id = contact['WeChatID']
            else:
                id = None
            Dlg_Forward.add_member(dlg, category, name, id)
            index += 1
            if Dlg_Forward.number_selected(dlg) >= 9:
                break
        Dlg_Forward.click_send(dlg)
        return index

    def search_name(win, member, by_id):
        # logger.info('search name "%s", by_id=%s', member['name'], by_id)
        search = UI_Chats.set_focus_search(win)
        # entering [name] in edit box, then 'Enter'
        if by_id:
            if 'WeChatID' in member:
                UI_Comm.send_text(search, member['WeChatID'], False)
            else:
                return False
        else:
            UI_Comm.send_text(search, member['name'], False)

        retry = 5   # need to more than 3 times
        while retry > 0:
            retry -= 1
            list = win.child_window(title='Search Results', control_type='List')
            if list.exists():
                break
            time.sleep(0.2)   # wait to get searh results

        if not list.exists():
            logger.warning('did not find search result')
            return False

        # check if there is the name in search results
        # if yes, click and return True
        items = list.children()
        category = None
        found = False
        for item in items:
            if item.window_text() == '':
                texts = item.children_texts()
                if len(texts) == 0:
                    category = None
                    continue
                category = texts[0]
            else:
                if category == 'Group Chats' or category == 'Contacts':
                    if item.window_text() == member['name']:
                        UI_Comm.click_control(item)
                        found = True
                        break
        if not found:
            logger.warning('did not find named/group "%s"', member['name'])
            return False
        return True

    def get_title_pane(pane):
        for i in [1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]:
            cs = pane.children()
            # expected pane does not exists
            if len(cs) <= i:
                return None
            pane = cs[i]
        return pane

    def verify_title(win, name):
        # logger.info('verify title <%s>', name)
        retry = 10
        while retry > 0:
            retry -= 1
            pane = UI_Chats.get_title_pane(win)
            if pane != None:
                break
            time.sleep(0.2)

        if pane == None:
            return False

        pane.draw_outline()
        if pane.window_text() != name:
            logger.warning('verifying title failed "%s"', name)
            return False
        return True

    # click the edit box
    def click_edit(win):
        UI_Chats.click_chats_button(win)
        edit = win.child_window(title='Enter', control_type='Edit')
        if not edit.exists():
            return None
        retry = 3
        while retry > 0:
            UI_Comm.click_control(edit)
            if edit.has_keyboard_focus():
                break
            time.sleep(0.2)
            retry -= 1

        if retry == 0 and not edit.has_keyboard_focus():
            logger.warning('failed set focus on "edit"')
            raise Error
        return edit

    def set_focus_search(win):
        UI_Chats.click_chats_button(win)
        # put focus in 'Search Edit' field
        search = win.window(title=u'Search', control_type='Edit')
        retry = 3
        while retry > 0:
            if search.has_keyboard_focus():
                break
            UI_Comm.click_control(search)   # get focus
            time.sleep(0.2)
            retry -= 1
        if retry == 0 and not search.has_keyboard_focus():
            logger.warning('failed set focus on "search"')
            raise Error
        return search

    def open_chat_info_window(win):
        button = win.window(title='Chat Info', control_type='Button')
        UI_Comm.click_control(button)

    def click_send_file(win):
        button = win.child_window(title='Send File', control_type='Button')
        if not button.exists():
            logger.warning('did not find "Send File" button')
            return None
        UI_Comm.click_control(button)
        return button

    def upload_file(win, filename):
        logger.info('uploading "%s"', filename)
        if UI_Chats.click_send_file(win) == None:
            return False
        if UI_OpenDialog.open_file(win, filename) == False:
            return False
        edit = UI_Chats.click_edit(win)
        edit.type_keys('{ENTER}')
        return True
