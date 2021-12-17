#
# Written By:   Weiping Liu
# Created:      Jun 22, 2021
#
import datetime
import json, os
import imagehash
from helper.my_logging import *

logger = getMyLogger(__name__)

class Utils:
    # stime time string to be converted:
    #   '6:30 PM'
    #   '6-20-21 6:30 PM'
    #   'Yesterday 6:30 PM'
    #   'Monday 6:30 PM'
    # output format
    #   '2021-06-20 18:30'
    def format_time_tag(stime, warning=True):
        now = datetime.datetime.now()
        t = ''

        w = stime.split()
        ws = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Yesterday']
        if w[0] in ws:
            if w[0] == ws[7]:
                days = 1
            else:
                d0 = now.weekday()
                d1 = ws.index(w[0])
                days = d0 - d1
                if days < 0:
                    days += 7
            t = now - datetime.timedelta(days=days)
            t = t.strftime('%m-%d-%y') + stime[len(w[0]):]
        elif len(stime) <= 8:
            t = now.strftime('%m-%d-%y ') + stime
        else:
            t = stime
        try:
            tt = datetime.datetime.strptime(t, '%m-%d-%y %I:%M %p')
        except ValueError:
            if warning:
                logger.warning('wrong date-time string "%s"', stime)
            return None
        return tt.strftime('%Y-%m-%d %H:%M')

    def get_time_now():
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # write object to json file
    def to_json_file(obj, filename):
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        logger.info('write json to "%s"', filename)
        with open(filename, 'w', encoding='utf8') as jfile:
            json.dump(obj, jfile, indent=2, ensure_ascii=False)

    # read json file to object
    def from_json_file(filename):
        if os.path.exists(filename) == False:
            return None
        logger.info('read json from "%s"', filename)
        with open(filename, 'r', encoding='utf8') as jfile:
            obj = json.load(jfile)
            return obj

    def parse_keys(text):
        parsed = ''
        for c in text:
            if c == ' ':
                parsed += '{SPACE}'
            elif c in '(){}~+^%':
                parsed += '{' + c + '}'
            elif c == '\n':
                parsed += '^{ENTER}'
            else:
                parsed += c
        # logger.info('<%s><%s>', text, parsed)
        return parsed

    def get_img_key(img):
        key = imagehash.average_hash(img)
        return str(key)

if __name__ == '__main__':
    # print(Utils.format_time_tag('6-20-21 7:40 PM'))
    # print(Utils.format_time_tag('7:40 PM'))
    print(Utils.format_time_tag('Yesterday 7:40 PM'))
    print(Utils.format_time_tag('Sunday 7:40 PM'))
    print(Utils.format_time_tag('Monday 7:40 PM'))
    print(Utils.format_time_tag('Tuesday 7:40 PM'))
    print(Utils.format_time_tag('Wednesday 7:40 PM'))
    print(Utils.format_time_tag('Thursday 7:40 PM'))
    print(Utils.format_time_tag('Friday 7:40 PM'))
    print(Utils.format_time_tag('Saturday 7:40 PM'))
