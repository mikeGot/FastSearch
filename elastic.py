from elasticsearch import Elasticsearch
from loguru import logger


def connect_elasticsearch(host: str, port: int):
    _es = None
    _es = Elasticsearch([{'host': host, 'port': port}])
    if _es.ping():
        logger.info('ES Yay Connect')
    else:
        logger.error('ES Awww it could not connect!')
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

es_object = connect_elasticsearch(host="192.168.1.103", port=9200)


def csv_to_es(doc):
    data = {
        "doc_text": doc.text,
        "doc_id": doc.id
    }
    try:
        es_object.index(index='document', document=data)
    except Exception as e:
        logger.exception(e)


def create_index():
    es_object.create(index="document", document=doc_scheme, id="1")


def put_to_elastic(list_of_documents):
    for d in list_of_documents:
        csv_to_es(d)
    logger.info("Данные успешно импортировались в Elastic")

