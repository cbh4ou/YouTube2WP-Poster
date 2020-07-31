# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
from googleapiclient import discovery
from datetime import datetime
from models import Channels, Websites
from wp_user import update_user, create_user, create_category, get_user, user_post, get_category
from alerts import Twilio
from basemodel import db
from appdb import create_app
create_app()

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def process_videos():
    channels = Channels.query.filter().all()
    for x in channels:
        upload_date=[]
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        response = ''
        # Get credentials and create an API client
        if x.channel_id is False:
            youtube = discovery.build(
                api_service_name, api_version, developerKey='AIzaSyDkgxY7colARIhKWa3Ke0uHFZfgH8w9fEs')
            print(x.channel_name)
            request = youtube.channels().list(
                part="snippet,contentDetails,statistics",
                forUsername=x.channel_name
            )
            response = request.execute()
        else:
            youtube = discovery.build(
                "youtube", "v3", developerKey='AIzaSyDkgxY7colARIhKWa3Ke0uHFZfgH8w9fEs')
            print(x.channel_name)
            request = youtube.channels().list(
                part="snippet,contentDetails,statistics",
                id=str(x.youtube_id)
            )
            response = request.execute()
            #print(response)

        upload_list = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        x.playlist_id = upload_list
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=20,
            playlistId=upload_list
        )

        response = request.execute()


        #print(json.dumps(response, indent=4))

        for item in response['items']:
            old = x.time_created
            old = old.strftime('%Y-%m-%dT%H:%M:%S')
            old = datetime.strptime(old, '%Y-%m-%dT%H:%M:%S')
            upload_date.append(old)
            #print(old)
            new = item['snippet']['publishedAt'][:19]
            new_post_date = datetime.strptime(new, '%Y-%m-%dT%H:%M:%S')
            print(new_post_date)


            if new_post_date > min(upload_date):
                upload_date.append(new_post_date)
                Channels.query.filter(Channels.channel_name == x.channel_name).update({'time_created' : max(upload_date) }, synchronize_session = False)
                db.session.commit()
                db.session.close()
                print('POSTED' , new_post_date, item['snippet']['title'])
                request = youtube.videos().list(
                part="snippet,contentDetails,player",
                id=item['snippet']['resourceId']['videoId'],
                maxHeight=281,
                maxWidth=500
                )



                data = request.execute()
                embed = data['items'][0]['player']['embedHtml']
                title = data['items'][0]['snippet']['title']
                description = data['items'][0]['snippet']['description']
                channel_name = data['items'][0]['snippet']['channelTitle']
                thumbnail_default = data['items'][0]['snippet']['thumbnails']['default']['url']
                thumbnail_hq = data['items'][0]['snippet']['thumbnails']['high']['url']


                content = '''
                The following video is brought to you courtesy of the {0} YouTube Channel. Click the video below to watch it now.

                {1}

                <a href="{2}" target="_blank"><img style="float: right; display: inline" src="{3}" width="144" align="right" height="108"></a>{4}"
                '''.format(channel_name, embed, thumbnail_hq, thumbnail_default, description)
                websites = db.session.query(Websites).filter().all()

                for website in websites:

                    url = website.website
                    print(url)
                    ariclePhotoUrl=thumbnail_hq
                    # Dont forget the /xmlrpc.php cause thats your posting adress for XML Server
                    #WordPress Username
                    wpUserName=x.username
                    #WordPress Password
                    #Post Title
                    articleTitle= title
                    #Post Body/Description
                    articleContent= content
                    #list of tags
                    articleTags=[]
                    #list of Categories
                    articleCategories= str(get_category(url, x.category))


                    #On Post submission this function will print the post id
                    try:
                        create_category(wpUserName, url, articleCategories[0])
                        uid  = get_user(url, wpUserName)
                        user_post(url, uid, articleTitle, articleCategories, articleContent, articleTags,ariclePhotoUrl, description[0:150])
                    except Exception as ex:
                        create_user(wpUserName, url)
                        update_user(url, get_user(url, wpUserName) , wpUserName)
                        print('ERRRRRRROOOOOOOOOOOOORRRRRRRRRRRRRRRRRRRR')
                        print(ex)
                        alert_sms = Twilio(url, str(ex))
                        alert_sms.send_alert()
                        continue
                    #print(content)
                    #print(json.dumps(data, indent=4))
                db.session.close()
            print(x.channel_name, 'MAX    :' ,  max(upload_date))



process_videos()
