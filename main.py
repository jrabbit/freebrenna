import time
from collections import namedtuple
import shelve

from twython import Twython
import auth

Tweet = namedtuple('Tweet', ['user', 'twid'])

class FreeBrenna(object):
    def __init__(self):
        self.t = Twython(app_key=auth.app_key,
            app_secret=auth.app_secret,
            oauth_token=auth.oauth_token,
            oauth_token_secret=auth.oauth_token_secret)
        self.s = shelve.open("nagged")
        if 'users' in self.s:
            self.users_nagged = self.s['users']
            self.last_id = self.s['lastid']
            
        else:
            self.users_nagged = []
            self.last_id = None
    
    def savetheworld(self):
        f = self.t.search(q="-breanna bradley manning", since_id=self.last_id, rpp=100)
        if not f['results']:
            time.sleep(60*5) #5 min sleep
            self.savetheworld()
        for i in [Tweet(x['from_user'], x['id']) for x in f['results']]:
            print i
            if i.user not in self.users_nagged:
                self.send_reply(i)
                time.sleep(15)
            self.users_nagged.append(i.user)
        self.last_id = sorted([(x['id']) for x in f['results']])[-1]
        time.sleep(60*4) #4 minute sleep
        self.savetheworld()
    
    def send_reply(self, i):
        text = "@%s http://feministing.com/2011/12/22/why-does-the-media-and-her-supposed-supporters-continue-to-misgender-breanna-manning/" % str(i.user)
        self.t.updateStatus(status=text,
         in_reply_to_status_id=str(i.twid),
         lat="39.374325", 
         long="-94.940114",
         display_coordinates= "true")
         #https://en.wikipedia.org/wiki/Midwest_Joint_Regional_Correctional_Facility

    def teardown(self):
        "Write out nagged_users to file"
        self.s['users'] = self.users_nagged
        self.s['lastid'] = self.last_id
        self.s.close()
        
if __name__ == '__main__':
    q = FreeBrenna()
    try:
        q.savetheworld()
    except KeyboardInterrupt:
        q.teardown()
    except Exception as e:
        q.teardown()
        raise e