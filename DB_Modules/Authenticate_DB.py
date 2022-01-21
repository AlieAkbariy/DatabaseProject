def get_user_password(cursor, user_name):
    sql_query = 'select g_password from Guest where national_id= ?'
    cursor.execute(sql_query, (user_name,))
    sql_pass = cursor.fetchone()
    return sql_pass


def create_user(conn, cursor, user_name, password):
    sql_query = 'insert into Guest (national_id,g_password) values (?,?)'
    cursor.execute(sql_query, (user_name, password))
    conn.commit()


def get_user_id(cursor, user_name, password):
    sql_query = ''' select Guest.id from Guest where Guest.national_id = ? and 
    Guest.g_password = ?
    '''
    user_id = cursor.execute(sql_query, (user_name, password)).fetchone()
    return int(user_id[0])


def complete_user_information(conn, cursor, user_name, first_name, last_name, phone_number, address, birth_date,
                              gender):
    sql_query = '''update Guest set first_name = ? , last_name = ? , phone_number = ? ,
        guest_address = ? , birth_date = ? , gender = ? where id = ? 

    '''
    cursor.execute(sql_query, (first_name, last_name, phone_number, address, birth_date, gender, user_name))
    conn.commit()
