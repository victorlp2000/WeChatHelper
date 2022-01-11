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
from PIL import Image
import imagehash

logger = getMyLogger(__name__)

class Action_FindSameMember:
    def find_same_member(win, settings):
        logger.info('action: "find_same_member"')

        folder = settings['folder']

        list_groups = settings['list_groups']

        check_groups = settings['check_groups']

        # read-in all meta data
        list_data = []
        for group in list_groups:
            pdir = folder + group['name'] + '\\'
            meta = Utils.from_json_file(pdir + group['id'] + '.json')
            logger.info('%s: %d', group['name'], len(meta))
            members = []
            index = 0
            for member in meta:
                index += 1
                # if index > 3:
                #     break
                img = Image.open(pdir + member['img'])
                hash = imagehash.average_hash(img, hash_size=16)
                # print(member['name'], hash)
                members.append({'name':member['name'],
                                'img':member['img'],
                                'hash':hash})
            list_data.append({'folder':folder, 'name':group['name'], 'id':group['id'], 'members':members})

        check_data = []
        for group in check_groups:
            pdir = folder + group['name'] + '\\'
            meta = Utils.from_json_file(pdir + group['id'] +'.json')
            logger.info('%s: %d', group['name'], len(meta))
            members = []
            index = 0
            for member in meta:
                index += 1
                # if index > 3:
                #     break
                img = Image.open(pdir + member['img'])
                hash = imagehash.average_hash(img, hash_size=16)
                # if member['img'] == 'bri_15_10.png':
                #     print('bri_15_10', hash)
                # print(member['name'], hash)
                members.append({'name':member['name'],
                                'img':member['img'],
                                'hash':hash})
            check_data.append({'folder':folder, 'name':group['name'], 'id':group['id'], 'members':members})

        for group in check_data:
            f = open(group['folder'] + group['id'] + '.html', 'w', encoding='utf8')
            html = Action_FindSameMember.check_members(group, list_data)
            f.write(html)
            f.close()

    # members = [{name:.., img:..., hash:...}, ]
    # list_data = [
    #   [{name:..., img:..., hash:...}, ]
    #   [{name:..., img:..., hash:...}, ]
    # ]
    def check_members(check_group, list_groups):
        html = ''
        index = 0
        for m0 in check_group['members']:
            # m0  a member to be checked
            # 忽略特殊图片　－空头像
            if str(m0['hash']) == 'fffffffffffffffffe7ffc3ffc3ffc3ffe3ff81ff00ff00fffffffffffffffff':
                continue

            in_groups = []
            for group in list_groups:
                for m1 in group['members']:
                    distance = m0['hash'] - m1['hash']
                    if distance == 0:
                        if len(in_groups) == 0:
                            in_groups.append({'group_name':check_group['name'], 'group_id':group['id'], 'img':m0['img'], 'id':m0['name']})
                        in_groups.append({'group_name':group['name'], 'group_id':group['id'], 'img':m1['img'], 'id':m1['name']})
                        break
            # logger.info('%s: %s', m0['name'], in_groups)
            if len(in_groups) > 0:
                index += 1
                ids = ''
                for i in in_groups:
                    ids += i['group_id'] + ', '
                logger.info('%d "%s" [%s]', index, m0['name'], str(len(in_groups)))
                html += '<div style="display:table-row;"><div style="display:table-cell;">' + str(index) + ' ' + m0['name'] + ':</div>'
                for cell in in_groups:
                    html += '<div style="display:table-cell"><img src="' + cell['group_name'] + '/' + cell['img'] + '" /><br>' + cell['img'][:cell['img'].rindex('_')] + '<br>' + cell['id'] + '</div>'
                html += '</div>\n'
        return html
