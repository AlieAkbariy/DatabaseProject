from PyQt5.QtWidgets import QTableWidgetItem

from DB_Modules.DataBaseConnection import connect_to_database
from DB_Modules.Food_DB import get_restaurants_from_database, get_foods_from_database, search_food_from_database, \
    get_foods_with_id, create_food_interface, get_food_order_id, get_all_foods_from_database, food_order_submit
from DB_Modules.Reservation_DB import get_rooms_with_reserve_id, get_reservation_details_id


class Restaurants:
    restaurant_id = 0
    foods = []

    def show_all_restaurants(self, parent_class):
        conn, cursor = connect_to_database()
        restaurants = get_restaurants_from_database(cursor)
        table_row = 0
        for row in restaurants:
            parent_class.restaurants.setItem(table_row, 0, QTableWidgetItem(str(row[0])))
            parent_class.restaurants.setItem(table_row, 1, QTableWidgetItem(row[1]))
            parent_class.restaurants.setItem(table_row, 2, QTableWidgetItem(row[2]))
            table_row += 1

    def select_restaurants(self, parent_class, id):
        if len(id) == 0:
            parent_class.error.setText('Please Enter Id!')
        else:
            self.restaurant_id = int(id)

    def restaurant_all_foods(self, parent_class):
        conn, cursor = connect_to_database()
        foods = get_all_foods_from_database(cursor, self.restaurant_id)
        parent_class.foods.setRowCount(0)
        parent_class.foods.setRowCount(100)
        table_row = 0
        for row in foods:
            parent_class.foods.setItem(table_row, 0, QTableWidgetItem(str(row[0])))
            parent_class.foods.setItem(table_row, 1, QTableWidgetItem(row[1]))
            parent_class.foods.setItem(table_row, 2, QTableWidgetItem(row[2]))
            parent_class.foods.setItem(table_row, 3, QTableWidgetItem(row[3]))
            parent_class.foods.setItem(table_row, 4, QTableWidgetItem(row[4]))
            table_row += 1

    def search_food_with_name(self, parent_class, search_word):
        conn, cursor = connect_to_database()
        foods = search_food_from_database(cursor, self.restaurant_id, search_word)
        table_row = 0
        parent_class.foods.setRowCount(0)
        parent_class.foods.setRowCount(100)
        for row in foods:
            parent_class.foods.setItem(table_row, 0, QTableWidgetItem(str(row[0])))
            parent_class.foods.setItem(table_row, 1, QTableWidgetItem(row[1]))
            parent_class.foods.setItem(table_row, 2, QTableWidgetItem(row[2]))
            parent_class.foods.setItem(table_row, 3, QTableWidgetItem(row[3]))
            parent_class.foods.setItem(table_row, 4, QTableWidgetItem(row[4]))
            table_row += 1

    def set_foods(self, foods):
        self.foods = foods

    def foods_list(self, parent_class):
        conn, cursor = connect_to_database()
        parent_class.foods.setRowCount(0)
        parent_class.foods.setRowCount(100)
        for i in range(len(self.foods)):
            food = get_foods_with_id(cursor, self.restaurant_id, self.foods[i])
            parent_class.foods.setItem(i, 0, QTableWidgetItem(str(food[0])))
            parent_class.foods.setItem(i, 1, QTableWidgetItem(food[1]))
            parent_class.foods.setItem(i, 2, QTableWidgetItem(food[2]))
            parent_class.foods.setItem(i, 3, QTableWidgetItem(food[3]))
            parent_class.foods.setItem(i, 4, QTableWidgetItem(food[4]))

    def rooms_list(self, parent_class, reservation_id):
        conn, cursor = connect_to_database()
        rooms = get_rooms_with_reserve_id(cursor, reservation_id)
        table_row = 0
        for row in rooms:
            parent_class.rooms.setItem(table_row, 0, QTableWidgetItem(str(row[0])))
            table_row += 1

    def order_confirmed(self, parent_class, reservation_id, room_id, serve_in):
        conn, cursor = connect_to_database()
        reservation_details_id = get_reservation_details_id(cursor, room_id, reservation_id)
        food_order_submit(conn, cursor, reservation_details_id, serve_in)
        food_order_id = get_food_order_id(cursor, reservation_details_id, serve_in)
        create_food_interface(conn, cursor, self.foods, food_order_id)

    def get_all_foods(self, parent_class, reservation_id):
        conn, cursor = connect_to_database()
        foods = get_foods_from_database(cursor, reservation_id)
        table_row = 0
        for row in foods:
            parent_class.foods.setItem(table_row, 0, QTableWidgetItem(str(row[0])))
            parent_class.foods.setItem(table_row, 1, QTableWidgetItem(row[1]))
            parent_class.foods.setItem(table_row, 2, QTableWidgetItem(str(row[2])))
            parent_class.foods.setItem(table_row, 3, QTableWidgetItem(row[3]))
            parent_class.foods.setItem(table_row, 4, QTableWidgetItem(row[4]))
            table_row += 1
