#coding: utf-8

import argparse
import operator
import re
import sys
import time
import urlparse
import fhp.api.five_hundred_px as _fh
import fhp.helpers.authentication as _a
from fhp.models.user import User
from fhp.models.photo import Photo

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
    def _g(users):
        f = []
        for u in users:
            try:f.append([u, u.photos[0].created_at])
            except IndexError: f.append([u, "???"])
        return f
    return sorted(_g(user.friends), reverse=True, key=operator.itemgetter(1))

def _get_sorted_data (user): # like get_sorted_data but slower :-(
    return sorted([(u, get_last_upload_photo(u).created_at) for u in user.friends],
                  reverse=True, key=operator.itemgetter(1))

def format_info_html (data):
    yield _HTML_BEGIN
    for user, date in data:
        yield '<a href="%s">%s</a> (%s)<p>' % (
            urlparse.urljoin(_URL, user.username), user.fullname.strip(), date)
            #time.strftime('%Y-%m-%d %H:%M:%S', get_time(date))) #DEBUG
    yield _HTML_END

def format_info_txt (data):
    for user, date in data:
        yield '%s (%s, %s)' % (
            urlparse.urljoin(_URL, user.username), user.fullname.strip(), date)
            #time.strftime('%Y-%m-%d %H:%M:%S', get_time(date))) #DEBUG

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

def friends_update(user):
    sorted_uploads = list(get_sorted_data(user))
    print_info(sorted_uploads)

def show_stat(user):
    #friends = {}
    for friend in user.friends:
        print friend.fullname, friend.username, friend.id,
        likes = 0
        favs = 0
        for count, photo in enumerate(friend.photos):
            print photo.__dict__
            if photo.voted: #XX+TODO: must use auth...
                likes += 1
            if photo.favorited:
                favs += 1
        print "- %d photos (%d fav, %d like)" % (count, favs, likes)
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('username')
    parser.add_argument('-s', '--friends-stats',
        dest='stat', action='store_true', help='show following stats')
    _a.VERIFY_URL = "http://verify-oauth.herokuapp.com/"
    args = parser.parse_args()
    _f = _fh.FiveHundredPx(_a.get_consumer_key(),
                           _a.get_consumer_secret(),
                           _a.get_verify_url())
    username = args.username.decode('utf-8')
    me = User(username=username, authorize=True)
    if args.stat:
        show_stat(me)
    else:
        friends_update(me)

