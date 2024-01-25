from pymongo import MongoClient

class MongoDB:
    def __init__(self, connection_string, database_name, collection_name):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = self.db[collection_name]

    def update_spreads(self, market_id, new_spread):
            spread_document = self.collection.find_one({'market_id': market_id})

            if spread_document:
                existing_spreads = spread_document.get('spreads')
                if existing_spreads is not None:
                    existing_spreads.append(new_spread)
                    self.collection.update_one({'market_id': market_id}, {'$set': {'spreads': existing_spreads}})
                else:
                    self.collection.update_one({'market_id': market_id}, {'$set': {'spreads': [new_spread]}})
                    existing_spreads = [new_spread]
            else:
                self.collection.insert_one({'market_id': market_id, 'spreads': [new_spread]})
                existing_spreads = [new_spread]

            return existing_spreads