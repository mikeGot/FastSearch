from loguru import logger
import psycopg2
from psycopg2 import errors

# from parser import Document

# параметры в переменные окружения
conn = psycopg2.connect(user="postgres",
                        password="postgres",
                        host="192.168.1.103",
                        port="5432",
                        dbname="postgres"
                        )


# serial == autoincrement
def create_table():
    cursor = conn.cursor()
    try:
        cursor.execute("create table document(\
            id integer primary key,\
            rubrics text [],\
            text text,\
            created_date timestamp);", )

        conn.commit()
        logger.info("Таблица успешно создалась")

    except errors.lookup('42P07') as DuplicateTable:
        logger.info("Таблица уже создана")

    except Exception as e:
        logger.exception(e)

    finally:
        cursor.close()


def insert_data(doc):
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO public.document (id, rubrics, text, created_date ) \
        VALUES (%s, %s, %s, TIMESTAMP %s)", (doc.id, doc.rubrics, doc.text, doc.created_date))
        conn.commit()

    except Exception as e:
        logger.exception(e)

    finally:
        cursor.close()


# def select_data():
#     try:
#         cursor.execute(f"SELECT id FROM public.document")
#         all_id = cursor.fetchall()
#         logger.info(all_id)
#     except Exception as e:
#         logger.exception(e)
#
#     finally:
#         cursor.close()
#         conn.close()
#         print("Соединение с PostgreSQL закрыто")


if __name__ == "__main__":
    pass
    # try:
    #     create_table()
    # except Exception:
    #     logger.info("Таблица уже созданна")

