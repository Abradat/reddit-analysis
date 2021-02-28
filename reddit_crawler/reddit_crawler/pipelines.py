# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pycorenlp import StanfordCoreNLP


class DataManipulatePipeline:
    def process_item(self, item, spider):
        item['score'] = item['score'] + 1
        item['numAwards'] = item['numAwards'] + 1
        return item


class SentimentAnalyzerPipeline:
    def __init__(self):
        self.nlp = StanfordCoreNLP('http://localhost:9000')

    def process_item(self, item, spider):
        result = self.nlp.annotate(item['title'],
                                   properties={
                                       'annotators': 'sentiment',
                                       'outputFormat': 'json',
                                       'timeout': 1000
                                   })
        average_sentiment = 0.0
        for s in result['sentences']:
            print("{}: '{}': {} (Sentiment Value) {} (Sentiment)".format(
                s["index"],
                " ".join([t["word"] for t in s["tokens"]]),
                s["sentimentValue"], s["sentiment"]))
            average_sentiment += int(s['sentimentValue'])
        average_sentiment = int(round(average_sentiment / len(result['sentences'])))
        item['titleSentiment'] = average_sentiment
        return item
