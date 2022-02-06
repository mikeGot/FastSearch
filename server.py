from flask import Flask
from loguru import logger
import db
import elastic

app = Flask(__name__)


@app.route('/document/<text_query>')
def get_documents(text_query):
    id_list = elastic.search(user_query=text_query)
    if len(id_list):
        selected_data = db.select_data(id_list)
        result_list = list()

        for data in selected_data:
            parameters = ["id", "rubrics", "text", "created_date"]
            data_dict = dict(zip(parameters, data))

            result_list.append(data_dict)

        return {"result": result_list}

    return {"result": None}


@app.get("/document/<int:doc_id>/delete")
def delete_document(doc_id):
    try:
        elastic.delete(doc_id)
        db.delete_data(doc_id)
        return {"result": {"status": "success", "doc_id": doc_id}}
    except IndexError as ie:
        logger.exception(ie)
        return {"result": {"status": "error", "reason": "Invalid ID"}}


# удаление с помощью метода delete
# @app.delete("/document/<int:doc_id>")
# def delete_document_delete(doc_id):
#     try:
#         elastic.delete(doc_id)
#         return {"result": {"status": "success", "doc_id": doc_id}}
#     except IndexError as ie:
#         logger.exception(ie)
#         return {"result": {"status": "error", "reason": "Invalid ID"}}


if __name__ == "__main__":
    app.run(debug=True)
