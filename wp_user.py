import base64
import http.client
from extensions import db
from urllib.parse import urlencode, urlparse
from models import Websites, Channels
import json
import urllib.request

def update_user(website, uid, username):
    getpass = db.session.query(Websites).filter(Websites.website == website).first()
    auth = 'admin1:%s' % getpass.password
    token = base64.b64encode(auth.encode('utf-8')).decode("utf-8")
    conn = http.client.HTTPSConnection(website)
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
    #print(data.decode("utf-8"))


def create_user(username, website):
    getpass = db.session.query(Websites).filter(Websites.website == website).first()
    db.session.close()
    auth = 'admin1:%s' % getpass.password
    token = base64.b64encode(auth.encode('utf-8')).decode("utf-8")

    print('Creating user')


    conn = http.client.HTTPSConnection(website)
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
    #print(data.decode("utf-8"))



def create_category(username, website, category):

    getpass = db.session.query(Websites).filter(Websites.website == website).first()
    db.session.close()
    auth = 'admin1:%s' % getpass.password
    token = base64.b64encode(auth.encode('utf-8')).decode("utf-8")

    print('Creating Category')


    conn = http.client.HTTPSConnection(website)
    payload = {
        'name': category
    }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic %s' % token
    }
    conn.request("POST", "/wp-json/wp/v2/categories", urlencode(payload), headers)
    res = conn.getresponse()
    data = res.read()
    #print(data)


def delete_channel(username):
    result = db.session.query(Channels).filter(Channels.channel_name == username).first()
    db.session.delete(result)
    db.session.commit()
    db.session.close()

def get_user(website, username):
    getpass = db.session.query(Websites).filter(Websites.website == website).first()
    auth = 'admin1:%s' % getpass.password
    token = base64.b64encode(auth.encode('utf-8')).decode("utf-8")
    conn = http.client.HTTPSConnection(website)
    db.session.commit()
    db.session.close()
    payload = {

        }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic %s' % token
    }
    conn.request("GET",  '/wp-json/wp/v2/users?per_page=100', urlencode(payload),  headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)

    for x in data:
        if x['name'] == username:
            print("ID Recieved")
            return( x['id'])

def user_post(website, uid, title, category, content, tags, photo, description):


    getpass = db.session.query(Websites).filter(Websites.website == website).first()
    show_img(photo)
    media_id = create_media(getpass.website)
    auth = 'admin1:%s' % getpass.password
    token = base64.b64encode(auth.encode('utf-8')).decode("utf-8")
    conn = http.client.HTTPSConnection(website)
    db.session.commit()
    db.session.close()
    payload = {
        'author': uid,
        'title' : title,
        'content' : content,
        'categories' : category,
        'excerpt': description,
        'status': 'publish',
        'featured_media': media_id
        }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic %s' % token
    }
    conn.request("POST", "/wp-json/wp/v2/posts", urlencode(payload),  headers)
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data)
    print('Article Posted')

def get_category(website, category):
    getpass = db.session.query(Websites).filter(Websites.website == website).first()
    db.session.close()
    auth = 'admin1:%s' % getpass.password
    token = base64.b64encode(auth.encode('utf-8')).decode("utf-8")
    conn = http.client.HTTPSConnection(website)
    payload = {

        }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic %s' % token
    }
    conn.request("GET",  '/wp-json/wp/v2/categories?per_page=50', urlencode(payload),  headers)
    res = conn.getresponse()
    data = res.read()
    try:
        data = json.loads(data)
    except:
        print('category failed')

    for x in data:
        if x['name'] == category:
            print("Category Recieved")
            return( x['id'])

def create(url):
    url = urlparse(url)
    user_query = db.session.query(Channels).all()
    websites = db.session.query(Websites).filter(Websites.website == 'christianconservativedaily.com').all()
    for website in websites:
        for user in user_query:
            create_user(user.username, website.website)
            create_category(user.username, website.website, user.category)

def create_media(website):
    getpass = db.session.query(Websites).filter(Websites.website == website).first()
    db.session.close()
    auth = 'admin1:%s' % getpass.password
    token = base64.b64encode(auth.encode('utf-8')).decode("utf-8")

    print('Uploading Media')

    imgBytes = open('temp.jpg','rb').read()
    imgeFilename = 'temp.jpg'
    conn = http.client.HTTPSConnection(getpass.website)
    payload = imgBytes
    headers = {
      'Content-Disposition': 'attachment; filename=%s' % imgeFilename ,
      'Authorization': 'Basic %s' % token,
      'Content-Type': 'image/jpeg'
    }
    conn.request("POST", "/wp-json/wp/v2/media", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)
    details = json.loads(data)
    media_id = details['id']
    print(media_id)
    return media_id




def show_img(photo):
    URL = photo
    with urllib.request.urlopen(URL) as url:
        with open('temp.jpg', 'wb') as f:
            f.write(url.read())


#create_media('familysurvivalheadlines.com')

