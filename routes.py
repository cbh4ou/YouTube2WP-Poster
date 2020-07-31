    # A very simple Flask Hello World app for you to get started with...
from flask import Blueprint, request, jsonify
from extensions import db
from models import Channels, Websites
from str2bool import str2bool
from wp_user import delete_channel, create_user, create_category
from urllib.parse import  urlparse

channels = Blueprint('channels', __name__,
                    template_folder='assets/templates',
                    static_folder='assets')


@channels.route('/channels/names', methods=['GET', 'POST'])
def get_channels():
    if request.method == "GET":
        channel_query = db.session.query(Channels).all()
        dropdown_object = []
        num = 0
        for i in channel_query:
            num=num+1
            dropdown_object.append(notif_item(num, i.channel_name).__dict__)

        return jsonify(dropdown_object)
    else:
        resp = request.get_json()
        channel_query = db.session.query(Channels).filter(Channels.channel_name == resp['channel']).first()
        return jsonify({'category': channel_query.category, 'hasID': channel_query.channel_id, 'channel_id': channel_query.youtube_id})


@channels.route('/channels/update', methods=['POST'])
def update_channels():
    if request.method == "POST":
        resp = request.get_json()
        channel_query = db.session.query(Channels).filter(Channels.channel_name == resp['channelName']).first()
        if channel_query == None:
            new_channel = Channels(channel_name = resp['channelName'], username = resp['channelName'],  category = resp['category'],
            channel_id = str2bool(resp['hasID'].lower()), youtube_id = resp['youtubeID'], password = 'IEOo s0hV 4R0h lZex I5uq bw7v', time_created = '2020-04-08 21:00:28')
            db.session.add(new_channel)
            db.session.commit()
            websites = db.session.query(Websites).all()
            for x in websites:
                create_user(resp['channelName'], x.website)
                create_category(resp['channelName'], x.website, resp['category'])
            return 'None', 200
        else:
            channel_query.category = resp['category']
            channel_query.youtube_id = resp['youtubeID']
            db.session.commit()
            return 'Success', 200


@channels.route('/channels/delete', methods=['POST'])
def delete_channels():
    if request.method == "POST":
        resp = request.get_json()
        delete_channel(resp['channelName'])
        return 'Channel Deleted', 200
    else:
        return 'Success', 200

@channels.route('/websites/names', methods=['GET'])
def get_websites():
    if request.method == "GET":
        channel_query = db.session.query(Websites).all()
        dropdown_object = []
        num = 0
        for i in channel_query:
            num=num+1
            dropdown_object.append(notif_item(num, i.website).__dict__)

        return jsonify(dropdown_object)
    else:
        resp = request.get_json()
        new_website = Websites(website = resp['website'].lower(), password = resp['password'])
        db.session.add(new_website)
        db.session.commit()

@channels.route('/websites/update', methods=['GET','POST'])
def update_websites():
    if request.method == "GET":
        pass
    else:
        resp = request.get_json()
        url = urlparse(resp['website'].lower())

        website_query = db.session.query(Websites).filter(Websites.website == url.netloc).first()
        if website_query == None:

            new_website = Websites(website = url.netloc, password = resp['password'])
            db.session.add(new_website)
            db.session.commit()
            user_query = db.session.query(Channels).all()
            for user in user_query:
                create_user(user.username, url.netloc)
                create_category('default', url.netloc, user.category )
            return 'Success'
        else:
            website_query.website = url.netloc
            website_query.password = resp['password']
            return 'Success'

class notif_item():

    def __init__(self, row, name):
        self.id = row
        self.name = name