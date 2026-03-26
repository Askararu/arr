import csv
from connect import connect

def insert_console(name, phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()

def insert_csv():
    conn = connect()
    cur = conn.cursor()

    with open("contacts.csv", "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            cur.execute("INSERT INTO contacts (name, phone) VALUES (%s, %s)", (row[0], row[1]))

    conn.commit()
    cur.close()
    conn.close()

def update_user(name, new_name=None, new_phone=None):
    conn = connect()
    cur = conn.cursor()

    if new_name:
        cur.execute("UPDATE contacts SET name=%s WHERE name=%s", (new_name, name))
    if new_phone:
        cur.execute("UPDATE contacts SET phone=%s WHERE name=%s", (new_phone, name))

    conn.commit()
    cur.close()
    conn.close()

def view_all():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

def search(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM contacts WHERE name ILIKE %s", (f"%{name}%",))
    rows = cur.fetchall()

    for row in rows:
        print(row)

    cur.close()
    conn.close()

def delete(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute("DELETE FROM contacts WHERE name=%s", (name,))
    conn.commit()

    cur.close()
    conn.close()

def menu():
    while True:
        print("\n1. Insert (console)")
        print("2. Insert (CSV)")
        print("3. Update")
        print("4. View all")
        print("5. Search")
        print("6. Delete")
        print("7. Exit")

        choice = input("Choose: ")

        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            insert_console(name, phone)

        elif choice == "2":
            insert_csv()

        elif choice == "3":
            name = input("Old name: ")
            new_name = input("New name (or press enter): ")
            new_phone = input("New phone (or press enter): ")

            update_user(name,
                        new_name if new_name else None,
                        new_phone if new_phone else None)

        elif choice == "4":
            view_all()

        elif choice == "5":
            name = input("Search name: ")
            search(name)

        elif choice == "6":
            name = input("Delete name: ")
            delete(name)

        elif choice == "7":
            break

menu()