import psycopg2
from connect import get_connection

def execute_sql_file(filename, conn):
    with open(filename, 'r') as file:
        sql = file.read()
    with conn.cursor() as cur:
        cur.execute(sql)
    conn.commit()

def call_procedure(conn, query, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params or ())
    conn.commit()

def fetch_query(conn, query, params=None):
    with conn.cursor() as cur:
        cur.execute(query, params or ())
        return cur.fetchall()


def menu():
    conn = get_connection()

    while True:
        print("\n1. Load SQL")
        print("2. Search")
        print("3. Add/Update user")
        print("4. Bulk insert")
        print("5. Pagination")
        print("6. Delete")
        print("7. Exit")

        choice = input("Choose: ")

        if choice == "1":
            execute_sql_file("functions.sql", conn)
            execute_sql_file("procedures.sql", conn)
            print("SQL loaded")

        elif choice == "2":
            pattern = input("Enter pattern: ")
            rows = fetch_query(conn, "SELECT * FROM search_phonebook(%s)", (pattern,))
            for r in rows:
                print(r)

        elif choice == "3":
            name = input("Name: ")
            phone = input("Phone: ")
            call_procedure(conn, "CALL upsert_user(%s, %s)", (name, phone))

        elif choice == "4":
            names = input("Names (comma separated): ").split(',')
            phones = input("Phones (comma separated): ").split(',')
            call_procedure(conn, "CALL bulk_insert_users(%s, %s)", (names, phones))

        elif choice == "5":
            limit = int(input("Limit: "))
            offset = int(input("Offset: "))
            rows = fetch_query(conn, "SELECT * FROM get_phonebook_paginated(%s, %s)", (limit, offset))
            for r in rows:
                print(r)

        elif choice == "6":
            name = input("Name (or empty): ")
            phone = input("Phone (or empty): ")
            call_procedure(conn, "CALL delete_user(%s, %s)", (name or None, phone or None))

        elif choice == "7":
            break

    conn.close()


if __name__ == "__main__":
    menu()