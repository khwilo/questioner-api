'''Module for commonly used methods'''

def fetch_item(item_search_term, key, item_list):
    '''Fetch an item by its id'''
    item = {}
    for index, _ in enumerate(item_list):
        if item_list[index].get(key) == item_search_term:
            item = item_list[index]
    return item
