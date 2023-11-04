# Libraries

from chat_downloader import ChatDownloader
import datetime
import time

from pymongo import MongoClient
from passwords import STR_CONN # a file with my connection string to the mongodb atlas db

from selenium import webdriver
from selenium.webdriver.common.by import By

from preloads import *

def extractor(user, platform):
    '''
    TO DO LIST:
    
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
                'platform': platform,
                'last_update': datetime.datetime.now()
                }
    
    # take creator id
    new_id = temp[0]['channel_id']
    try:
        db.creator.update_one(
                    {"name": vid_id},
                    {"$set": {"last_update": datetime.datetime.now()}}
                    )
    except:
        pass

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
        sent = ANALYZER.predict(mess).__dict__['output']
        hate = HATE_SPEECH.predict(mess).__dict__['output']
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
                    'video_title': vid_title,
                    'platform': platform,
                    'sentiment_analysis': sent,
                    'hate_speech_analysis': hate
                    }

        auth_son = {
                    '_id': com_id,
                    'name': name,
                    'platform': platform,
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

            
def get_top_twitch():
    
    '''
    TO DO:
    
    - Add description.
    '''

    driver = webdriver.Chrome(OPCIONES)

    time.sleep(2)

    url = 'https://twitchtracker.com/channels/live/spanish' # web with top live streams in spanish at the moment

    driver.get(url)

    # process to get the top_5
    table = driver.find_element(By.CSS_SELECTOR, 'table')
    top_5 = table.find_elements(By.CSS_SELECTOR, 'tr')[:5]

    users = []

    for e in top_5:
        users.append(e.find_elements(By.CSS_SELECTOR, 'a')[1].text.lower())
    

    for user in users:
        if user == users[0]:
            continue
        else:
            add_creator(user, users[0], driver)
        
    driver.quit()
    return(users)

def get_top_twitch_lame():
    
    '''
    TO DO:
    
    - Add description.
    '''

    driver = webdriver.Chrome(OPCIONES)

    time.sleep(2)

    url = 'https://twitchtracker.com/channels/live/spanish' # web with top live streams in spanish at the moment

    driver.get(url)

    # process to get the top_5
    table = driver.find_element(By.CSS_SELECTOR, 'table')
    best = table.find_element(By.CSS_SELECTOR, 'tr').find_elements(By.CSS_SELECTOR, 'a')[1].text.lower()

    users = ['twitch', best]

    for user in users:
        if user == users[0]:
            continue
        else:
            add_creator(user, users[0], driver)
        
    driver.quit()
    return(users)


def add_creator(user, platform, driver):

    url = f'https://www.twitch.tv/{user}'
    driver.get(url)

    followers = driver.find_element(By.XPATH, '//*[@id="live-channel-about-panel"]/div/div[2]/div/div/div/div/div[1]/div/div[2]/div/span/div/div/span').text

    user = {'name': user,
            'platform': platform,
            'followers': followers,
            'last_update': datetime.datetime.now()
            }
    
    cursor = MongoClient(STR_CONN)
    db = cursor.live_chats
    
    try:
        db.creator.insert_one(user)
    except:
        db.creator.update_one(
                            {"name": user},
                            {"$set": {"last_update": datetime.datetime.now(),
                                     "followers": followers}}
                            )