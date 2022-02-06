import elasticsearch
from elasticsearch import Elasticsearch, helpers
from loguru import logger


host = "192.168.1.103"
port = 9200
es_index = "document"


def connect(host: str, port: int):
    _es = None
    _es = Elasticsearch([{'host': host, 'port': port}])
    if not _es.ping():
        logger.error('ES Awww it could not connect!')
        raise elasticsearch.ConnectionError
    return _es


doc_scheme = {
    "settings": {
        "refresh_interval": "1s",
        "analysis": {
            "filter": {
                "russian_stop": {
                    "type": "stop",
                    "stopwords": "_russian_"
                },
                "russian_stemmer": {
                    "type": "stemmer",
                    "language": "russian"
                }
            },
            "analyzer": {
                "ru": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "russian_stop",
                        "russian_stemmer"
                    ]
                }
            }
        }
    },
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "doc_text": {
                "type": "text",
                "analyzer": "ru"
            },
            "doc_id": {
                "type": "long"
            }
        }
    }
}

# es_object = connect_elasticsearch(host=host, port=port)


def create_index():
    es_object = connect(host=host, port=port)
    es_object.create(index=es_index, document=doc_scheme, id="1")
    es_object.close()


def put(list_of_documents):
    es_object = connect(host=host, port=port)
    action = list()
    for d in list_of_documents:
        data = {
            "_index": es_index,
            "_source": {
                "doc_text": d.text,
                "doc_id": d.id
            }
        }
        action.append(data)
    helpers.bulk(es_object, action)
    logger.info("Данные успешно импортировались в Elastic")


def search(user_query: str = None, doc_id: int = None):
    es_object = connect(host=host, port=port)
    if user_query is not None:
        query_body = {
                "match": {
                    "doc_text": user_query
                    }
                }
        result = es_object.search(index=es_index, query=query_body, size=20)
        all_hits = result.get("hits").get("hits")

        list_of_search_id = [id.get("_source").get("doc_id") for id in all_hits]

        return list_of_search_id

    elif doc_id is not None:
        query_body = {
            "match": {
                "doc_id": doc_id
            }
        }
        result = es_object.search(index=es_index, query=query_body, size=1)
        inner_id = result.get("hits").get("hits")[0].get("_id")
        es_object.close()
        return inner_id


def delete(doc_id):
    es_object = connect(host=host, port=port)
    inner_id = search(doc_id=doc_id)
    es_object.delete(index=es_index, id=inner_id)
    es_object.close()


if __name__ == "__main__":
    print(search("парень"))
