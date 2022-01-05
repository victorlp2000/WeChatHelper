#
# Written By:   Weiping Liu
# Created:      Jun 28, 2021
#
import datetime, time, random
from helper.my_logging import *
from helper.utils import Utils
from settings.settings import Settings
from ui.chats import UI_Chats
from ui.chat_info import UI_ChatInfo
from ui.comm import UI_Comm
from ui.user import UI_User
from ui.wechat_pane import UI_WeChatPane
from ui.add_member import Dlg_AddMember
from member_info import Members, Cache

logger = getMyLogger(__name__)

'''
    转发: 从本人的聊天记录中选取最后一组内容，转发到指定的名单
'''
class Action_ForwardMsg:
    def forward_msg(win, settings):
        logger.info('action: "forward_msg"')

        folder = settings['folder']
        name = settings['member_group']
        category = settings['category']

        data = Utils.from_json_file(folder+name+'.json')
        contacts = data['members']

        UI_Chats.click_chats_button(win)

        index = 0
        while index < len(contacts):
            index1 = UI_Chats.forward_msgs(win, category, contacts, index)
            if index1 == index:
                logger.warning('stop forwarding')
                break
            index = index1
