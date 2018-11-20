import boto3
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection
import curator
import os
import json

host = os.environ['DOMAIN_ENDPOINT']
region = os.environ['REGION']
service = 'es'
counter = 0

def get_client(host, awsauth):
    return Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

def handler(event, ctx):
    global counter
    counter += 1
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    es = get_client(host, awsauth)

    # log cluster health and stats
    cluster = es.cluster
    print(json.dumps(cluster.health()))
    print(json.dumps(cluster.stats()))

    # A test document.
    document = {
        "title": f"Moneyball {counter}",
        "director": f"Bennett Miller {counter}",
        "year": "2011"
    }

    # Index the test document so that we have an index that matches the timestring pattern.
    # You can delete this line and the test document if you already created some test indices.
    es.index(index="movies-2017.01.31", doc_type="movie", id=str(counter), body=document)

    query = {"query": {"match": {"title": "Moneyball"}}}
    res = es.search(index='movies-2017.01.31', doc_type='movie', body=query)
    print(json.dumps(res))

    # get a list of indexes
    index_list = curator.IndexList(es)
    # Filters by age, anything with a time stamp older than 30 days in the index name.
    index_list.filter_by_age(source='name', direction='older', timestring='%Y.%m.%d', unit='days', unit_count=30)
    print("Found %s indices to delete" % len(index_list.indices))
    # If our filtered list contains any indices, delete them.
    if index_list.indices:
        curator.DeleteIndices(index_list).do_action()
