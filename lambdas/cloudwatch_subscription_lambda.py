import gzip
import json
from base64 import b64decode

def decompress(data) -> bytes:
    return gzip.decompress(data)

def decode_record(data: dict) -> dict:
    x = decompress(b64decode(data['data']))
    return json.loads(x.decode('utf8'))

def decode_event(event: dict) -> dict:
    return decode_record(event['awslogs'])

def handler(event, ctx) -> None:
    print(json.dumps(decode_event(event)))
