import time
from datetime import datetime 
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
        if 'users' not in self.s:
            self.s['users'] = []
            self.s['lastid'] = None
            self.s['count'] = 0
    
    def savetheworld(self):
        f = self.t.search(q="-breanna bradley manning", since_id=self.last_id, rpp=100)
        if not f['results']:
            time.sleep(60*5) #5 min sleep
            self.savetheworld()
        for i in [Tweet(x['from_user'], x['id']) for x in f['results']]:
            print i
            if i.user not in self.s['users']:
                self.send_reply(i)
                time.sleep(15)
            self.s['users'].append(i.user)
        self.s['lastid'] = sorted([(x['id']) for x in f['results']])[-1]
        time.sleep(60*4) #4 minute sleep
        self.savetheworld()
    
    def send_reply(self, i):
        text = "@%s http://feministing.com/2011/12/22/why-does-the-media-and-her-supposed-supporters-continue-to-misgender-breanna-manning/ #freepvtmanning" % str(i.user)
        self.t.updateStatus(status=text,
         in_reply_to_status_id=str(i.twid),
         lat="39.374325", 
         long="-94.940114",
         display_coordinates= "true")
         #https://en.wikipedia.org/wiki/Midwest_Joint_Regional_Correctional_Facility

    def islimited(self):
        if self.s['count'] < 900:
            return False
        if 'limitday' in self.s:
            elif self.s['limitday'].day is not datetime.now().day:
                return False
            elif self.s['count'] >= 900:
                return True
        elif self.s['count'] >= 900:
            return True
      
if __name__ == '__main__':
    q = FreeBrenna()
    try:
        q.savetheworld()
    except KeyboardInterrupt as e:
        q.s.close()
        raise e
    except Exception as e:
        q.s.close()
        raise e