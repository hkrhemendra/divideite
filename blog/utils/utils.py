from bson import json_util
import json

def parse_json(data):
    return json.loads(json_util.dumps(data))

def data_length(data):
    database = []
    print('data ==================> ',data)
    for single_data in data:
        database.append(single_data)

    if len(database) == 0:
        return 0
    else: 
        return database[0]['id']