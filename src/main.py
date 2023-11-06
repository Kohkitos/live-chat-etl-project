import time
from joblib import Parallel, delayed
from tools import *
from preloads import *

duration = 5 * 60 * 60  # 5 hours * 60 minutes * 60 seconds

# Tiempo inicial
initiation_time = time.time()

para = Parallel(n_jobs = -1, verbose = True)

while True:
    
    elapsed_time = time.time() - initiation_time
  
    if elapsed_time >= duration:
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
        try:
            para(delayed(extractor)(user, users[0]) for user in users[:1])
        except:
            pass
