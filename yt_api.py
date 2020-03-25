# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import sys
from datetime import datetime
from wp_post import Custom_WP_XMLRPC

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey='AIzaSyDkgxY7colARIhKWa3Ke0uHFZfgH8w9fEs')

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        forUsername="FoxBusinessNetwork"
    )
    response = request.execute()

    upload_list = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        maxResults=10,
        playlistId=upload_list
    )

    response = request.execute()
    
    #print(json.dumps(response, indent=4))

    for item in response['items']:
        last_post_date = datetime.strptime('2020-03-24T19:36:53.000Z', '%Y-%m-%dT%H:%M:%S.%fZ')
        new_post_date = datetime.strptime(item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')

        if new_post_date > last_post_date:

            print(item['snippet']['title'])
            request = youtube.videos().list(
            part="snippet,contentDetails,statistics, player",
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

            ariclePhotoUrl='https://upload.wikimedia.org/wikipedia/commons/a/a7/Action_photo_of_nasal_spray_on_a_black_background.jpg' 
            # Dont forget the /xmlrpc.php cause thats your posting adress for XML Server
            wpUrl='https://economiccrisisreport.com/xmlrpc.php' 
            #WordPress Username
            wpUserName='admin'
            #WordPress Password
            wpPassword='dw$jhqd*aWOlFwl1T5XUMlM3'
            #Post Title
            articleTitle= title
            #Post Body/Description
            articleContent= content
            #list of tags
            articleTags=['code','python'] 
            #list of Categories
            articleCategories=['language','art'] 

            xmlrpc_object	=	Custom_WP_XMLRPC()
            #On Post submission this function will print the post id
            xmlrpc_object.post_article(wpUrl,wpUserName,wpPassword,articleTitle, articleCategories, articleContent, articleTags,ariclePhotoUrl)
            print(content)
            print(json.dumps(data, indent=4))



if __name__ == "__main__":
    main()