'''JSON serializer for objects'''
from datetime import datetime

def serialize(obj):
    '''Helper function to serialize an object'''
    if isinstance(obj, datetime):
        serial = obj.isoformat()
        return serial

    return obj.__dict__
