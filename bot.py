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
                                  client_secret=os.environ.get('CLIENT_SECRET'),
                                  username=os.environ.get('REDDIT_USERNAME'),
                                  password=os.environ.get('REDDIT_PASSWORD'),
                                  user_agent='There\'s only one Arsène Wenger (by /u/panarangcurry)')

        self.subreddit = self.reddit.subreddit('Gunners')

        self.search_phrase = 'papa wengz'

    def run(self):
        for comment in self.subreddit.stream.comments(skip_existing=True):
            if self.search_phrase in comment.body.lower():
                logger.info('Found key phrase')
                try:
                    reply = '>' + random.choice(self.quotes)
                    reply += '\n___\n'
                    reply += '^(***There\'s only one Arsène Wenger*** ([/u/panarangcurry](https://www.reddit.com/u/panarangcurry), quote from [QuoteTab]({link}) archive)^)'.format(
                        link=QUOTES_BASE_URL_1)
                    comment.reply(reply)
                    logger.info('Replied')
                except PrawcoreException:
                    logger.exception('Prawcore Exception')
                except KeyboardInterrupt:
                    logger.exception('Keyboard Interrupt')


def main():
    bot = Bot()
    bot.run()


if __name__ == '__main__':
    main()
