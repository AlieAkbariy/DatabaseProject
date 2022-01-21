from DB_Modules.DataBaseConnection import fetchone, fetchoneObject


def get_user_password(cursor, user_name):
    sql_query = 'select g_password from Guest where national_id= %s'
    cursor.execute(sql_query, (user_name,))
    sql_pass = fetchoneObject(cursor)
    return sql_pass


def create_user(conn, cursor, user_name, password):
    sql_query = 'insert into Guest (national_id,g_password) values (%s,%s)'
    cursor.execute(sql_query, (user_name, password))
    conn.commit()


def get_user_id(cursor, user_name, password):
    sql_query = ''' select Guest.id from Guest where Guest.national_id = %s and 
    Guest.g_password = %s
    '''
    cursor.execute(sql_query, (user_name, password))
    user_id = fetchone(cursor)
    return int(user_id)


def complete_user_information(conn, cursor, user_name, first_name, last_name, phone_number, address, birth_date,
                              gender):
    sql_query = '''update Guest set first_name = %s , last_name = %s , phone_number = %s ,
        guest_address = %s , birth_date = %s , gender = %s where id = %s 

    '''
    cursor.execute(sql_query, (first_name, last_name, phone_number, address, birth_date, gender, user_name))
    conn.commit()
