#-----------------------------------------------------------------------------------------------------------------------#
                                                    #INSTABOT#
#-----------------------------------------------------------------------------------------------------------------------#

#Required libraries imported  for developing the app

import requests
import urllib
from pprint import pprint
from colorama import Fore
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()

#-----------------------------------------------------------------------------------------------------------------------#
print "*******WELCOME TO INSTABOT*******"
#-----------------------------------------------------------------------------------------------------------------------#
#To get the Instagram API and Convert it into JSON forma

APP_ACCESS_TOKEN = response['access_token']
BASE_URL='https://api.instagram.com/v1/'


#-----------------------------------------------------------------------------------------------------------------------#
#Function For Own Information

def owner_info():
    r = requests.get('%susers/self/?access_token=%s' % (BASE_URL,APP_ACCESS_TOKEN)).json()

    if r['meta']['code'] == 200:

        print "Username : %s" % (r['data']['username'])
        print "User's followers : %s" % (r['data']['counts']['followed_by'])
        print "User's Bio : %s" % (r['data']['bio'])
        print "User Follows : %s" % (r['data']['counts']['follows'])
        print "Website : %s" % (r['data']['website'])
        print "User's id : %s" % (r['data']['id'])
        print "User's Full Name : %s" % (r['data']['full_name'])
        print "User's Profile Pic : %s" % (r['data']['profile_picture'])
        print "User's posts : %s" % (r['data']['counts']['media'])
    else:
        print "Status code recieved is other than 200"

#-----------------------------------------------------------------------------------------------------------------------#

def owner_post():
    r = requests.get('%susers/self/media/recent/?access_token=%s' % (BASE_URL, APP_ACCESS_TOKEN)).json()
    if r['meta']['code'] == 200:

        print r['data'][0]['images']['standard_resolution']['url']



    else:
        print "Status code other than 200 received."

#-----------------------------------------------------------------------------------------------------------------------#
#Function defines to get the user id
def get_user_id(uname):
    r = requests.get("%susers/search?q=%s&access_token=%s" % (BASE_URL, uname, APP_ACCESS_TOKEN)).json()

    if r['meta']['code'] == 200:  # HTTP 200 means transmission is OK
        if len(r['data']):  # Checking length using len() function
            return r['data'][0]['id']
        else:
            return None
    else:
        print "Status code other than 200 received!"


#-----------------------------------------------------------------------------------------------------------------------#
def user_info(uname):
    user_id = get_user_id(uname)
    if user_id is None:
        print "User does not exist!"
        exit()
    else:
        r = requests.get("%susers/%s?access_token=%s" % (BASE_URL, user_id, APP_ACCESS_TOKEN)).json()
        print "\nUser Info is :"
        if r['meta']['code'] == 200:
            if len(r['data']):
                # To display  the info of other user
                print 'User ID    :: %s' % (r['data']['id'])
                print 'Username   :: %s' % (r['data']['username'])
                print 'Full name  :: %s ' % (r['data']['full_name'])
                print 'Profile pic URL   :: %s' % (r['data']['profile_picture'])
                print 'No. of followers   :: %s' % (r['data']['counts']['followed_by'])
                print 'No. of  followings   :: %s' % (r['data']['counts']['follows'])
                print 'No. of posts   :: %s' % (r['data']['counts']['media'])
            else:
                print "No info. exists of this user!"
        else:
            print "Status code other than 200 received!"


#-----------------------------------------------------------------------------------------------------------------------#
#Function defines to get the othe user post info
def user_post(username):
    user_id = get_user_id(username)
    if user_id is None:
        print "User does not exist!"
        exit()
    else:
        r = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL, user_id, APP_ACCESS_TOKEN)).json()
        if r['meta']['code'] == 200:
            print r['data'][0]['images']['standard_resolution']['url']
        else:
            print "Status code other than 200 received!"

#-----------------------------------------------------------------------------------------------------------------------#
#Function defines to download the user's post
def dwnld_user_post(uname):
    user_id = get_user_id(uname)
    if user_id is None:
        print "User does not exist!"
        exit()
    else:
        post = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL, user_id, APP_ACCESS_TOKEN)).json()
        if post['meta']['code'] == 200:
            # To Check post exist or not
            if len(post['data']) > 0:
                if post['data'][1]['type'] == "image":
                    image_name = post['data'][1]['id'] + '.jpeg'
                    image_url = post['data'][1]['images']['standard_resolution']['url']
                    urllib.urlretrieve(image_url, image_name)
                    print "Image Successfully downloaded"
                elif post['data'][1]['type'] == "video":
                    video_name = post['data'][1]['id'] + '.mp4'
                    video_url = post['data'][1]['videos']['standard_resolution']['url']
                    urllib.urlretrieve(video_url, video_name)
                    print "Video successfully downloaded..."
                else:
                    print "No image  or video post to show..."
            else:
                print "Post does not  exist!"
        else:
            print "Status code other than 200 received!"


#-----------------------------------------------------------------------------------------------------------------------#
def get_media_id(uname):
    user_id = get_user_id(uname)
    if user_id is None:
        print "User does not exist!"
        exit()
    else:
        r = requests.get('%susers/%s/media/recent/?access_token=%s' % (BASE_URL, user_id, APP_ACCESS_TOKEN)).json()
        if r['meta']['code'] == 200:
            # To check post exist or not
            if len(r['data']) > 0:
                #Returns media id
                return r['data'][0]['id']
            else:
                print "Post does not exist!"
        else:
            print "Status code other than 200 received!"

#-----------------------------------------------------------------------------------------------------------------------#
#Function Defines to Like the user's post
def like_post(uname):
    media_id = get_media_id(uname)
    payload = {"access_token": APP_ACCESS_TOKEN}
    url = '%smedia/%s/likes' % (BASE_URL, media_id)
    r = requests.post(url, payload).json()
    if r['meta']['code'] == 200:
        print "Like Successful!"
    else:
        print "Like Unsuccessful...Try again!"

#-----------------------------------------------------------------------------------------------------------------------#
#Function defines to comment on the user's post
def comment_post(uname):
    media_id = get_media_id(uname)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text": comment_text}
    url = '%smedia/%s/comments' % (BASE_URL, media_id)
    r = requests.post(url, payload).json()
    if r['meta']['code'] == 200:
        print "Comment Successful!"
    else:
        print "Comment Unsuccessful... Try again!"

#-----------------------------------------------------------------------------------------------------------------------#
#Function defines to display the list of comments
def comment_list(uname):
    media_id = get_media_id(uname)
    request_url = ('%smedia/%s/comments/?access_token=%s' % (BASE_URL, media_id, APP_ACCESS_TOKEN))
    comment = requests.get(request_url).json()
    if comment['meta']['code'] == 200:
        if len(comment['data']):
            number_of_comments = 0
            print "The list of comments on the post are   :: \n"
            for index in range(0, len(comment['data'])):
                cmnt_text = comment['data'][index]['text']
                print (cmnt_text)
                number_of_comments = number_of_comments + 1
            print "Number of comments on the post are   :: " + str(number_of_comments)
        else:
            print "No comments found on the post!"
    else:
        print "Status code other than 200 received!"


#-----------------------------------------------------------------------------------------------------------------------#
#Function Defines to delete the negative comments on post
def del_comment(uname):
    media_id = get_media_id(uname)
    request_url = ('%smedia/%s/comments/?access_token=%s' % (BASE_URL, media_id, APP_ACCESS_TOKEN))
    r = requests.get(request_url).json()
    if r['meta']['code'] == 200:
        if len(r['data'])>0:
            #Loops to check the comment is negative or positive
            for index in range(0,len(r['data'])):
                comment_id = r['data'][index]['id']
                comment_text = r['data'][index]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if ((blob.sentiment.p_neg) > (blob.sentiment.p_pos)):
                    print "Negative comment   :: %s" % (comment_text)
                    r = requests.delete('%smedia/%s/comments/%s?access_token=%s' % (BASE_URL, media_id, comment_id, APP_ACCESS_TOKEN)).json()
                    if r['meta']['code'] == 200:
                        print "Negative Comments deleted successfully !"
                    else:
                        print "Unable to delete comments !"
        else:
            print "No comments on the post!"
    else:
        print "Status code other than 200 received!"

#-----------------------------------------------------------------------------------------------------------------------#

#Function Defines to start the app
def start_bot():
     show_menu = True
     while show_menu:

        query = input("Enter your choice ::\n 1.Get Owner's Info. \n 2.Get Recent post of owner \n 3. Get Other User Info\n 4. Get User Recent Post \n 5. Download User's recent post \n 6. Like a Post  \n 7. Comment on a post \n 8. List Of Comments on a Post \n 9. Delete Negative comments \n 0. Exit ")

        if query ==1:

             owner_info()
        elif query == 2:
             owner_post()
        elif query==3:
             username=raw_input("Enter the user name:")
             user_info(username)
        elif query==4:
             username=raw_input("Enter the user name:")
             user_post(username)
        elif query == 5:
             username = raw_input("\nEnter the username: ")
             dwnld_user_post(username)  # Calling the download_user_post() method to download other user's post
        elif query==6:
             username=raw_input("\n Enter the username:")
             like_post(username)
        elif query==7:
             username=raw_input("\n Enter the username:")
             comment_post(username)
        elif query==8:
             username=raw_input("\n Enter the username:")
             comment_list(username)
        elif query ==9:
            username=raw_input("\n Enter the username:")
            del_comment(username)

        elif query==0:
             exit()
        else:
            print "Invalid choice"

#-----------------------------------------------------------------------------------------------------------------------#
#Function call to run the app
start_bot()
