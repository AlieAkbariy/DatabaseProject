from DB_Modules.DataBaseConnection import fetchone, fetchoneObject


def get_nights(cursor, reservation_id):
    sql_query = '''select Reservation.no_nights from Reservation where
    Reservation.id = %s
    '''
    cursor.execute(sql_query, (reservation_id,))
    nights = fetchone(cursor)
    return int(nights)


def get_room_price(cursor, room_id):
    sql_query = '''select Room.price_per_night from Room where Room.id = %s'''
    cursor.execute(sql_query, (room_id,))
    price = fetchone(cursor)
    return int(price)


def get_services_from_database(cursor, reservation_id):
    sql_query = '''select ReservationDetails.room_id from CleaningService,ReservationDetails where
     CleaningService.rd_id = ReservationDetails.id and CleaningService.rd_id in
          (select ReservationDetails.id from ReservationDetails where ReservationDetails.reservation_id = %s)
        '''
    cursor.execute(sql_query, (reservation_id,))
    return cursor


def create_bill_database(conn, cursor, reservation_id, total_amount):
    sql_quary = '''insert into Bill(total_amount,bill_status,reservation_id) values (%s,%s,%s)
    '''
    cursor.execute(sql_quary, (total_amount, 1, reservation_id))
    conn.commit()


def get_bill_id(cursor, reservation_id):
    sql_query = '''select Bill.id from Bill where Bill.reservation_id = %s order by Bill.id desc
    '''
    cursor.execute(sql_query, (reservation_id,))
    temp = fetchoneObject(cursor)
    return temp


def update_bill(conn, cursor, id, total_amount):
    sql_quary = '''update Bill set Bill.total_amount = %s where Bill.id = %s'''
    cursor.execute(sql_quary, (total_amount, id))
    conn.commit()
