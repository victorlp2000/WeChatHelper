#
# Written By:   Weiping Liu
# Created:      Jun 28, 2021
#
import datetime, time
from helper.my_logging import *
from helper.utils import Utils
from settings.settings import Settings
from ui.contacts import UI_Contacts
from ui.manage_contacts import UI_ManageContacts
from ui.comm import UI_Comm
from ui.user import UI_User
from member_info import Members

logger = getMyLogger(__name__)

class Action_ListContacts:
    def list_contacts(win, settings):
        logger.info('action: "list_contacts"')

        types = {
            'groups': settings['groups'],
            'contacts': settings['contacts']
            }

        UI_Contacts.click_contacts_button(win)
        contacts = UI_Contacts.get_contacts(win, types)

        contacts_data = {
            'group_name': 'Contacts',
            'time': Utils.get_time_now(),
            'size': len(contacts['contacts']),
            'members': contacts['contacts']
            }
        groups_data = {
            'group_name': 'Saved Groups',
            'time': Utils.get_time_now(),
            'size': len(contacts['saved_groups']),
            'members': contacts['saved_groups']
            }
        if types['contacts']:
            filename = settings['save_to'] + 'contacts.json'
            Utils.to_json_file(contacts_data, filename)
            logger.info('number of contacts: %d', contacts_data['size'])

        if types['groups']:
            filename = settings['save_to'] + 'saved_groups.json'
            Utils.to_json_file(groups_data, filename)
            logger.info('number of groups: %d', groups_data['size'])
