import json

def parse(file_path: str) -> (str, str):
    # Returns URL, Content
    with open(file_path, 'rb') as f:
        data = json.load(f)

    return data['url'], data['content'].encode('utf-8'), data['encoding']