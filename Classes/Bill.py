from PyQt5.QtWidgets import QTableWidgetItem

from DB_Modules.DataBaseConnection import connect_to_database
from DB_Modules.Food_DB import get_foods_from_database
from DB_Modules.Invoice_DB import get_services_from_database, get_nights, get_room_price, create_bill_database, \
    get_bill_id, update_bill
from DB_Modules.Reservation_DB import get_rooms_with_reserve_id


class Invoice:
    id = 0
    foods_price = 0
    rooms_price = 0
    services_price = 0
    total = 0

    def get_all_foods(self, parent_class, reservation_id):
        conn, cursor = connect_to_database()
        foods = get_foods_from_database(cursor, reservation_id)
        table_row = 0
        foods_price = 0
        for row in foods:
            parent_class.foods.setItem(table_row, 0, QTableWidgetItem(str(row[0])))
            parent_class.foods.setItem(table_row, 1, QTableWidgetItem(row[1]))
            parent_class.foods.setItem(table_row, 2, QTableWidgetItem(str(row[2])))
            foods_price += row[2]
            table_row += 1

        self.foods_price = foods_price

    def get_all_rooms(self, parent_class, reservation_id):
        conn, cursor = connect_to_database()
        rooms = get_rooms_with_reserve_id(cursor, reservation_id)
        conn, cursor = connect_to_database()
        nights = get_nights(cursor, reservation_id)
        table_row = 0
        rooms_price = 0
        for row in rooms:
            parent_class.rooms.setItem(table_row, 0, QTableWidgetItem(str(row[0])))
            parent_class.rooms.setItem(table_row, 1, QTableWidgetItem(str(nights)))
            conn, cursor = connect_to_database()
            price = get_room_price(cursor, row[0])
            rooms_price += price * nights
            parent_class.rooms.setItem(table_row, 2, QTableWidgetItem(str(price)))
            table_row += 1

        self.rooms_price = rooms_price

    def get_services(self, parent_class, reservation_id):
        conn, cursor = connect_to_database()
        services = get_services_from_database(cursor, reservation_id)
        table_row = 0
        services_price = 0
        for row in services:
            parent_class.services.setItem(table_row, 0, QTableWidgetItem(str(row[0])))
            parent_class.services.setItem(table_row, 1, QTableWidgetItem('100000'))
            services_price += 100000
            table_row += 1
        self.services_price = services_price

    def set_total(self):
        self.total = self.services_price + self.rooms_price + self.foods_price

    def submit_bill(self, reservation_id):
        conn, cursor = connect_to_database()
        if get_bill_id(cursor, reservation_id) is None:
            self.id = 0
        else:
            self.id = get_bill_id(cursor, reservation_id)[0]
        if self.id == 0:
            create_bill_database(conn, cursor, reservation_id, self.total)
        else:
            update_bill(conn, cursor, self.id, self.total)
