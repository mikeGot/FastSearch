from loguru import logger
import psycopg2
from psycopg2 import errors

# from parser import Document

# параметры в переменные окружения
import config


# serial == autoincrement
def create_table():
    conn = psycopg2.connect(user=config.db_user,
                            password=config.db_password,
                            host=config.db_host,
                            port=config.db_port,
                            dbname=config.db_name
                            )

    cursor = conn.cursor()
    try:
        cursor.execute("create table document(\
            id integer primary key,\
            rubrics text [],\
            text text,\
            created_date timestamp);")

        conn.commit()
        logger.info("Таблица успешно создалась")

    except errors.lookup('42P07') as DuplicateTable:
        logger.info("Таблица уже создана")
        raise psycopg2.IntegrityError

    except Exception as e:
        logger.exception(e)

    finally:
        cursor.close()
        conn.close()


# use "executemany" as a variant
def insert_data(list_of_doc):
    conn = psycopg2.connect(user=config.db_user,
                            password=config.db_password,
                            host=config.db_host,
                            port=config.db_port,
                            dbname=config.db_name
                            )
    doc_tuple = tuple([(doc.id, doc.rubrics, doc.text, doc.created_date) for doc in list_of_doc])
    cursor = conn.cursor()
    try:
        query = "INSERT INTO public.document (id, rubrics, text, created_date ) VALUES (%s, %s, %s, TIMESTAMP %s)"
        cursor.executemany(query, doc_tuple)
        conn.commit()
        logger.info("Данные успешно импортировались в БД")

    except Exception as e:
        logger.exception(e)

    finally:
        cursor.close()
        conn.close()


def delete_data(doc_id):
    conn = psycopg2.connect(user=config.db_user,
                            password=config.db_password,
                            host=config.db_host,
                            port=config.db_port,
                            dbname=config.db_name
                            )
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM public.document WHERE id=%s", str(doc_id))
        conn.commit()

    except Exception as e:
        logger.exception(e)

    finally:
        cursor.close()
        conn.close()


def select_data(tuple_of_id: tuple):
    conn = psycopg2.connect(user=config.db_user,
                            password=config.db_password,
                            host=config.db_host,
                            port=config.db_port,
                            dbname=config.db_name
                            )
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM public.document WHERE id IN %s ORDER BY created_date;", (tuple(tuple_of_id), ))
        all_id = cursor.fetchall()
        return all_id
    except Exception as e:
        logger.exception(e)
        raise psycopg2.ProgrammingError

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    try:
        create_table()
    except Exception:
        logger.info("Таблица уже созданна")

