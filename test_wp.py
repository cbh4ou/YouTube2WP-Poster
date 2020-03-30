from wordpress import API
import requests
import json
import base64
import http.client
import mimetypes

def main():
    
    
    """
    wpapi = API(
        url="https://economiccrisisreport.com",
        consumer_key="mIW6KEbwAjfV3aID8MN8xMpMFiwFtcQPVMWGr8c2",
        consumer_secret="rsXvDF8LsWUZJjLoBh45uUVqHR680jasM7XpN6bf",
        api="wp-json",
        version="wp/v2",
        wp_user="admin",
        wp_pass="dw$jhqd*aWOlFwl1T5XUMlM3",
        oauth1a_3leg=True,
        callback='/',
        creds_store="~/.wc-api-creds.json"
    )

    endpoint = "/wp/v2/users"
    wpapi.get(endpoint)
    """
    
    conn = http.client.HTTPSConnection("americanboomerdaily.com")
    payload = ''
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic YWRtaW46NVFubSBKY3I2IFdaQ3UgcllnViBSUU9aIDVpN1c='
    }
    conn.request("GET", "/wp-json/wp/v2/users/3", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    
    
main()