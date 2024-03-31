import json

result_parser = "result_parser.json"


def load_json_file():
    try:
        with open(result_parser, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_json_file(item):
    with open(result_parser, 'w', encoding='utf-8') as file:
        json.dump(item, file, indent=4, ensure_ascii=False)
