import urllib.request
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import os
from wordpress_xmlrpc import Client, WordPressPost

class Custom_WP_XMLRPC:
    def post_article(self, wpUrl, wpUserName, wpPassword, articleTitle, articleCategories, articleContent, articleTags, PhotoUrl, excerptContent):


        self.path = os.path.dirname(os.path.abspath(__file__)) + "/YTimg.jpg"
        self.articlePhotoUrl = PhotoUrl
        self.wpUrl = wpUrl
        self.wpUserName = wpUserName
        self.wpPassword = wpPassword
        self.excerptContent=excerptContent

        print(excerptContent)
        # Download File
        f = open(self.path, 'wb')
        f.write(urllib.request.urlopen(self.articlePhotoUrl).read())
        f.close()
        # Upload to WordPress
        client = Client(self.wpUrl, self.wpUserName, self.wpPassword)
        filename = self.path
        # prepare metadata
        data = {'name': 'picture.jpg', 'type': 'image/jpg', }

        # read the binary file and let the XMLRPC library encode it into base64
        with open(filename, 'rb') as img:
                data['bits'] = xmlrpc_client.Binary(img.read())
        response = client.call(media.UploadFile(data))
        attachment_id = response['id']
        # Post
        post = WordPressPost()
        post.title = articleTitle
        post.content = articleContent
        post.terms_names = {'post_tag': articleTags,
                            'category': articleCategories}
        post.post_status = 'publish'
        post.thumbnail = attachment_id
        post.excerpt = excerptContent
        post.id = client.call(posts.NewPost(post))
        print('Post Successfully posted. Its Id is: ', post.id)


"""
#########################################
# POST & Wp Credentials Detail #
#########################################

#Url of Image on the internet
ariclePhotoUrl='https://upload.wikimedia.org/wikipedia/commons/a/a7/Action_photo_of_nasal_spray_on_a_black_background.jpg'
# Dont forget the /xmlrpc.php cause thats your posting adress for XML Server
wpUrl='https://economiccrisisreport.com/xmlrpc.php'
#WordPress Username
wpUserName='admin'
#WordPress Password
wpPassword='dw$jhqd*aWOlFwl1T5XUMlM3'
#Post Title
articleTitle='Testing Python Script version 3'
#Post Body/Description
articleContent='Final .... Testing Fully Automated'
#list of tags
articleTags=['code','python']
#list of Categories
articleCategories=['language','art']

#########################################
# Creating Class object & calling the xml rpc custom post Function
#########################################
xmlrpc_object	=	Custom_WP_XMLRPC()
#On Post submission this function will print the post id
xmlrpc_object.post_article(wpUrl,wpUserName,wpPassword,articleTitle, articleCategories, articleContent, articleTags,ariclePhotoUrl)
"""
