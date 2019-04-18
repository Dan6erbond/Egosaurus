# Egosaurus

Egosaurus is a simple script that allow you to print your Reddit statistics and/or post them to your user profile as well as save it in a .md file.

## Usage
Downloading the [stats.py](stats.py) file to your local system and create a file similar or identical to [example.py](example.py) to have your statistics printed and/or saved as well as posted to your profile:

```python
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
```

Instantiating the Stats object will instantly have it calculate the statistics that are needed when calling the next methods. `print()` outputs all the relevant statistics in the console while `get_md()` returns the statistics in default markdown format which can be saved in a file (in this case [statistics.md](statistics.md)) and viewed for future reference.

### Post to Reddit
The `post()` method is also very simple. With no arguments it will create a new post on the user's profile while giving it the URL to a post will have it edit the post. The format is identical to that of the markdown file generated with `get_md()` though the first line is removed as the title tends to be descriptive enough.
