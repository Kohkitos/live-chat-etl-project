import time
from tools import *
from preloads import *

DURATION = 5 * 60 * 60  # 5 hours * 60 minutes * 60 seconds
INITIATION_TIME = time.time()

if __name__=='__main__':
    while True:

        elapsed_time = time.time() - INITIATION_TIME

        if elapsed_time >= DURATION:
            break   

        # try except just in case something unexpected breaks
        for i in range(2):
            if i:
                try:
                    users = get_top_twitch()
                except:
                    continue
            else:
                try:
                    users = get_top_youtube()
                except:
                    continue

        # try except just in case a streaming goes offline just in time I initiate function
            for user in users[1:]:
                try:
                    extractor(user, users[0])
                except:
                    pass