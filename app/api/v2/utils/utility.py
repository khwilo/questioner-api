'''Module for utility methods'''
from datetime import datetime

class Utility:
    '''Common methods used by the API models'''

    @staticmethod
    def serialize(obj):
        '''Helper function to JSON serialize an object'''
        if isinstance(obj, datetime):
            serialized_date = obj.isoformat()
            return serialized_date
        return obj.__dict__

    @staticmethod
    def fetch_item(item_search_term, key, item_list):
        '''Fetch an item by its id'''
        item = {}
        for index, _ in enumerate(item_list):
            if item_list[index].get(key) == item_search_term:
                item = item_list[index]
        return item
