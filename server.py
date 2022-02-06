import datetime
from typing import List
from loguru import logger
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi

import db
import elastic

app = FastAPI()


class Document(BaseModel):
    id: int
    rubrics: List[str]
    text: str
    created_date: datetime.datetime


class DocResponse(BaseModel):
    result: List[Document]


class DeleteResponse(BaseModel):
    result: str
    doc_id: int



def my_schema():
    openapi_schema = get_openapi(
        title="This is a FastSearch app",
        version="1.0",
        description="You can search some info and delete files",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = my_schema


@app.get('/document/get/{text_query}', response_model=DocResponse)
def get_documents(text_query: str):
    id_list = elastic.search(user_query=text_query)
    if len(id_list):
        selected_data = db.select_data(id_list)
        result_list = list()

        for data in selected_data:
            parameters = ["id", "rubrics", "text", "created_date"]
            data_dict = dict(zip(parameters, data))

            result_list.append(data_dict)

        return {"result": result_list}
        # return result_list
    else:
        raise HTTPException(status_code=404, detail="Document not found")


# удаление с помощью метода delete
@app.delete("/document/delete/{doc_id}", response_model=DeleteResponse)
def delete_document(doc_id: int):
    try:
        elastic.delete(doc_id)
        db.delete_data(doc_id)

        return {"result": "success", "doc_id": doc_id}
    except IndexError as ie:
        logger.exception(ie)
        raise HTTPException(status_code=404, detail="Invalid ID")

# удаление с помощью метода post
# @app.post("/document/{doc_id}")
# def delete_document_delete(doc_id):
#     try:
#         elastic.delete(doc_id)
#         return {"result": {"status": "success", "doc_id": doc_id}}
#     except IndexError as ie:
#         logger.exception(ie)
#         return {"result": {"status": "error", "reason": "Invalid ID"}}


# if __name__ == "__main__":
#     app.run(debug=True, host=config.server_host, port=config.server_port)
