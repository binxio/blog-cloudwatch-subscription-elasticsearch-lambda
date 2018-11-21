import gzip
import json
import os
from base64 import b64decode
from datetime import date
from typing import List

import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

host = os.environ['DOMAIN_ENDPOINT']
region = os.environ['REGION']
service = 'es'

def decompress(data) -> bytes:
    return gzip.decompress(data)

def decode_record(data: dict) -> dict:
    decompressed = decompress(b64decode(data['data']))
    event = json.loads(decompressed.decode('utf8'))
    return event

def decode_cw_event(event: dict) -> dict:
    return decode_record(event['awslogs'])

def get_current_year_month_day() -> str:
    "returns the iso date format yyyy-mm-dd"
    return date.today().isoformat()

def get_index_with_date(index: str) -> str:
    "returns the index with date in the format index-yyyy-mm-dd"
    return index + get_current_year_month_day()

def get_client(host, awsauth):
    return Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

def get_cluster(es):
    return es.cluster

def dump_cluster_info(es) -> None:
    cluster = get_cluster(es)
    print(json.dumps(cluster.health()))
    print(json.dumps(cluster.stats()))

def string_to_dict(json_str: str) -> dict:
    try:
        return json.loads(json_str)
    except:
        return { 'message': json_str }

def process_cw_log(log: dict) -> List[dict]:
    "returns a cloudwatch log events with message field converted to dict"
    log_events = log.get('logEvents')
    if log_events:
        for event in log_events:
            if event['message']:
                event.update({'message': string_to_dict(event['message'])})
    return log_events

def handler(event, ctx):
    "index cloudwatch log to ES"
    log_events = process_cw_log(decode_cw_event(event))
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    es = get_client(host, awsauth)
    dump_cluster_info(es)

    # insert documents one-by-one
    for event in log_events:
        es.index(index=get_index_with_date('logs'), doc_type="log", body=event)

    # select all documents in the index
    query = {"query": {"match_all": {}}}
    res = es.search(index=get_index_with_date('logs'), doc_type='log', body=query)
    print(json.dumps(res))
