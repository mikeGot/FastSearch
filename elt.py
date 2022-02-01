from loguru import logger

import parser
import db
import elastic

list_of_documents = parser.parse_csv("posts.csv")


db.create_table()

for d in list_of_documents:
    db.insert_data(d)
logger.info("Данные успешно импортировались в БД")

elastic.create_index()

elastic.put_to_elastic(list_of_documents)

