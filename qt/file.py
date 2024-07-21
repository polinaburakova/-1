import json


def write_token(token: str):
    data = {
        "token": token
    }

    with open('payload.json', 'w', encoding='utf8') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


def read_token() -> str:
    with open('payload.json', 'r', encoding='utf8') as f:
        data = json.load(f)
        try:
            return data['token']
        except Exception as e:
            return ""


def remove_token():
    data = {
        "token": ""
    }
    with open('payload.json', 'r', encoding='utf8') as f:
        f.write(json.dumps(data))
