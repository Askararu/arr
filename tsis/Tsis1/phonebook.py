import json
import csv
from connect import connect

def export_to_json(filename="contacts_exported.json"):
    conn = connect()
    if not conn: return
    cur = conn.cursor()
    cur.execute("""
        SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name,
               ARRAY_AGG(p.phone || ':' || p.type) 
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, g.name
    """)
    rows = cur.fetchall()
    data = []
    for r in rows:
        data.append({
            "name": f"{r[1]} {r[2] if r[2] else ''}".strip(),
            "email": r[3],
            "birthday": str(r[4]) if r[4] else None,
            "group": r[5],
            "phones": r[6] if r[6] != [None] else []
        })
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"[*] Данные экспортированы в {filename}")
    conn.close()

def import_from_json(filename="contacts_import.json"):
    conn = connect()
    if not conn: return
    cur = conn.cursor()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            contacts = json.load(f)
            for c in contacts:
                name_parts = c['name'].split()
                f_name = name_parts[0]
                l_name = name_parts[1] if len(name_parts) > 1 else None

                cur.execute("SELECT id FROM contacts WHERE first_name = %s", (f_name,))
                exists = cur.fetchone()
                
                if exists:
                    ans = input(f"Контакт {c['name']} уже существует. Перезаписать? (y/n): ")
                    if ans.lower() != 'y': 
                        continue
                    cur.execute("DELETE FROM contacts WHERE id = %s", (exists[0],))
                
                
                cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (c['group'],))
                cur.execute("SELECT id FROM groups WHERE name = %s", (c['group'],))
                grp_id = cur.fetchone()[0]

                # Вставляем контакт
                cur.execute("""
                    INSERT INTO contacts (first_name, last_name, email, birthday, group_id) 
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """, (f_name, l_name, c['email'], c['birthday'], grp_id))
                new_id = cur.fetchone()[0]
                
                # Вставляем телефоны
                if c.get('phones'):
                    for p in c['phones']:
                        if p:
                            ph, pt = p.split(':')
                            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)", (new_id, ph, pt))
        conn.commit()
        print("[*] Импорт из JSON завершен!")
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
    finally:
        conn.close()

def import_from_csv(filename='contacts.csv'):
    conn = connect()
    if not conn: return
    cur = conn.cursor()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute("INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING", (row['group_name'],))
                cur.execute("SELECT id FROM groups WHERE name = %s", (row['group_name'],))
                group_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO contacts (first_name, last_name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """, (row['first_name'], row['last_name'], row['email'], row['birthday'], group_id))
                contact_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO phones (contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (contact_id, row['phone'], row['phone_type']))
        conn.commit()
        print("[*] Данные из CSV успешно импортированы!")
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
    finally:
        conn.close()

def show_with_pagination(limit=2):
    conn = connect()
    if not conn: return
    cur = conn.cursor()
    offset = 0
    while True:
        cur.execute("SELECT id, first_name, last_name, email FROM contacts ORDER BY id LIMIT %s OFFSET %s", (limit, offset))
        rows = cur.fetchall()
        print("\n--- Контакты ---")
        if not rows:
            print("(Пусто)")
        for r in rows: 
            print(f"[{r[0]}] {r[1]} {r[2] if r[2] else ''} - {r[3]}")
        
        cmd = input("\n[n]ext (вперед), [p]rev (назад), [q]uit (выход): ").lower()
        if cmd == 'n' and len(rows) == limit: offset += limit
        elif cmd == 'p': offset = max(0, offset - limit)
        elif cmd == 'q': break
    conn.close()

def search_database(query):
    conn = connect()
    if not conn: return
    cur = conn.cursor()
    # Вызов хранимой функции PostgreSQL
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()
    print("\n--- Результаты поиска ---")
    for r in rows:
        print(f"ID: {r[0]} | Имя: {r[1]} | Email: {r[2]} | Телефон: {r[3]}")
    conn.close()

def menu():
    while True:
        print("\n=== PHONEBOOK MENU ===")
        print("1. Показать контакты (Пагинация)")
        print("2. Импорт из CSV")
        print("3. Импорт из JSON")
        print("4. Экспорт в JSON")
        print("5. Расширенный поиск")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == '1':
            show_with_pagination()
        elif choice == '2':
            import_from_csv()
        elif choice == '3':
            import_from_json()
        elif choice == '4':
            export_to_json()
        elif choice == '5':
            q = input("Введите имя, email или телефон для поиска: ")
            search_database(q)
        elif choice == '0':
            print("Выход из программы.")
            break
        else:
            print("Неверный ввод.")

if __name__ == "__main__":
    menu()