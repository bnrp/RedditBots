import praw # simple interface to the reddit API, also handles rate limiting of requests
import time
import sqlite3
import re
 
SUMMONTEXT = (\w+)-*ass\s+(\w+) # MAKE A REGEX TO FIND A SUMMON TEXT
 
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
    stream = praw.helpers.comment_stream(r, 'fusion_gaming')
    for comment in stream:
    
        cbody = comment.body
        cid = comment.id
        
                
        cur.execute('SELECT * FROM posts WHERE CID=?', [cid])
        if not cur.fetchone():
            print("Found a summon comment")
            
            #DO STUFF HERE	
			match = re.search(SUMMONTEXT, cbody)
			if match:
				word1 = match.group(1)
				word2 = match.group(2)
				
				cbody.replace(group(0), word1+" ass-"+word2)
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
