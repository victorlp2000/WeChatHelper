#
# Written By:   Weiping Liu
# Created:      Nov 18, 2021
#
import time, os
from helper.my_logging import *
from ui.chats import UI_Chats
from settings.settings import Settings
from helper.utils import Utils

logger = getMyLogger(__name__)

class Action_GetLastMsg:
    def get_last_msg(win, settings):
        logger.info('action: "get last msg"')
        group = settings['member_group']
        folder = settings['folder']

        data = Utils.from_json_file(folder+group+'.json')
        members = data['members']

        UI_Chats.click_chats_button(win)

        blacked = []    # 被对方拉黑
        removed = []    # 删除
        for member in members:
            msg = UI_Chats.get_last_msg(win, member)
            # logger.info(msg)
            if msg == '消息已发出，但被对方拒收了。':
                blacked.append(member)
            if msg and ('开启了朋友验证' in msg):
                removed.append(member)
        print('blacked')
        print(blacked)
        print('removed')
        print(removed)
