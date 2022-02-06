import parser
import db
import elastic

list_of_documents = parser.parse_csv("posts.csv")


db.create_table()

db.insert_data(list_of_documents)


elastic.create_index()

elastic.put(list_of_documents)

