import logging
import os
import random
import re
import requests
import sys
import praw
from prawcore.exceptions import PrawcoreException

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

QUOTES_BASE_URL_1 = 'https://www.quotetab.com/quotes/by-arsene-wenger'
QUOTES_BASE_URL_2 = 'https://www.quotetab.com/quotes/by-arsene-wenger/2'


class Bot:
    def __init__(self):
        try:
            resp = requests.get(QUOTES_BASE_URL_1)
            self.quotes = re.findall(
                r'<blockquote.*>(.*)</blockquote>', resp.text)
            resp = requests.get(QUOTES_BASE_URL_2)
            self.quotes += re.findall(
                r'<blockquote.*>(.*)</blockquote>', resp.text)
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        self.reddit = praw.Reddit(client_id=os.environ.get('CLIENT_ID'),
                                  client_secret=os.environ.get(
                                      'CLIENT_SECRET'),
                                  username=os.environ.get('REDDIT_USERNAME'),
                                  password=os.environ.get('REDDIT_PASSWORD'),
                                  user_agent='There\'s only one Arsène Wenger (by /u/panarangcurry)')

        self.subreddit = self.reddit.subreddit('Gunners')

        self.search_phrase = 'papa wengz'

        self.comment_ids = set()
        self.comment_authors = set()

    def run(self):
        try:
            for comment in self.subreddit.stream.comments(skip_existing=True):
                if self.search_phrase in comment.body.lower() and comment.id not in self.comment_ids and comment.author.name not in self.comment_authors:
                    logger.info('Found key phrase')
                    try:
                        self.comment_ids.add(comment.id)
                        self.comment_authors.add(comment.author.name)
                        replyStr = '>' + random.choice(self.quotes)
                        replyStr += '\n___\n'
                        replyStr += '^(***There\'s only one Arsène Wenger*** (quote from [QuoteTab]({link}) archive)^)'.format(
                            link=QUOTES_BASE_URL_1)
                        comment.reply(replyStr)
                        logger.info('Replied')
                    except PrawcoreException:
                        logger.exception('Prawcore Exception')
                    except KeyboardInterrupt:
                        logger.exception('Keyboard Interrupt')
        except PrawcoreException:
            logger.exception('Prawcore Exception')


def main():
    bot = Bot()
    while True:
        bot.run()


if __name__ == '__main__':
    main()
