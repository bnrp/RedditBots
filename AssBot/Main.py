import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import sqlite3
import re
 
SUMMONTEXT = "(\w+)-*ass\s+(\w+)" # MAKE A REGEX TO FIND A SUMMON TEXT
 
#  Import Settings from Config.py
try:
    import Config
    USERNAME = Config.USERNAME
    PASSWORD = Config.PASSWORD
    USERAGENT = Config.USERAGENT
    MAXPOSTS = Config.MAXPOSTS
    SUBREDDIT = 'fusion_gaming'
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
    print('Searching %s.' % SUBREDDIT)
    subreddit = r.get_subreddit(SUBREDDIT)
    comments = subreddit.get_comments(limit=MAXPOSTS)
    
    for comment in comments:
    
        cbody = comment.body
        cid = comment.id
        
        cauthor = comment.author.name
        if cauthor.lower() is USERNAME.lower():
            continue
        
        match = re.search(SUMMONTEXT, cbody)
        if not match:
            continue
                
        cur.execute('SELECT * FROM posts WHERE CID=?', [cid])
        if not cur.fetchone():
            print("Found a summon comment")
            
            #DO STUFF HERE    
            if match:
                word1 = match.group(1)
                word2 = match.group(2)
                
                if word2 = 'it':
                    continue
                
                print(match.group())
                print(cbody)
                cbody = cbody.replace(match.group() , word1+" ass-"+word2)
                print(cbody)
            else:
                continue
                
            print('Replying to ' + cid)
            comment.reply(cbody)
            
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
