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

# use "execute many" as a variant
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


def delete_data(id):
    cursor = conn.cursor()
    try:
        cursor.execute(f"DELETE FROM public.document WHERE id=%s", str(id))
        conn.commit()

    except Exception as e:
        logger.exception(e)

    finally:
        cursor.close()


def select_data(tuple_of_id: tuple):
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM public.document WHERE id IN %s ORDER BY created_date;", (tuple_of_id, ))
        all_id = cursor.fetchall()
        return all_id
    except Exception as e:
        logger.exception(e)

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    a = select_data((1, 2))
    for i in a:
        print(i)
    # try:
    #     create_table()
    # except Exception:
    #     logger.info("Таблица уже созданна")

