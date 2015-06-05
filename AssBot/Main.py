import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import sqlite3
 
SUMMONTEXT = """+/u/FusionGaming\s*'([\s\S]+')\s*vs\s*'([\s\S]+')""" # MAKE A REGEX TO FIND A SUMMON TEXT
 
#  Import Settings from Config.py
try:
    import Config
    USERNAME = Config.USERNAME
    PASSWORD = Config.PASSWORD
    USERAGENT = Config.USERAGENT
    MAXPOSTS = Config.MAXPOSTS
    
    print("Loaded Config")
except ImportError:
    print("Error Importing Config.py")
    
WAIT = 5
 
r = praw.Reddit(USERAGENT)
r.login(USERNAME, PASSWORD)
 
sql = sqlite3.connect('comments.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS posts(CID TEXT)')
print('Loaded SQL Database')
sql.commit()
 
def scan():
    stream = praw.helpers.comment_stream(r, 'all')
    for comment in stream:
    
        cbody = comment.body.lower()
        cid = comment.id
        
                
        cur.execute('SELECT * FROM posts WHERE CID=?', [cid])
        if not cur.fetchone():
            print("Found a summon comment")
            
            #DO STUFF HERE
 
        
            print('Replying to ' + cid)
            comment.reply("MESSAGE")
            
            cur.execute('INSERT INTO posts VALUES(?)', [cid])
            sql.commit()
        else:
            print("Already replied to that comment")
                
    
while True:
    try:
        scan()
    except Exception as e:
        print("ERR", e)
    print('Sleeping ' + str(WAIT))
    time.sleep(WAIT)
