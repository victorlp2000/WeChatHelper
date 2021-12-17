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
    群成员合并
'''
class Action_MergeGroupMembers:
    def merge_group_members(win, settings):
        logger.info('action: "merge_group_members"')

        folder = settings['folder']

        save_to = settings['save_to']

        members = []

        include = settings['include_groups']
        for name in include:
            data = Utils.from_json_file(folder+name+'.json')
            members = Action_MergeGroupMembers.insert_members(members, data['members'])

        exclude = settings['exclude_groups']
        for name in exclude:
            data = Utils.from_json_file(folder+name+'.json')
            if data == None:
                print(name)
            members = Action_MergeGroupMembers.remove_members(members, data['members'])

        data = {
           "group_name": save_to,
           "time": Utils.get_time_now(),
           "size": len(members),
           "include": include,
           "exclude": exclude,
           "members": members
        }
        Utils.to_json_file(data, folder+save_to+'.json')

    def exist_member(members, member):
        if 'WeChatID' not in member:
            return None
        for m in members:
            if m['name'] == member['name'] and m['WeChatID'] == member['WeChatID']:
                return m
        return None

    def insert_members(members, group_members):
        if len(members) == 0:
            new_members = group_members.copy()
            return new_members

        new_member = members.copy()
        for m in group_members:
            if not Action_MergeGroupMembers.exist_member(new_members, m):
                new_members.append(m)
        return new_members

    def remove_members(members, group_members):
        new_members = members.copy()
        for m in group_members:
            element = Action_MergeGroupMembers.exist_member(new_members, m)
            if element != None:
                new_members.remove(element)
        return new_members
