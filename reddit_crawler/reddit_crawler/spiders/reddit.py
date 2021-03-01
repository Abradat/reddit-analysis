import scrapy
from urllib.parse import urlencode
import json
from datetime import datetime, date


class RedditSpider(scrapy.Spider):
    # Main Spider Responsible for Crawling Reddit

    name = 'reddit'
    allowed_domains = ['reddit.com']

    # Headers definition in order to prevent Reddit from blocking the spider
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
        'accept': '*/*'
    }

    def __init__(self, name=None, **kwargs):
        super(RedditSpider, self).__init__(name, **kwargs)
        self.from_date = datetime.strptime(self.from_date, '%d-%m-%Y')
        # if user enters now as the to_date argument, today's date will be used as the to_date variable
        if self.to_date == 'now':
            self.to_date = datetime.today()
        else:
            self.to_date = datetime.strptime(self.to_date, '%d-%m-%Y')

    def start_requests(self):
        # Defining the starting url for scarping the website
        url = self.generate_request_url(f'https://gateway.reddit.com/desktopapi/v1/subreddits/{self.topic}', '')
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        reached_before = False
        json_response = json.loads(response.text)
        posts = json_response['posts']
        for postId in json_response['postIds']:
            if len(postId) == 9:  # Ignoring ad posts
                if self.check_date_range(posts[postId]['created']):
                    post = {
                        'postId': postId,
                        'title': posts[postId]['title'],
                        'numComments': posts[postId]['numComments'],
                        'created': posts[postId]['created'],
                        'score': posts[postId]['score'],
                        'upvoteRatio': posts[postId]['upvoteRatio']
                    }
                    num_awards = 0
                    if 'allAwardings' in posts[postId]: # Summing all the awards for each post
                        for award in posts[postId]['allAwardings']:
                            num_awards += award['count']
                    post['numAwards'] = num_awards
                    yield post
                elif self.is_before_start(posts[postId]['created']): # Stop crawling more when reached the date before from date variable
                    reached_before = True
                    break
        if not reached_before:
            url = self.generate_request_url(f'https://gateway.reddit.com/desktopapi/v1/subreddits/{self.topic}',
                                            json_response['postIds'][-1])
            yield scrapy.Request(url, callback=self.parse)

    def generate_request_url(self, url, after_item_id):
        # Building the desired URL for sending request based on the last post crawled.

        query_params = {
            'rtj': 'only',
            'redditWebClient': 'web2x',
            'app': 'web2x-client-production',
            'include': 'prefsSubreddit',
            'after': after_item_id,
            'dist': 9,
            'layout': 'card',
            'sort': 'new'
        }
        return url + '?' + urlencode(query_params)

    def check_date_range(self, post_date):
        # Check whether the given date is between from_date and to_date variables or not

        post_date = datetime.fromtimestamp(post_date / 1000)
        return self.from_date <= post_date <= self.to_date

    def is_before_start(self, post_date):
        # Check whether the given date is before from_date variable or not
        post_date = datetime.fromtimestamp(post_date / 1000)
        return post_date < self.from_date
