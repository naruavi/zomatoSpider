import pymongo


class DataPipeline:

    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['zomato']
        self.collection = db['restaurants']

    def process_data(self, item):
        self.collection.insert(item)

    def close_conn(self):
        self.conn.close()