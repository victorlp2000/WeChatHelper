#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
from helper.my_logging import *
from ui.comm import UI_Comm
from ui.chats import UI_Chats
from ui.wechat_pane import UI_WeChatPane

logger = getMyLogger(__name__)

class UI_ChatInfo:
    def get_chat_info(win):
        pwin = UI_ChatInfo.open_chat_info(win)
        if pwin == None:
            return None

        # need to scroll into view
        UI_Comm.mouse_scroll(pwin, -30)
        group_name = UI_ChatInfo.get_group_name(pwin)
        announce = UI_ChatInfo.get_announcement(pwin)
        UI_Comm.mouse_scroll(pwin, 30)

        members = UI_ChatInfo.get_members(pwin)
        names = []
        for member in members:
            names.append(member.window_text())

        UI_ChatInfo.close_chat_info(win)

        logger.info('found members: %d', len(members))
        return {'name':group_name, 'announce':announce, 'members':names}

    # returns the 'chat info' window if open successfull,
    # or None if failed
    def open_chat_info(win):
        # if 'Chat Info' window exists, it is in open
        title='Chat Info'
        pwin = win.window(title=title, control_type='Window')
        if pwin.exists():
            return pwin

        # try to open it b pressing '...' (Chat Info) button
        retry = 3
        while retry > 0:
            retry -= 1
            button = win.window(title=title, control_type='Button')
            # if group is been blocked, the button will not shown
            if button.exists():
                UI_Comm.click_control(button)

            pwin = win.window(title=title, control_type='Window', found_index=0)
            if pwin.exists():
                pwin.draw_outline()
                return pwin

        logger.error('failed to open "%s" window', title)
        return None

    def close_chat_info(win):
        # click edit field should cause close chat info window
        UI_Chats.click_edit(win)

        retry = 3
        while retry > 0:
            retry -= 1
            pwin = win.window(title='Chat Info', control_type='Window')
            if not pwin.exists():
                return True

            # close any existing sub-window if there is
            #   AddMemberWnd(Window) - Close/Cancel(Button)
            #   DeleteMemberWnd(Window) - Close/Cancel(Button)
            #   WeChat(Window) for Group Notice - Close(Button)
            subw = pwin.child_window(control_type='Window', found_index=0)
            while subw.exists():
                close = subw.child_window(title='Close', control_type='Button')
                if close.exists():
                    UI_Comm.click_conotrol(close)
                subw = pwin.child_window(control_type='Window', found_index=0)
        logger.warning('failed to close "Chat Info" window')
        return False

    def view_more(pwin):
        # in case of less member, there is no 'View More Members'
        view_more = pwin.window(title='View More Members', control_type='Button')
        if view_more.exists():
            UI_Comm.click_control(view_more)

    def click_add_member(pwin):
        list = pwin.child_window(title='Members', control_type='List')
        items = list.children(control_type='ListItem')
        for item in items:
            if item.window_text() == 'Add':
                UI_Comm.click_control(item)
                return True
        return False

    def scroll_in_view(list, member):
        rect = list.parent().rectangle()
        m_rect = member.rectangle()

        while m_rect.bottom > rect.bottom:
            UI_Comm.mouse_scroll(list.parent(), -10)     # scroll content up
            m_rect = member.rectangle()
        while m_rect.top < rect.top:
            UI_Comm.mouse_scroll(list.parent(), 10)
            m_rect = member.rectangle()

    def get_members(pwin, win, picks):
        logger.info('get members from group')
        # view more suppose to list ALL members
        UI_ChatInfo.view_more(pwin)

        members = []
        list = pwin.window(title='Members', control_type='List')
        items = list.children(control_type='ListItem')
        logger.info('%d members in the list', len(items))

        for item in items:
            name = item.window_text()
            if name == 'Add' or name == 'Delete':
                continue

            UI_ChatInfo.scroll_in_view(list, item)
            info = UI_WeChatPane.get_member_info(win, item)
            if '*' in picks:
                data = info
            else:
                data = {}
                if 'name' in info:
                    data['name'] = info['name']
                if 'WeChatID' in info:
                    data['WeChatID'] = info['WeChatID']
            if info != None:
                members.append(data)
                logger.info('%s', str(info))

            # for testing
            # if len(members) >= 15:
            #     break
        return members

    def get_members_fast(pwin, win, picks):
        logger.info('get members from group')
        # view more suppose to list ALL members
        UI_ChatInfo.view_more(pwin)

        members = []
        list = pwin.window(title='Members', control_type='List')
        items = list.children(control_type='ListItem')
        logger.info('%d members in the list', len(items))

        for item in items:
            item.draw_outline()
            name = item.window_text()
            if name == 'Add' or name == 'Delete':
                continue

            UI_ChatInfo.scroll_in_view(list, item)

            # get image
            button = item.children()[0].children()[0].children()[1]
            img = button.capture_as_image()
            members.append({'name':name, 'img':img})
            # n = len(members)
            # if n > 20:
            #     break
        return members

    def get_announcement(pwin):
        p = pwin.window(title='Group Notice', control_type='Text').parent()
        pane = p.children(control_type='Pane')[0]
        text = pane.children(control_type='Text')[0].window_text()
        return text

    def get_group_name(pwin):
        # print(pwin.print_control_identifiers())
        # child_window(title="Group Name", control_type="Text")
        p = pwin.child_window(title='Group Name', control_type='Text').parent()
        pane = p.children(control_type='Pane')[0]
        text = pane.children(control_type='Text')[0].window_text()
        return text
'''
Dialog - 'Chat Info'    (L957, T27, R1207, B719)
child_window(title="Chat Info", control_type="Window")
   |    |    |    |    |    |    |    | child_window(title="Search by group member", control_type="Edit")
   |    |    |    |    |    |    | child_window(title="Members", control_type="List")
   |    |    |    |    |    |    |    | child_window(title="Add", control_type="ListItem")
   |    |    |    |    |    |    |    |    |    | child_window(title="Add", control_type="Button")
   |    |    |    |    |    |    |    | child_window(title="競芬姐", control_type="ListItem")
   |    |    |    |    |    |    |    |    |    |    | child_window(title="競芬姐", control_type="Button")
   |    |    |    |    |    |    |    |    |    | child_window(title="競芬姐", control_type="Button")
......
   |    |    |    |    |    |    | child_window(title="View More Members", control_type="Button")
   |    |    |    |    |    |    |    |    | child_window(title="Group Name", control_type="Text")
   |    |    |    |    |    |    |    |    |    | child_window(title="【BRI】1️⃣全球公益讲座Dr.Jiang", control_type="Text")
   |    |    |    |    |    |    |    |    |    | child_window(title="Group Name", control_type="Button")
   |    |    |    |    |    |    |    |    | child_window(title="Remark", control_type="Text")
   |    |    |    |    |    |    |    |    |    | child_window(title="The name is only visible to you.", control_type="Button")
   |    |    |    |    |    |    |    |    | child_window(title="Group Notice", control_type="Text")
   |    |    |    |    |    |    |    |    |    | child_window(title="【一条免责、两条群规、三个尊重】：\n\n眾朋友，BRI 及所有讲者均享有...
   |    |    |    |    |    |    |    |    |    | child_window(title="Group Notice", control_type="Button")
   |    |    |    |    |    |    |    |    | child_window(title="My Alias in Group", control_type="Text")
   |    |    |    |    |    |    |    |    |    | child_window(title="刘维平", control_type="Button")
   |    |    |    |    |    |    |    |    | child_window(title="On-Screen Names", control_type="Text")
   |    |    |    |    |    |    |    |    | child_window(title="On-Screen Names", control_type="CheckBox")
   |    |    |    |    |    |    |    |    | child_window(title="Mute Notifications", control_type="Text")
   |    |    |    |    |    |    |    |    | child_window(title="Mute Notifications", control_type="CheckBox")
   |    |    |    |    |    |    |    |    | child_window(title="Sticky on Top", control_type="Text")
   |    |    |    |    |    |    |    |    | child_window(title="Sticky on Top", control_type="CheckBox")
   |    |    |    |    |    |    |    |    | child_window(title="Save to Contacts", control_type="Text")
   |    |    |    |    |    |    |    |    | child_window(title="Save to Contacts", control_type="CheckBox")
   |    |    |    |    |    |    | child_window(title="Delete and Leave", control_type="Button")
'''
