from datetime import datetime

class Stats():

    def __init__(self, reddit):
        self.reddit = reddit

        user = reddit.user.me()
        self.user = user

        self.age = datetime.now() - datetime.utcfromtimestamp(user.created_utc)

        best_submission = None
        for submission in user.submissions.top(limit=None):
            if best_submission is not None:
                if submission.score > best_submission.score:
                    best_submission = submission
                    break
            else:
                best_submission = submission
        self.best_submission = best_submission

        self.best_comment = list(user.comments.top(limit=1))[0]

        karma = reddit.user.karma()
        subs = [{"sub": sub, "comment": karma[sub]["comment_karma"], "link": karma[sub]["link_karma"]} for sub in karma]
        self.popular_subs = sorted(subs, reverse=True, key=lambda k: k["comment"] + k["link"])

        path = "/user/{user}/moderated_subreddits".format(user=user)
        subs = [reddit.subreddit(sub["sr"]) for sub in reddit.get(path)["data"]]
        self.moderated_subs = sorted(subs, reverse=True, key=lambda k: k.subscribers)

    def get_md(self):
        user = self.user

        markdown = "# /u/{} Statistics\n\n".format(user)
        markdown += "{} Karma\n\n".format(user.comment_karma + user.link_karma)
        markdown += "{} Comment Karma | {} Link Karma\n\n".format(user.comment_karma, user.link_karma)
        markdown += "{} Days Old\n\n".format(self.age.days)
        markdown += " - [Most upvoted post.](https://wwww.reddit.com/{})\n".format(self.best_submission.permalink)
        markdown += " - [Most upvoted comment.]({})\n\n".format(self.best_comment.permalink)

        markdown += "# Top 15 Subreddits by Total Karma gained\n"
        table = "| Subreddit | Comment Karma | Link Karma |\n" \
                "|-----------|---------------|------------|\n"
        max_subs = min(len(self.popular_subs), 15)
        for i in range(0, max_subs):
            sub = self.popular_subs[i]
            table += "| /r/{} | {} | {} |\n".format(sub["sub"], sub["comment"], sub["link"])
        markdown += table + "\n"

        markdown += "# 15 Biggest Moderated Subreddits\n"
        table = "| Subreddit | Subscribers |\n" \
                "|-----------|-------------|\n"
        max_subs = min(len(self.moderated_subs), 15)
        for i in range(0, max_subs):
            sub = self.moderated_subs[i]
            table += "| /r/{} | {} |\n".format(sub, sub.subscribers)
        markdown += table + "\n"

        return markdown

    def post(self, url=""):
        lines = self.get_md().splitlines()
        lines = lines[1:len(lines)]
        md = "\n".join(lines)
        md += "\n^(Generated with Egosaurus | Get on [GitHub](https://github.com/Dan6erbond/Egosaurus))"

        if url != "":
            submission = self.reddit.submission(url=url)
            submission.edit(md)
        else:
            sub = self.reddit.subreddit("u_{}".format(self.user))
            sub.submit("/u/{} Statistics".format(self.user), md)

    def print(self):
        user = self.user

        print("/u/{} Statistics:".format(user))
        print("")
        print("{} Karma".format(user.comment_karma + user.link_karma))
        print("{} Comment Karma | {} Link Karma".format(user.comment_karma, user.link_karma))
        print("{} Days Old".format(self.age.days))
        print("")
        print("Most upvoted post: {}".format(self.best_submission.title))
        print("Most upvoted comment on /r/{}: {}".format(self.best_comment.subreddit, self.best_comment.body))
        print("")

        print("Top 15 Subreddits by Total Karma gained:")
        max_subs = min(len(self.popular_subs), 15)
        for i in range(0, max_subs):
            sub = self.popular_subs[i]
            print("{} Comment Karma | {} Link Karma in /r/{}".format(sub["comment"], sub["link"], sub["sub"]))

        print("")

        print("15 Biggest Moderated Subreddits:")
        max_subs = min(len(self.moderated_subs), 15)
        for i in range(0, max_subs):
            sub = self.moderated_subs[i]
            print("{}: {} Subscribers".format(sub, sub.subscribers))
