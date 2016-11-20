import praw
import os
import time
import OAuth2Util

def remove_punc(s):
    for i in ['.',',','"', ';']:
        s = s.replace(i, "")
    return s

def parse_file(f):
    #Parse the text file that contains all of the rules
    s = [word.replace('\n','\n\n') for word in f.read().split('*')]
    return s
    
def run_bot():
    user_agent = "FTC Rules"
    r = praw.Reddit(user_agent=user_agent)
    o = OAuth2Util.OAuth2Util(r)
    o.refresh(force=True)

    # Have we run this code before? If not, create an empty list
    if not os.path.isfile("posts_replied_to.txt"):
        posts_replied_to = []

    # If we have run the code before, load the list of posts we have replied to
    else:
        # Read the file into a list and remove any empty values
        with open("posts_replied_to.txt", "r") as f:
            posts_replied_to = f.read()
            posts_replied_to = posts_replied_to.split("\n")
            posts_replied_to = filter(None, posts_replied_to)
        
    rulesDict = dict((line.strip().split(' = ') for line in parse_file(file("RulesDict.txt"))))
    for c in praw.helpers.comment_stream(r, 'ftc'):    #Choose what subreddit to get comments from
        o.refresh()
        text = c.body
        words = text.split()
        rules = []

        for word in words:
            if word[0] == '!':      #The bot is called by using '!' followed by a rule number
                word = remove_punc(word[1:]).upper()     
                if word in rulesDict and rulesDict[word] not in rules:
                    rules.append(rulesDict[word])
    
        if len(rules) > 0 and c.id not in posts_replied_to:
            message = ''.join([rule + '\n\n' for rule in rules])
            #send the message here
            while len(message) > 9500:
                c.reply(message[:9500] + " ...continued in next post... ")
                message = message[9500:]
            sent = False
            while not sent:
                try:
                    c.reply(message)
                    posts_replied_to.append(c.id)
                    with open("posts_replied_to.txt", "a") as f:
                        f.write(c.id+'\n')
                    sent = True
                except praw.errors.RateLimitExceeded as error:
                    print '\tSleeping for %d seconds' % error.sleep_time
                    for i in range(int(error.sleep_time)):
                        time.sleep(1)

if __name__ == '__main__':
    run_bot()
