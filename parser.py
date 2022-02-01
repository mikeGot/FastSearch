import csv

import ast


class Document:
    def __init__(self, doc_id, rubrics, text, created_date):
        self.id = doc_id
        self.rubrics = rubrics
        self.text = text
        self.created_date = created_date


def csv_dict_reader(file_obj):
    """
    Read a CSV file using csv.DictReader
    """
    list_of_documents = list()
    reader = csv.DictReader(file_obj, delimiter=',')
    counter = 0
    for line in reader:
        doc = Document(doc_id=counter, rubrics=ast.literal_eval(line["rubrics"]), text=line["text"],
                       created_date=line["created_date"])
        list_of_documents.append(doc)
        counter += 1
    return list_of_documents


def parse_csv(filename) -> list:
    with open(filename) as f_obj:
        return csv_dict_reader(f_obj)


# if __name__ == "__main__":
#     with open("posts.csv") as f_obj:
#         csv_dict_reader(f_obj)

    # for d in list_of_documents:
    #     db.insert_data(d)

