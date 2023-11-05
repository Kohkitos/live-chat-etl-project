import time
from functions import *
from preloads import *

duration = 5 * 60 * 60  # 5 hours * 60 minutes * 60 seconds

# Tiempo inicial
initiation_time = time.time()

while True:
    
    elapsed_time = time.time() - initiation_time
    
    if elapsed_time >= duration:
        break   
    else:
        pass
    
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
        for user in users:
            if user == users[0]:
                continue
            else:
                try:
                    extractor(user, users[0])
                except:
                    pass