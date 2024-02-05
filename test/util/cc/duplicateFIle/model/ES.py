from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, scan
import logging

ES_CONFIG = {
    "hosts": ["127.0.0.1"],
    "http_auth": ["elasticuser", "123***4"],
    "sniff_on_start": False,
    "sniff_on_connection_fail": True,
    "sniffer_timeout": 180,
    "sniff_timeout": 5
}

ES_CLIENT = Elasticsearch(**ES_CONFIG)


def worker(es, actions, chunk_size=3000, max_chunk_bytes=100 * 1024 * 1024):
    try:
        success, _ = bulk(es, actions=actions, chunk_size=chunk_size, max_chunk_bytes=max_chunk_bytes,
                          raise_on_error=False, request_timeout=180)
        print(success, _)
    except Exception as e:
        logging.info(e)
        # logging.error(e,exc_info=1)


# es查询  do_scroll
def do_scroll(es, index, body):
    try:
        return scan(client=es, query=body, index=index, scroll=u"10m", size=5000, request_timeout=180,
                    raise_on_error=False)
    except Exception as e:
        logging.info(e)


if __name__ == '__main__':

    index = "flink-test"
    search_body = {
        "query": {
            "match_all": {}
        }
    }

    res = ES_CLIENT.search(index=index, body=search_body)
    res_scroll = do_scroll(ES_CLIENT, index, search_body)
    print(res_scroll)
    for item in res_scroll:
        print(item)