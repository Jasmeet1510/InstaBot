#-----------------------------------------------------------------------------------------------------------------------#
                                                    #INSTABOT#
#-----------------------------------------------------------------------------------------------------------------------#

#Required libraries imported  for developing the app

import requests
from pprint import pprint
response = requests.get('https://api.jsonbin.io/b/59d0f30408be13271f7df29c').json()

#-----------------------------------------------------------------------------------------------------------------------#
#To get the Instagram API and Convert it into JSON forma

APP_ACCESS_TOKEN = response['access_token']
BASE_URL='https://api.instagram.com/v1/'


#-----------------------------------------------------------------------------------------------------------------------#
#Function For Own Information

def owner_info():
    r = requests.get('%susers/self/?access_token=%s' % (BASE_URL,APP_ACCESS_TOKEN)).json()

    if r['meta']['code'] == 200:
        pprint(r)
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

owner_info()



