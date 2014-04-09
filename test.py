#coding: utf-8

import operator
import re
import sys
import time
import urlparse
import fhp.api.five_hundred_px as _fh
import fhp.helpers.authentication as _a
from fhp.models.user import User

_TREG = re.compile('^(\d+)-(\d+)-(\d+).*?(\d+):(\d+):(\d+).*')
_URL = 'http://500px.com/'
_HTML_BEGIN = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
 "http://www.w3.org/TR/html4/strict.dtd">
<HTML>
<HEAD>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<TITLE>following last updates</TITLE>
</HEAD>
<BODY>
'''
_HTML_END = '''</BODY>
</HTML>'''
FMT_TEXT = 'txt'
FMT_HTML = 'html'

def get_time (s):
    return time.strptime(' '.join(_TREG.match(s).groups()),
                         '%Y %m %d %H %M %S')

def get_last_upload_photo (user):
    return sorted(user.photos,
                  reverse=True, key=lambda p: get_time(p.created_at))[0]

def get_sorted_data (user):
    return sorted([(u, u.photos[0].created_at) for u in user.friends],
                  reverse=True, key=operator.itemgetter(1))

def _get_sorted_data (user): # like get_sorted_data but slower :-D
    return sorted([(u, get_last_upload_photo(u).created_at) for u in user.friends],
                  reverse=True, key=operator.itemgetter(1))

def format_info_html (data):
    yield _HTML_BEGIN
    for user, date in data:
        yield '<a href="%s">%s</a> (%s)<p>' % (
            urlparse.urljoin(_URL, user.username), user.fullname.strip(), date)
            #time.strftime('%Y-%m-%d %H:%M:%S', get_time(date))) # last for debug only
    yield _HTML_END

def format_info_txt (data):
    for user, date in data:
        yield '%s (%s, %s)' % (
            urlparse.urljoin(_URL, user.username), user.fullname.strip(), date)
            #time.strftime('%Y-%m-%d %H:%M:%S', get_time(date))) # last for debug only

def print_info(data, fmt=FMT_HTML):
    if fmt == FMT_HTML:
        func = format_info_html
    elif fmt == FMT_TEXT:
        func = format_info_txt
    else:
        raise ValueError("unknown format <%s>" % fmt)
    for out in func(data):
        try:
            print out
        except UnicodeEncodeError:
            print out.encode('utf-8', 'replace')


if __name__ == '__main__':
    _f = _fh.FiveHundredPx(_a.get_consumer_key(),
                           _a.get_consumer_secret(),
                           _a.get_verify_url())
    username = sys.argv[1].decode('utf-8')
    me = User(username=username)
    sorted_uploads = get_sorted_data(me)
    print_info(sorted_uploads)
        

##############################################
sys.exit()
if 0:
    __t = []
    #class
    for i in range(10):
        __t.append(time.localtime())
        sleep(1)
    
    me.friends = 8



"""
print type(me), dir(me), me.id
print "------"
print type(f), dir(f)

for i in me.friends:
    print i.fullname, i.username, i.id, i.domain, dir(i)
    break

if 0:
    for p in sorted((x.created_at for x in i.photos), reverse=True, key=lambda s:get_time(s)):
        print p
        break
    break
    for p in i.photos:
        print p, p.created_at, p.id
    break

print list(f.get_user_friends(username))
print type(me), len(me)
print dir(f)
"""
