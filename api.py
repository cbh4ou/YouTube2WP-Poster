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


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "OTHER.json"

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
    
    print(json.dumps(response, indent=4))

    for item in response['items']:
        print(item['snippet']['title'])
if __name__ == "__main__":
    main()