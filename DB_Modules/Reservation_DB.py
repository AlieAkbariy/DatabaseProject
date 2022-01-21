import random


def get_room_with(cursor, from_date, to_date, room_type):
    if room_type == 'All':
        sql_query = ''' select top(100) Room.id,Room.room_floor,Room.maximum_capacity,Room.price_per_night,
         RoomType.no_bed , RoomType.name_type from Room,RoomType where Room.rt_id = RoomType.id and Room.rs_id = 2 and 
         Room.id not in 
         (select ReservationDetails.room_id from ReservationDetails, Reservation where
         ReservationDetails.reservation_id = Reservation.id and 
         ((Reservation.reserve_date >= ? and Reservation.reserve_date <= ?) or
          (Reservation.reserve_date <=? and Reservation.checkout_date >= ?)))

    '''
        sql_output = cursor.execute(sql_query, (from_date, to_date, from_date, from_date))

    else:
        sql_query = ''' select top(100) Room.id,Room.room_floor,Room.maximum_capacity,Room.price_per_night,
                 RoomType.no_bed , RoomType.name_type from Room,RoomType where Room.rt_id = RoomType.id and
                  Room.rs_id = 2 and 
                 RoomType.name_type = ? and Room.id 
                 not in (select ReservationDetails.room_id from ReservationDetails, Reservation where
                 ReservationDetails.reservation_id = Reservation.id and 
                 ((Reservation.reserve_date >= ? and Reservation.reserve_date <= ?) or 
                 (Reservation.reserve_date <=? and Reservation.checkout_date >= ?)))

            '''
        sql_output = cursor.execute(sql_query, (room_type, from_date, to_date, from_date, from_date))

    return sql_output


def make_reservation(conn, cursor, user_id, from_date, to_date, no_night):
    get_staff_count = '''select StaffInformation.id from StaffInformation where
     StaffInformation.staff_role = ?
     '''
    staff_ids = cursor.execute(get_staff_count, ('Receptionist',))
    length = 0
    for i in staff_ids:
        length += 1
    random_staff = random.randint(1, length)
    i = 1
    staff_ids = cursor.execute(get_staff_count, ('Receptionist',))
    for id in staff_ids:
        if i == random_staff:
            random_id = id[0]
        i += 1

    sql_query = '''insert into Reservation (g_id,bs_id,staff_id,checkin_date,checkout_date,reserve_date,no_nights)
     values(?,?,?,?,?,?,?)

    '''
    cursor.execute(sql_query, (int(user_id), 2, random_id, from_date, to_date, from_date, no_night))
    conn.commit()


def get_reservation_from_database(cursor, user_id, from_date, no_nightٍ):
    query = '''select Reservation.id from Reservation where Reservation.g_id = ?
    and Reservation.bs_id = ? and Reservation.reserve_date = ? and Reservation.no_nights = ?

    '''
    reservation_id = cursor.execute(query, (int(user_id), 2, from_date, no_nightٍ)).fetchone()

    return int(reservation_id[0])


def reservation_details(conn, cursor, reservation_id, room_id, extra_facilities):
    sql_query = '''insert into ReservationDetails(reservation_id,room_id , extra_facilities) values(?,?,?)
        '''
    cursor.execute(sql_query, reservation_id, room_id, extra_facilities)
    conn.commit()


def update_room_status(conn, cursor, room_id):
    sql_quary = '''update Room set Room.rs_id = 1 where Room.id = ?'''
    cursor.execute(sql_quary, (room_id,))
    conn.commit()


def add_people_to_database(conn, cursor, reservation_id, first_name, last_name, national_id, gender):
    sql_query = ''' insert into People (r_id , first_name, last_name, national_id, gender)
    values (?,?,?,?,?)
    '''
    cursor.execute(sql_query, (reservation_id, first_name, last_name, national_id, gender))
    conn.commit()


def get_rooms_with_reserve_id(cursor, reservation_id):
    sql_query = '''select ReservationDetails.room_id from ReservationDetails
    where ReservationDetails.reservation_id = ?
    '''
    rooms = cursor.execute(sql_query, (reservation_id,))
    return rooms


def get_reservation_id_from_database(cursor, user_id):
    sql_query = '''select * from Reservation where g_id = ? order by id desc 
    '''
    if user_id != 0:
        try:
            res_id = cursor.execute(sql_query, (user_id,)).fetchone()[0]
            return res_id
        except:
            return '0'
    else:
        return '0'


def get_reservation_details_id(cursor, room_id, reservation_id):
    sql_query = '''select ReservationDetails.id from ReservationDetails where ReservationDetails.reservation_id = ? and 
        ReservationDetails.room_id = ?
    '''
    reservation_details_id = int(cursor.execute(sql_query, (reservation_id, room_id)).fetchone()[0])
    return reservation_details_id


def get_all_reservation_from_database(cursor, user_id, reservation_id):
    sql_query = '''select Reservation.g_id,Reservation.reserve_date,Reservation.no_nights,ReservationDetails.room_id,
    ReservationDetails.extra_facilities from Reservation,ReservationDetails
     where Reservation.id = ReservationDetails.reservation_id and Reservation.id = ?
     and Reservation.g_id = ? 
    '''
    reservations = cursor.execute(sql_query, (reservation_id, user_id))
    return reservations


def check_status_from_database(cursor, reservation_id):
    if reservation_id != 0:
        sql_query = '''select Reservation.bs_id from Reservation where Reservation.id = ?
        '''
        status = cursor.execute(sql_query, (reservation_id,)).fetchone()[0]
        return int(status)
    else:
        return 2
