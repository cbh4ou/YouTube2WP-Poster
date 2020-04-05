# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json
import googleapiclient.discovery
import googleapiclient.errors
from datetime import datetime
from wp_post import Custom_WP_XMLRPC
from appdb import db
from models import Channels
from user_test import update_user, create_user




scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

def process_videos():
    channels = db.session.query(Channels).filter().all()
    for x in channels:
        upload_date=[]
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"

        # Get credentials and create an API client
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey='AIzaSyDkgxY7colARIhKWa3Ke0uHFZfgH8w9fEs')
        print(x.channel_name)
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            forUsername=x.channel_name
        )
        response = request.execute()


        upload_list = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        x.playlist_id = upload_list
        db.session.commit()
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
            new = item['snippet']['publishedAt'][:19]
            new_post_date = datetime.strptime(new, '%Y-%m-%dT%H:%M:%S')
            upload_date.append(new_post_date)

            if new_post_date > old:
                print(x.time_created)
                print(old)
                print(new_post_date)
                #print(item['snippet']['title'])
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
                #print(embed)

                content = '''
                The following video is brought to you courtesy of the {0} YouTube Channel. Click the video below to watch it now.

                {1}

                <a href="{2}" target="_blank"><img style="float: right; display: inline" src="{3}" width="144" align="right" height="108"></a>{4}"
                '''.format(channel_name, embed, thumbnail_hq, thumbnail_default, description)

                for website in ['https://americanboomerdaily.com/postmaker.php']:
                    ariclePhotoUrl=thumbnail_default
                    # Dont forget the /xmlrpc.php cause thats your posting adress for XML Server
                    wpUrl=website
                    #WordPress Username
                    wpUserName=x.username
                    #WordPress Password
                    wpPassword=x.password
                    #Post Title
                    articleTitle= title
                    #Post Body/Description
                    articleContent= content
                    #list of tags
                    articleTags=[]
                    #list of Categories
                    articleCategories=[]

                    xmlrpc_object	=	Custom_WP_XMLRPC()
                    #On Post submission this function will print the post id
                    i = 2
                    while True:
                        try:
                            print(x.username)
                            print(website)
                            xmlrpc_object.post_article(wpUrl,wpUserName,wpPassword,articleTitle, articleCategories, articleContent, articleTags,ariclePhotoUrl, description)
                            break
                        except Exception as ex:
                            print(ex)
                            wpPassword = update_user(website, i, wpUserName)
                            create_user(wpUserName, website)
                            i = i+1
                            continue
                    #print(content)
                    #print(json.dumps(data, indent=4))
        x.time_created = max(upload_date)
        db.session.commit()
process_videos()
