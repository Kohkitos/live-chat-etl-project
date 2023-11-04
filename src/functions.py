# Libraries

from chat_downloader import ChatDownloader
import datetime
from pymongo import MongoClient
from passwords import STR_CONN # a file with my connection string to the mongodb atlas db

from selenium import webdriver
from selenium.webdriver.common.by import By

def extractor(user):
    '''
    TO DO LIST:
    
    - add a second argument to specify if twitch or youtube
    - add a proper description
    '''
    
    url = f'https://www.twitch.tv/{user}'
    chat = ChatDownloader().get_chat(url,
                                    retry_timeout = -1, # -1 makes the downloader to retreive a message as soon as is published
                                    timeout = 150)      # 150 secs of scrapping
    temp = []
    for message in chat:                        
        temp.append(message)
        
    # load mongo cursor
    cursor = MongoClient(STR_CONN)

    db = cursor.live_chats

    # video data
    vid_id = chat.__dict__['id']
    vid_url = url
    vid_title = chat.__dict__['title']

    video_son = {
                '_id': vid_id,
                'title': vid_title,
                'first_recored': datetime.datetime.now(),
                'last_update': datetime.datetime.now()
                }

    # try pass just in case the author id is already there
    try:
        db.video.insert_one(video_son)
    except:
        db.video.update_one(
                            {"_id": vid_id},
                            {"$set": {"last_update": datetime.datetime.now()}}
                            )
    # message and author
    messages = []
    commentors = []

    for samp in temp:
        # message
        mess = samp['message']
        mess_id = samp['message_id']
        sent = analyzer.predict(mess).__dict__['output']
        hate = hate_speech_analyzer.predict(mess).__dict__['output']
        # common
        ts = samp['timestamp']
        # author
        name = samp['author']['name']
        com_id = samp['author']['id']

        mess_son = {
                    '_id': mess_id,
                    'message': mess,
                    'date': datetime.datetime.now(),
                    'timestamp': ts,
                    'commentator_id': com_id,
                    'video_id': vid_id,
                    'sentiment_analysis': sent,
                    'hat_speech_analysis': hate
                    }

        auth_son = {
                    '_id': com_id,
                    'name': name,
                    'last_update': datetime.datetime.now()
                    }

        messages.append(mess_son)
        commentors.append(auth_son)
        
    # sometimes, a message can be recorded twice, this will prevent any error
    for message in messages:
        try:
            db.message.insert_one(message)
        except:
            pass
    
    # just in case a commentor is a recurrent user, we will update the last_update
    for commentor in commentors:
        try:
            db.user.insert_one(commentor)
        except:
            db.user.update_one(
                    {"_id": commentor['_id']},
                    {"$set": {"last_update": datetime.datetime.now()}}
                    )

            
def get_top():
    
    '''
    TO DO:
    
    - Add description.
    '''

    driver = webdriver.Chrome(opciones)

    time.sleep(2)

    url = 'https://twitchtracker.com/channels/live/spanish' # web with top live streams in spanish at the moment

    driver.get(url)

    # process to get the top_5
    table = driver.find_element(By.CSS_SELECTOR, 'table')
    top_5 = table.find_elements(By.CSS_SELECTOR, 'tr')[:5]

    users = []

    for e in top_5:
        users.append(e.find_elements(By.CSS_SELECTOR, 'a')[1].text.lower())

    driver.quit()
    return(users)