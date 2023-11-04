import time
from functions import *

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
    try:
        users = get_top()

        # try except just in case a streaming goes offline just in time I initiate function
        for user in users:
            try:
                extractor(user)
            except:
                continue
    except:
        print (f'An unexpected error ocurred when {elapsed_time} seconds have transcurred.')
        break