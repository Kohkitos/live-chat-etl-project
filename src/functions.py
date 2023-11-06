# Libraries

from chat_downloader import ChatDownloader
import datetime
import time

from pymongo import MongoClient
from passwords import STR_CONN # a file with my connection string to the mongodb atlas db

from selenium import webdriver
from selenium.webdriver.common.by import By

from preloads import *


'''
 ___   _   ___   ____  _     _   _      ____ 
| |_) | | | |_) | |_  | |   | | | |\ | | |_  
|_|   |_| |_|   |_|__ |_|__ |_| |_| \| |_|__ 
'''

def extractor(user, platform):
    '''
    Initialise a new session for making requests to the user prompted, and 
    then extracts the messages, saves video information to a mongo database, 
    does an analysis of the messages and uploads the results to the same database.

    :param user: the user from whose video the chat is going to be extracted,
    either the name for twitch or the url for youtube.
    :type user: str
    :param platform: either twitch or youtube
    :type platform: str
    '''
    if platform == 'twitch':
        url = f'https://www.twitch.tv/{user}'
    else:
        url = user
    
    # load mongo cursor
    cursor = MongoClient(STR_CONN)
    db = cursor.live_chats
    
    try:
        chat = ChatDownloader().get_chat(url,
                                        retry_timeout = -1, # -1 makes the downloader to retreive a message as soon as is published
                                        timeout = 120)       # 120 secs of scrapping
    except:
        try:
            video_son = {
                '_id': url[32:],
                'url': url,
                'first_recored': datetime.datetime.now(),
                'platform': platform,
                'last_update': datetime.datetime.now(),
                'chat_disabled': True
                }
            db.video.insert_one(video_son)
        except:
            db.video.update_one(
                                {"_id": vid_id},
                                {"$set": {"last_update": datetime.datetime.now(),
                                         'chat_disabled': True}}
                                )
        return 1

    # video data
    vid_id = chat.__dict__['id']
    vid_title = chat.__dict__['title']

    video_son = {
                '_id': vid_id,
                'title': vid_title,
                'url': url,
                'first_recored': datetime.datetime.now(),
                'platform': platform,
                'last_update': datetime.datetime.now(),
                'chat_disabled': False
                }

    # try pass just in case the author id is already there
    try:
        db.video.insert_one(video_son)
    except:
        db.video.update_one(
                            {"_id": vid_id},
                            {"$set": {"last_update": datetime.datetime.now(),
                                     'chat_disabled': False}}
                            )
    for message in chat:                        
        add_message(message, db)
 
'''
_____  _       _  _____  __    _    
 | |  \ \    /| |  | |  / /`  | |_| 
 |_|   \_\/\/ |_|  |_|  \_\_, |_| | 
'''
          
def get_top_twitch():
    
    '''
    Retrieves a list with the names of the top 5 streamers with the most viewers
    in Spanish language.

    :return: a list with the first element being 'twitch', and the other five the
    streamers' names.
    :rtype: lst of str.
    '''

    driver = webdriver.Chrome(OPCIONES)

    time.sleep(2)

    url = 'https://twitchtracker.com/channels/live/spanish' # web with top live streams in spanish at the moment

    driver.get(url)

    # process to get the top_5
    table = driver.find_element(By.CSS_SELECTOR, 'table')
    top_5 = table.find_elements(By.CSS_SELECTOR, 'tr')[:5]

    users = ['twitch']

    for e in top_5:
        users.append(e.find_elements(By.CSS_SELECTOR, 'a')[1].text.lower())
    

    for user in users:
        if user == users[0]:
            continue
        else:
            add_creator(user, users[0], driver)
        
    driver.quit()
    return(users)

'''
 _     ___   _    _____  _     ___   ____ 
\ \_/ / / \ | | |  | |  | | | | |_) | |_  
 |_|  \_\_/ \_\_/  |_|  \_\_/ |_|_) |_|__ 
'''

def get_top_youtube():
    
    '''
    Retrievs a list with the names of the top 1 streamers with the most viewers
    in Spanish language.

    :return: a list with the first element being 'twitch', and the other one the
    streamer's names.
    :rtype: lst of str.
    '''

    driver = webdriver.Chrome(OPCIONES)

    time.sleep(2)

    url = 'https://playboard.co/en/live/top-viewing-all-live-in-spain' # web with top live streams in spanish at the moment

    driver.get(url)

    # process to get the top_5
    best = top_5 = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div/main/div[5]/div').find_elements(By.CSS_SELECTOR, 'div.item.list__item')[:5]
    
    users = ['youtube']

    for vid in best:
        href = vid.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')[30:]
        users.append(f'https://www.youtube.com/watch?v={href}')
    for user in users:
        if user == users[0]:
            continue
        else:
            add_creator(user, users[0], driver)
    
    driver.quit()
    return(users)    

'''
 _      ___   _      __    ___   ___   ___  
| |\/| / / \ | |\ | / /`_ / / \ | | \ | |_) 
|_|  | \_\_/ |_| \| \_\_/ \_\_/ |_|_/ |_|_) 
'''

def add_message(samp, db):
    '''
    Takes a message and adds its info and the author's info to the mongo database provided.
    
    :param samp: a json with message's info.
    :type samp: json.
    :param db: a cursor to a mongoDB database.
    :type db: mongoDB cursor.
    '''
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
    
    # just in case a commentor is a recurrent user, we will update the last_update
    try:
        db.user.insert_one(auth_son)
    except:
        db.user.update_one(
                {"_id": auth_son['_id']},
                {"$set": {"last_update": datetime.datetime.now()}}
                )
    # sometimes, a message can be recorded twice, this will prevent any error
    try:
        db.message.insert_one(mess_son)
    except:
        pass


def add_creator(user, platform, driver):
    
    '''
    Extracts the information of the creator provided and then either adds or updates
    the information in the mongo database.

    :param user: the user that is going to be added or updated to the database,
    either the name for twitch or the url for youtube.
    :type user: str
    :param platform: either twitch or youtube
    :type platform: str
    :param driver: selenium driver.
    :type driver: selenium.webdriver.
    '''
    
    
    if platform == 'twitch':
        url = f'https://www.twitch.tv/{user}'
        driver.get(url)

        followers = driver.find_element(By.XPATH, '//*[@id="live-channel-about-panel"]/div/div[2]/div/div/div/div/div[1]/div/div[2]/div/span/div/div/span').text
        _id = user
        
    else:
        driver.get(user)
        
        try:
            driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/form[1]/div/div/button/span').click() # reject cookies
        
        except:
            pass
        
        time.sleep(2)
        
        try:
            driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]').click() # reject second set of cookies
        except:
            pass
        
        _id = user[32:]
        user = driver.find_element(By.XPATH, '//*[@id="text"]/a').text
        followers = driver.find_element(By.XPATH, '//*[@id="owner-sub-count"]').text[:6]
    
    user = {'_id': _id,
            'name': user,
            'platform': platform,
            'followers/subs': followers,
            'last_update': datetime.datetime.now()
            }
    
    cursor = MongoClient(STR_CONN)
    db = cursor.live_chats
    
    try:
        db.creator.insert_one(user)
    except:
        db.creator.update_one(
                    {"_id": _id},
                    {"$set": {"last_update": datetime.datetime.now(),
                             "followers/subs": followers}}
                    )