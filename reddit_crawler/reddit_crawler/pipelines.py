# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pycorenlp import StanfordCoreNLP



class DataManipulatePipeline:
    # This class is a pipeline for modifying score, numAwards, and created values to have a better dataset

    def process_item(self, item, spider):
        item['score'] = item['score'] + 1  # Incrementing score one unit to avoid many zero values in dataset
        item['numAwards'] = item[
                                'numAwards'] + 1  # Incrementing numAwards one unit to avoid many zero values in dataset
        item['created'] = int(item['created'] / 1000)  # Removing 000 from the end of timestamps
        return item


class SentimentAnalyzerPipeline:
    # This class is a pipeline for extracting sentiment of posts' titles using Stanford Core NLP

    def __init__(self):
        self.nlp = StanfordCoreNLP(
            'http://localhost:9000')  # Initialization of an instance for connecting to the Core NLP

    def process_item(self, item, spider):
        # Calling CoreNLP through its API. Passing sentiment as the property to retrieve the sentiment of the title
        result = self.nlp.annotate(item['title'],
                                   properties={
                                       'annotators': 'sentiment',
                                       'outputFormat': 'json',
                                       'timeout': 1000
                                   })
        average_sentiment = 0.0
        for s in result['sentences']:  # Calculation the average sentiment for titles having multiple sentences
            average_sentiment += int(s['sentimentValue'])
        average_sentiment = int(round(average_sentiment / len(result['sentences'])))
        item['titleSentiment'] = average_sentiment  # Adding title's sentiment to the item
        del item['title']  # Removing the title from the item
        return item
