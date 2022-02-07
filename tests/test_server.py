from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


# передаем тест, которого нет в документах
def test_get_documents_error404():
    response = client.get("/document/get/23rujij4f")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Document not found"
    }


# передаем невалидный индекс
def test_delete_document_error422():
    response = client.delete("/document/delete/fegfr")
    assert response.status_code == 422
    assert response.json() == {
        'detail': [
            {
                'loc': ['path', 'doc_id'],
                'msg': 'value is not a valid integer', 'type': 'type_error.integer'
            }
        ]
    }


# передаем индекс, которого не существует
def test_delete_document_error404():
    response = client.delete("/document/delete/2000000")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Invalid ID"
    }


def test_get_document_false_method():
    response = client.delete("/document/get/hello")
    assert response.status_code == 405
    assert response.json() == {
        'detail': 'Method Not Allowed'
    }


def test_delete_document_false_method():
    response = client.get("/document/delete/123")
    assert response.status_code == 405
    assert response.json() == {
        'detail': 'Method Not Allowed'
    }
