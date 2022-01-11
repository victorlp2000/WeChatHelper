#
# Written By:   Weiping Liu
# Created:      Jul 15, 2021
#
import pywinauto
import datetime, time
from helper.my_logging import *
from helper.utils import Utils
from settings.settings import Settings
from ui.chats import UI_Chats
from ui.chat_info import UI_ChatInfo
from ui.comm import UI_Comm
from ui.user import UI_User
from member_info import Members

logger = getMyLogger(__name__)

class Action_ListGroupMembers:
    def list_group_members(win, settings):
        logger.info('action: "list_group_members"')
        groups = settings['groups']
        save = settings['save']

        for group in groups:
            folder = save + group['name'] + '\\'
            os.makedirs(folder, exist_ok=True)
            members = Action_ListGroupMembers.list_members(win, group)
            meta = []
            for m in members:
                imgfile = group['id'] + '_' + str(members.index(m)+1) + '.png'
                m['img'].save(folder + imgfile, format='png')
                meta.append({'name':m['name'], 'img':imgfile})
            filename = folder + group['id'] + '.json'
            Utils.to_json_file(meta, filename)

    def list_members(win, group):
        if UI_Chats.chat_to(win, {'name':group['name']}) != True:
            return None
        # open 'chat info' window
        pwin = UI_ChatInfo.open_chat_info(win)
        if pwin == None:
            return None

        members = UI_ChatInfo.get_members_fast(pwin, win, ['*'])

        UI_ChatInfo.close_chat_info(win)
        return members
