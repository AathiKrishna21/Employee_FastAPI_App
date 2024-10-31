from pymongo import MongoClient


class MongoDB:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['employees']

    @classmethod
    def get_db(cls):
        return cls.db
