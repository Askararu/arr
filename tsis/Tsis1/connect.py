import psycopg2
from config import params

def connect():
    try:
        conn = psycopg2.connect(**params) # информэйшон из парамет
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"[Ошибка подключения]: {error}")
        return None