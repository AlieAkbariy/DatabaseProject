def add_cleaning_service_database(conn, cursor, reservation_details_id, cleaning_time, cleaning_date,
                                  cleaning_description):
    sql_query = '''insert into CleaningService(staff_id,rd_id,cleaning_time,cleaning_date,cleaning_description)
    values (%s,%s,%s,%s,%s)
    '''
    cursor.execute(sql_query, (1, reservation_details_id, cleaning_time, cleaning_date, cleaning_description))
    conn.commit()
