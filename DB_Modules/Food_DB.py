def get_restaurants_from_database(cursor):
    sql_query = 'select * from ResturantCoffeeShop'
    restaurants = cursor.execute(sql_query)
    return restaurants


def get_all_foods_from_database(cursor, restaurant_id):
    sql_query = '''select Food.id , Food.food_name , Food.food_price , Food.food_ingredients ,
    Food.food_type from Food where Food.resturant_id = ? 

    '''
    foods = cursor.execute(sql_query, (restaurant_id,))
    return foods


def search_food_from_database(cursor, restaurant_id, search_word):
    sql_query = '''select Food.id , Food.food_name , Food.food_price , Food.food_ingredients ,
    Food.food_type from Food where Food.resturant_id = ? and Food.food_name like ?
    '''
    foods = cursor.execute(sql_query, (restaurant_id, '%' + search_word + '%'))
    return foods


def get_foods_with_id(cursor, restaurant_id, food_id):
    sql_query = '''select Food.id , Food.food_name , Food.food_price , Food.food_ingredients ,
    Food.food_type from Food where Food.resturant_id = ? and Food.id = ? 
    '''
    food = cursor.execute(sql_query, (restaurant_id, food_id)).fetchone()
    return food


def food_order_submit(conn, cursor, reservation_details_id, serve_in):
    sql_query = '''insert into FoodOrder values(?,?)
    '''
    cursor.execute(sql_query, (reservation_details_id, serve_in))
    conn.commit()


def get_food_order_id(cursor, reservation_details_id, serve_in):
    sql_query = ''' select FoodOrder.id from FoodOrder where FoodOrder.rd_id = ? and FoodOrder.flag = ?    
        '''
    food_order_id = int(cursor.execute(sql_query, (reservation_details_id, serve_in)).fetchone()[0])
    return food_order_id


def create_food_interface(conn, cursor, foods, food_order_id):
    sql_query = '''insert into FoodInterface values(?,?)'''
    for i in foods:
        cursor.execute(sql_query, (food_order_id, i))
        conn.commit()


def get_foods_from_database(cursor, reservation_id):
    sql_query = '''select Food.id , Food.food_name , Food.food_price , Food.food_ingredients ,
    Food.food_type from Food,FoodInterface,FoodOrder where Food.id = FoodInterface.f_id
     and FoodInterface.fd_id = FoodOrder.id and FoodOrder.rd_id in
      (select ReservationDetails.id from ReservationDetails where ReservationDetails.reservation_id = ?)
    '''
    foods = cursor.execute(sql_query, (reservation_id,))
    return foods
