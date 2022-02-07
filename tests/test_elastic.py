import config
import elastic


def test_connect():
    es = elastic.connect(config.es_host, config.es_port)
    assert es.ping() == True
