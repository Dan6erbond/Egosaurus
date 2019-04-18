import login
import praw
from stats import Stats

reddit = praw.Reddit(user_agent='Egosaurus',
                     client_id=CLIENTID, client_secret=CLIENTSECRET,
                     username=USERNAME, password=PASSWORD)

stat = Stats(reddit)
stat.print()

with open("statistics.md", "w+") as f:
    f.write(stat.get_md())

# enter the URL of the post if you want the bot to edit it
stat.post()
