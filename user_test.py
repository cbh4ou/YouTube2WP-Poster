import base64
import http.client
from urllib.parse import urlencode, urlparse
from models import Websites, Channels
from appdb import db


def update_user(website, uid, username):
    url = urlparse(website)
    print('Updating Password')
    website = db.session.query(Websites).filter(Websites.website == url.netloc).first()
    auth = 'admin1:%s' % website.password
    token = base64.b64encode(auth.encode('utf-8')).decode("utf-8")
    conn = http.client.HTTPSConnection(url.netloc)
    chan = db.session.query(Channels).filter(Channels.username == username).first()
    chan.password = 'IEOo s0hV 4R0h lZex I5uq bw7v'
    db.session.commit()
    payload = {'password' : 'IEOo s0hV 4R0h lZex I5uq bw7v'}
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic %s' % token
    }
    conn.request("POST", "/wp-json/wp/v2/users/%s" % uid, urlencode(payload), headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


def create_user(username, website):
    url = urlparse(website)
    website = db.session.query(Websites).filter(Websites.website == url.netloc).first()
    auth = 'admin1:%s' % website.password
    token = base64.b64encode(auth.encode('utf-8')).decode("utf-8")

    print('Creating user')


    conn = http.client.HTTPSConnection(url.netloc)
    payload = {
        'username' : username,
        'password' : 'IEOo s0hV 4R0h lZex I5uq bw7v',
        'email' : username.replace(" ", "") + '@youtubeposter.com',
        "capabilities": {
            "upload_files": True,
            "edit_posts": True,
            "edit_published_posts": True,
            "publish_posts": True,
            "read": True,
            "level_2": True,
            "level_1": True,
            "level_0": True,
            "delete_posts": True,
            "delete_published_posts": True,
            "author": True
        },
        "extra_capabilities": {
            "author": True
        }
    }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic %s' % token
    }
    conn.request("POST", "/wp-json/wp/v2/users", urlencode(payload), headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))


def create_category():
    pass



