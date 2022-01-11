#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
import sys, os
import yaml
from helper.my_logging import *
from ui.comm import UI_Comm
from settings.settings import Settings
from actions.report_group_info import Action_ReportGroupInfo
from actions.welcome_new_member import Action_WelcomeNewMember
from actions.remove_member import Action_RemoveMember
from actions.send_file import Action_SendFile
from actions.invite_friends import Action_InviteFriends
from actions.list_group_members import Action_ListGroupMembers
from actions.list_contacts import Action_ListContacts
from actions.invite_join_group import Action_InviteJoinGroup
from actions.forward_msg import Action_ForwardMsg
from actions.merge_group_members import Action_MergeGroupMembers
from actions.get_last_msg import Action_GetLastMsg
from actions.find_same_member import Action_FindSameMember
import pywinauto

def main(setting_file):
    logger.info('Using pywinauto version: %s', pywinauto.__version__)
    logger.info('settings from: %s', setting_file)
    settings = Settings.get_yaml(setting_file)
    if settings == None:
        logger.error('error in setting file %s', setting_file)
        return

    win = UI_Comm.connect_wechat()
    if win == None:
        return

    # raise window on top
    win.set_focus()

    # pywinauto.timings.Timings.fast()
    # pywinauto.timings.Timings.window_find_timeout = 0.2

    # before doing any action, make sure there is no sub-windows in open,
    # and any special input method not active (cause input problem)

    actions = settings['actions']
    if 'report_group_info' in actions:
        Action_ReportGroupInfo.report_group_info(win, actions['report_group_info'])
    if 'welcome_new_member' in actions:
        Action_WelcomeNewMember.welcome_new_member(win, actions['welcome_new_member'])
    if 'remove_member' in actions:
        Action_RemoveMember.remove_member(win, actions['remove_member'])
    if 'send_file' in actions:
        Action_SendFile.send_file(win, actions['send_file'])
    if 'invite_friends' in actions:
        Action_InviteFriends.invite_friends(win, actions['invite_friends'])
    if 'list_group_members' in actions:
        Action_ListGroupMembers.list_group_members(win, actions['list_group_members'])
    if 'list_contacts' in actions:
        Action_ListContacts.list_contacts(win, actions['list_contacts'])
    if 'invite_join_group' in actions:
        Action_InviteJoinGroup.invite_join_group(win, actions['invite_join_group'])
    if 'forward_msg' in actions:
        Action_ForwardMsg.forward_msg(win, actions['forward_msg'])
    if 'merge_group_members' in actions:
        Action_MergeGroupMembers.merge_group_members(win, actions['merge_group_members'])
    if 'get_last_msg' in actions:
        Action_GetLastMsg.get_last_msg(win, actions['get_last_msg'])
    if 'find_same_member' in actions:
        Action_FindSameMember.find_same_member(win, actions['find_same_member'])

    logger.info('no more actions')
    # update_history()
    # accept_new_friends(win)

if __name__ == '__main__':
    if sys.argv[1] == None:
        logger.warning('need setting file')
    else:
        setting_file = os.path.abspath(sys.argv[1])
        logger = getMyLogger(__name__, setting_file)
        if os.path.exists(setting_file):
            main(setting_file)
