from DB_Modules.DataBaseConnection import fetchone, fetchoneObject


def get_restaurants_from_database(cursor):
    sql_query = 'select * from ResturantCoffeeShop'
    cursor.execute(sql_query)
    return cursor


def get_all_foods_from_database(cursor, restaurant_id):
    sql_query = '''select Food.id , Food.food_name , Food.food_price , Food.food_ingredients ,
    Food.food_type from Food where Food.resturant_id = %s 

    '''
    cursor.execute(sql_query, (restaurant_id,))
    return cursor


def search_food_from_database(cursor, restaurant_id, search_word):
    sql_query = '''select Food.id , Food.food_name , Food.food_price , Food.food_ingredients ,
    Food.food_type from Food where Food.resturant_id = %s and Food.food_name like %s
    '''
    cursor.execute(sql_query, (restaurant_id, '%' + search_word + '%'))
    return cursor


def get_foods_with_id(cursor, restaurant_id, food_id):
    sql_query = '''select Food.id , Food.food_name , Food.food_price , Food.food_ingredients ,
    Food.food_type from Food where Food.resturant_id = %s and Food.id = %s 
    '''
    cursor.execute(sql_query, (restaurant_id, food_id))
    food = fetchoneObject(cursor)
    return food


def food_order_submit(conn, cursor, reservation_details_id, serve_in):
    sql_query = '''insert into FoodOrder(rd_id,flag) values(%s,%s)
    '''
    cursor.execute(sql_query, (reservation_details_id, serve_in))
    conn.commit()


def get_food_order_id(cursor, reservation_details_id, serve_in):
    sql_query = ''' select FoodOrder.id from FoodOrder where FoodOrder.rd_id = %s and FoodOrder.flag = %s    
        '''
    cursor.execute(sql_query, (reservation_details_id, serve_in))
    food_order_id = int(fetchone(cursor))
    return food_order_id


def create_food_interface(conn, cursor, foods, food_order_id):
    sql_query = '''insert into FoodInterface(fd_id,f_id) values(%s,%s)'''
    for i in foods:
        cursor.execute(sql_query, (food_order_id, i))
        conn.commit()


def get_foods_from_database(cursor, reservation_id):
    sql_query = '''select Food.id , Food.food_name , Food.food_price , Food.food_ingredients ,
    Food.food_type from Food,FoodInterface,FoodOrder where Food.id = FoodInterface.f_id
     and FoodInterface.fd_id = FoodOrder.id and FoodOrder.rd_id in
      (select ReservationDetails.id from ReservationDetails where ReservationDetails.reservation_id = %s)
    '''
    cursor.execute(sql_query, (reservation_id,))
    return cursor
