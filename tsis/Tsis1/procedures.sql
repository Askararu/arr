-- Процедура 1: Добавление телефона к контакту
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE 
    v_id INT;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE first_name = p_contact_name OR last_name = p_contact_name LIMIT 1;
    IF v_id IS NOT NULL THEN
        INSERT INTO phones (contact_id, phone, type) VALUES (v_id, p_phone, p_type);
    ELSE
        RAISE NOTICE 'Контакт % не найден', p_contact_name;
    END IF;
END; $$;

-- Процедура 2: Перенос контакта в группу
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE 
    v_group_id INT;
BEGIN
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    UPDATE contacts SET group_id = v_group_id WHERE first_name = p_contact_name OR last_name = p_contact_name;
END; $$;

-- Функция 3: Расширенный поиск
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(contact_id INT, full_name TEXT, contact_email VARCHAR, phone_num VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT c.id, (c.first_name || ' ' || COALESCE(c.last_name, '')), c.email, p.phone
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_query || '%' 
       OR c.last_name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END; $$ LANGUAGE plpgsql;