from PyQt5 import QtWidgets

from DB_Modules.DataBaseConnection import connect_to_database
from DB_Modules.Reservation_DB import get_room_with, make_reservation, get_all_reservation_from_database, \
    reservation_details, add_people_to_database, get_reservation_id_from_database, get_reservation_from_database, \
    check_status_from_database, update_room_status


class Reservation:
    reservation_id = 0
    room_id = 0
    room_id_list = []
    status = 2

    def __init__(self, user_id=0):
        conn, cursor = connect_to_database()
        self.reservation_id = int(get_reservation_id_from_database(cursor, user_id))

    def get_rooms(self, parent_class, from_date, to_date, room_type):
        conn, cursor = connect_to_database()
        if len(from_date) == 0 or len(to_date) == 0 and len(room_type) == 0:
            parent_class.error.setText('Please input Fields')

        else:
            sql_output = get_room_with(cursor, from_date, to_date, room_type)
            print(sql_output)
            parent_class.rooms.setRowCount(0)
            parent_class.rooms.setRowCount(100)
            table_row = 0
            for row in sql_output:
                parent_class.rooms.setItem(table_row, 0, QtWidgets.QTableWidgetItem(str(row[0])))
                parent_class.rooms.setItem(table_row, 1, QtWidgets.QTableWidgetItem(str(row[1])))
                parent_class.rooms.setItem(table_row, 2, QtWidgets.QTableWidgetItem(str(row[2])))
                parent_class.rooms.setItem(table_row, 3, QtWidgets.QTableWidgetItem(str(row[3])))
                parent_class.rooms.setItem(table_row, 4, QtWidgets.QTableWidgetItem(str(row[4])))
                parent_class.rooms.setItem(table_row, 5, QtWidgets.QTableWidgetItem(row[5]))
                table_row += 1

    def room_reservation(self, user_id, room_id, from_date, to_date, no_night):
        conn, cursor = connect_to_database()
        self.room_id = room_id
        self.room_id_list.append(room_id)
        if self.reservation_id == 0:
            make_reservation(conn, cursor, user_id, from_date, to_date, no_night)
            self.reservation_id = get_reservation_from_database(cursor, user_id, from_date, no_night)

    def create_reservation_details(self, extra_facilities):
        conn, cursor = connect_to_database()
        reservation_details(conn, cursor, self.reservation_id, self.room_id, extra_facilities)
        update_room_status(conn, cursor, self.room_id)

    def create_people(self, first_name, last_name, national_id, gender):
        conn, cursor = connect_to_database()
        add_people_to_database(conn, cursor, self.reservation_id, first_name, last_name, national_id, gender)

    def check_status(self):
        conn, cursor = connect_to_database()
        status = check_status_from_database(cursor, self.reservation_id)
        self.status = status

    def get_all_reservation(self, parent_class, user_id):
        conn, cursor = connect_to_database()
        reservations = get_all_reservation_from_database(cursor, user_id, self.reservation_id)
        table_row = 0
        for row in reservations:
            parent_class.reservation.setItem(table_row, 0, QtWidgets.QTableWidgetItem(str(row[0])))
            parent_class.reservation.setItem(table_row, 1, QtWidgets.QTableWidgetItem(str(row[1])))
            parent_class.reservation.setItem(table_row, 2, QtWidgets.QTableWidgetItem(str(row[2])))
            parent_class.reservation.setItem(table_row, 3, QtWidgets.QTableWidgetItem(str(row[3])))
            parent_class.reservation.setItem(table_row, 4, QtWidgets.QTableWidgetItem(row[4]))
            table_row += 1
