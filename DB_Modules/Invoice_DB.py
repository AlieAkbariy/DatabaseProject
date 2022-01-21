def get_nights(cursor, reservation_id):
    sql_query = '''select Reservation.no_nights from Reservation where
    Reservation.id = ?
    '''
    nights = cursor.execute(sql_query, (reservation_id,)).fetchone()[0]
    return int(nights)


def get_room_price(cursor, room_id):
    sql_query = '''select Room.price_per_night from Room where Room.id = ?'''
    price = cursor.execute(sql_query, (room_id)).fetchone()[0]
    return int(price)


def get_services_from_database(cursor, reservation_id):
    sql_query = '''select ReservationDetails.room_id from CleaningService,ReservationDetails where
     CleaningService.rd_id = ReservationDetails.id and CleaningService.rd_id in
          (select ReservationDetails.id from ReservationDetails where ReservationDetails.reservation_id = ?)
        '''
    services = cursor.execute(sql_query, (reservation_id,))
    return services


def create_bill_database(conn, cursor, reservation_id, total_amount):
    sql_quary = '''insert into Bill values (?,?,?)
    '''
    cursor.execute(sql_quary, (total_amount, 1, reservation_id))
    conn.commit()


def get_bill_id(cursor, reservation_id):
    sql_query = '''select Bill.id from Bill where Bill.reservation_id = ? order by Bill.id desc
    '''
    return cursor.execute(sql_query, (reservation_id,)).fetchone()



def update_bill(conn, cursor, id, total_amount):
    sql_quary = '''update Bill set Bill.total_amount = ? where Bill.id = ?'''
    cursor.execute(sql_quary, (total_amount, id))
    conn.commit()
