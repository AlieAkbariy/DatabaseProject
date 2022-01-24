import sys

from PyQt5.QtWidgets import QApplication, QDialog, QLineEdit, QStackedWidget
from PyQt5.uic import loadUi

from Classes import Reserve
from Classes.Auth import Authenticate
from Classes.Bill import Invoice
from Classes.Cleaning import CleaningService
from Classes.Foods import Restaurants
from Classes.Reserve import Reservation


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("GUI/Authenticate_Screens/WelcomeScreen.ui", self)
        self.login.clicked.connect(self.go_to_login_screen)
        self.create_new_account.clicked.connect(self.go_to_signup_screen)

    def go_to_login_screen(self):
        login_screen = LoginScreen()
        widget.addWidget(login_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_signup_screen(self):
        signup_screen = CreateNewAccount()
        widget.addWidget(signup_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("GUI/Authenticate_Screens/Login.ui", self)
        self.password.setEchoMode(QLineEdit.Password)
        self.login.clicked.connect(self.log_in)

    def log_in(self):
        user_name = self.username.text()
        passsword = self.password.text()
        flag = auth.login(self, user_name, passsword)
        if flag:
            if Reserve.Reservation(auth.user_id) is not None:
                globals()['reserve'] = Reserve.Reservation(auth.user_id)
            main_menu = MainMenu()
            widget.addWidget(main_menu)
            widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateNewAccount(QDialog):
    def __init__(self):
        super(CreateNewAccount, self).__init__()
        loadUi("GUI/Authenticate_Screens/CreateNewAccount.ui", self)
        self.password.setEchoMode(QLineEdit.Password)
        self.confirmpassword.setEchoMode(QLineEdit.Password)
        self.signup.clicked.connect(self.sign_up)

    def sign_up(self):
        user_name = self.username.text()
        password = self.password.text()
        confirm_password = self.confirmpassword.text()
        flag = auth.signup(self, user_name, password, confirm_password)
        if flag:
            self.go_to_profile()

    def go_to_profile(self):
        fill_profile = FillProfile()
        widget.addWidget(fill_profile)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class FillProfile(QDialog):
    def __init__(self):
        super(FillProfile, self).__init__()
        loadUi("GUI/Authenticate_Screens/FillProfile.ui", self)
        self.save.clicked.connect(self.set_profile)

    def set_profile(self):
        first_name = self.firstname.text()
        last_name = self.lastname.text()
        phone_number = self.phonenumber.text()
        gender = self.gender.currentText()
        birth_date = self.birthdate.text()
        address = self.address.toPlainText()
        flag = auth.fill_profile(self, first_name, last_name, phone_number, address, birth_date, gender, auth.user_id)
        if flag:
            main_menu = MainMenu()
            widget.addWidget(main_menu)
            widget.setCurrentIndex(widget.currentIndex() + 1)


class MainMenu(QDialog):
    def __init__(self):
        super(MainMenu, self).__init__()
        loadUi("GUI/MainMenu_Screens/MainMenu.ui", self)
        self.bookroom.clicked.connect(self.go_to_book_room_screen)
        self.logout.clicked.connect(self.log_out)
        reserve.check_status()
        if reserve.status == 1:
            self.showrestaurants.clicked.connect(self.go_to_show_restaurants_screen)
            self.showallfood.clicked.connect(self.go_to_show_allfood_screen)
            self.cleaningservicebtn.clicked.connect(self.go_to_cleaning_service_screen)
            self.reservations.clicked.connect(self.go_reservations_screen)
            self.bill.clicked.connect(self.go_to_bill_screen)

        self.userid.setText(auth.national_id)

    def go_to_book_room_screen(self):
        globals()['reserve'] = Reserve.Reservation()
        book_room = BookRoom()
        widget.addWidget(book_room)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_show_restaurants_screen(self):
        show_restaurants = ShowRestaurants()
        widget.addWidget(show_restaurants)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_show_allfood_screen(self):
        all_food = AllFood()
        widget.addWidget(all_food)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_cleaning_service_screen(self):
        cleaning_service_request = CleaningServiceRequest()
        widget.addWidget(cleaning_service_request)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_reservations_screen(self):
        reservation_list = ReservationList()
        widget.addWidget(reservation_list)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_bill_screen(self):
        bill = Bill()
        widget.addWidget(bill)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def log_out(self):
        globals()['invoice'] = Invoice()
        globals()['reserve'] = Reservation()
        globals()['restaurants'] = Restaurants()
        globals()['auth'] = Authenticate()
        first_screen = WelcomeScreen()
        widget.addWidget(first_screen)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class BookRoom(QDialog):
    def __init__(self):
        super(BookRoom, self).__init__()
        loadUi("GUI/Reservation_Screens/BookRoom.ui", self)
        self.search.clicked.connect(self.show_rooms)
        self.reserve.clicked.connect(self.reserve_room)

    def show_rooms(self):
        from_date = self.fromdate.text()
        to_date = self.todate.text()
        room_type = self.roomtype.currentText()
        self.rooms.setColumnWidth(0, 100)
        self.rooms.setColumnWidth(1, 100)
        self.rooms.setColumnWidth(2, 100)
        self.rooms.setColumnWidth(3, 100)
        self.rooms.setColumnWidth(4, 100)
        self.rooms.setColumnWidth(5, 100)
        self.rooms.setHorizontalHeaderLabels([
            "ID", "Floor", "Capacity", "Price", "NO_Bed", "Room_Type"
        ])
        self.rooms.setRowCount(100)
        reserve.get_rooms(self, from_date, to_date, room_type)

    def reserve_room(self):
        room_id = self.roomid.text()
        from_date = self.fromdate.text()
        to_date = self.todate.text()
        no_night = int(self.nonight.text())
        if len(room_id) == 0:
            self.error.setText('Please Enter Room ID!')
        else:
            reserve.room_reservation(auth.user_id, room_id, from_date, to_date, no_night)
            reservation_details = ReservationDetails()
            widget.addWidget(reservation_details)
            widget.setCurrentIndex(widget.currentIndex() + 1)


class ReservationDetails(QDialog):
    def __init__(self):
        super(ReservationDetails, self).__init__()
        loadUi("GUI/Reservation_Screens/ReservationDetails.ui", self)
        self.confirm.clicked.connect(self.make_reservation_details)
        self.add.clicked.connect(self.add_people)
        self.back.clicked.connect(self.back_to_main_menu)
        self.reserveroom.clicked.connect(self.go_to_book_room_screen)

    def go_to_book_room_screen(self):
        book_room = BookRoom()
        widget.addWidget(book_room)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def back_to_main_menu(self):
        main_menu = MainMenu()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def make_reservation_details(self):
        extra_facilities = self.extrafacilities.toPlainText()
        reserve.create_reservation_details(extra_facilities)
        self.confirmmassage.setText("Reservation Confirmed")

    def add_people(self):
        first_name = self.firstname.text()
        last_name = self.lastname.text()
        national_id = self.nationalid.text()
        gender = self.gender.currentText()
        reserve.create_people(first_name, last_name, national_id, gender)
        self.addmassage.setText("Person Added")


class ShowRestaurants(QDialog):
    def __init__(self):
        super(ShowRestaurants, self).__init__()
        loadUi("GUI/FoodOrder_Screens/ShowRestaurants.ui", self)
        self.show_restaurants()
        self.select.clicked.connect(self.restaurants_select)

    def show_restaurants(self):
        self.restaurants.setColumnWidth(0, 100)
        self.restaurants.setColumnWidth(1, 215)
        self.restaurants.setColumnWidth(2, 215)
        self.restaurants.setHorizontalHeaderLabels([
            "ID", "Name", "Type"
        ])
        self.restaurants.setRowCount(100)
        restaurants.show_all_restaurants(self)

    def restaurants_select(self):
        res_id = self.restaurantid.text()
        restaurants.select_restaurants(self, res_id)
        self.go_to_food_menu()

    def go_to_food_menu(self):
        food_menu = FoodOrder()
        widget.addWidget(food_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class FoodOrder(QDialog):
    def __init__(self):
        super(FoodOrder, self).__init__()
        loadUi("GUI/FoodOrder_Screens/FoodOrder.ui", self)
        self.restaurant_foods()
        self.searchbtn.clicked.connect(self.search_food)
        self.select.clicked.connect(self.select_food)

    def restaurant_foods(self):
        self.foods.setColumnWidth(0, 100)
        self.foods.setColumnWidth(1, 100)
        self.foods.setColumnWidth(2, 100)
        self.foods.setColumnWidth(3, 200)
        self.foods.setColumnWidth(4, 100)
        self.foods.setHorizontalHeaderLabels([
            "ID", "Name", "Price", "Ingredients", "Type"
        ])
        self.foods.setRowCount(100)
        restaurants.restaurant_all_foods(self)

    def search_food(self):
        search = self.searchinput.text()
        if len(search) != 0:
            restaurants.search_food_with_name(self, search)
        else:
            restaurants.restaurant_all_foods(self)

    def select_food(self):
        foods = self.foodsid.text()
        foods_list = foods.split(',')
        for food in foods_list:
            food = food.replace(" ", "")
            food = int(food)
        restaurants.set_foods(foods_list)
        self.go_to_food_list_screen()

    def go_to_food_list_screen(self):
        food_list = FoodList()
        widget.addWidget(food_list)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class FoodList(QDialog):
    def __init__(self):
        super(FoodList, self).__init__()
        loadUi("GUI/FoodOrder_Screens/FoodList.ui", self)
        self.rooms_list()
        self.food_order()
        self.confirm.clicked.connect(self.confirm_order)
        self.mainmenu.clicked.connect(self.back_to_main_menu)
        self.foodmenu.clicked.connect(self.go_to_food_menu)

    def food_order(self):
        self.foods.setColumnWidth(0, 100)
        self.foods.setColumnWidth(1, 100)
        self.foods.setColumnWidth(2, 100)
        self.foods.setColumnWidth(3, 200)
        self.foods.setColumnWidth(4, 100)
        self.foods.setHorizontalHeaderLabels([
            "ID", "Name", "Price", "Ingredients", "Type"
        ])
        self.foods.setRowCount(100)
        restaurants.foods_list(self)

    def rooms_list(self):
        self.rooms.setColumnWidth(0, 100)
        self.rooms.setHorizontalHeaderLabels([
            "ID",
        ])
        self.rooms.setRowCount(100)
        restaurants.rooms_list(self, reserve.reservation_id)

    def confirm_order(self):
        serve_in = self.serveplace.currentText()
        room_id = self.roomid.text()
        restaurants.order_confirmed(self, reserve.reservation_id, room_id, serve_in)
        self.massage.setText("Order Confirmed")

    def back_to_main_menu(self):
        main_menu = MainMenu()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def go_to_food_menu(self):
        food_menu = FoodOrder()
        widget.addWidget(food_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class AllFood(QDialog):
    def __init__(self):
        super(AllFood, self).__init__()
        loadUi("GUI/FoodOrder_Screens/AllFood.ui", self)
        self.show_all_foods()
        self.mainmenu.clicked.connect(self.back_to_main_menu)

    def show_all_foods(self):
        self.foods.setColumnWidth(0, 100)
        self.foods.setColumnWidth(1, 100)
        self.foods.setColumnWidth(2, 100)
        self.foods.setColumnWidth(3, 200)
        self.foods.setColumnWidth(4, 100)
        self.foods.setHorizontalHeaderLabels([
            "ID", "Name", "Price", "Ingredients", "Type"
        ])
        self.foods.setRowCount(100)
        restaurants.get_all_foods(self, reserve.reservation_id)

    def back_to_main_menu(self):
        main_menu = MainMenu()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CleaningServiceRequest(QDialog):
    def __init__(self):
        super(CleaningServiceRequest, self).__init__()
        loadUi("GUI/CleaningOrder_Screens/CleaningServiceRequest.ui", self)
        self.rooms_list()
        self.confirm.clicked.connect(self.request_cleaning_service)
        self.mainmenu.clicked.connect(self.back_to_main_menu)

    def rooms_list(self):
        self.rooms.setColumnWidth(0, 100)
        self.rooms.setHorizontalHeaderLabels([
            "ID",
        ])
        self.rooms.setRowCount(100)
        restaurants.rooms_list(self, reserve.reservation_id)

    def request_cleaning_service(self):
        room_id = int(self.roomid.text())
        reservation_id = reserve.reservation_id
        temp = self.time.text().split(' ')
        cleaning_date = temp[0]
        cleaning_time = self.time.text()
        cleaning_description = self.description.toPlainText()
        cleaning_service = CleaningService(reservation_id, room_id, cleaning_time, cleaning_date, cleaning_description)
        cleaning_service.confirm_cleaning_service()
        self.massage.setText("Order Confirmed")

    def back_to_main_menu(self):
        main_menu = MainMenu()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ReservationList(QDialog):
    def __init__(self):
        super(ReservationList, self).__init__()
        loadUi("GUI/Reservation_Screens/ReservationList.ui", self)
        self.reservation_list()
        self.mainmenu.clicked.connect(self.back_to_main_menu)

    def reservation_list(self):
        self.reservation.setColumnWidth(0, 100)
        self.reservation.setColumnWidth(1, 100)
        self.reservation.setColumnWidth(2, 100)
        self.reservation.setColumnWidth(3, 100)
        self.reservation.setColumnWidth(4, 200)
        self.reservation.setHorizontalHeaderLabels([
            "ID", "Reserve Date", "Nights", "RoomId", "Extra Facilities"
        ])
        self.reservation.setRowCount(100)
        reserve.get_all_reservation(self, auth.user_id)

    def back_to_main_menu(self):
        main_menu = MainMenu()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Bill(QDialog):
    def __init__(self):
        super(Bill, self).__init__()
        loadUi("GUI/Invoice_Screen/Bill.ui", self)
        self.get_bill()
        self.mainmenu.clicked.connect(self.back_to_main_menu)

    def get_bill(self):
        self.foods.setColumnWidth(0, 100)
        self.foods.setColumnWidth(1, 100)
        self.foods.setColumnWidth(2, 100)
        self.foods.setHorizontalHeaderLabels([
            "ID", "Name", "Price"
        ])
        self.foods.setRowCount(100)

        self.rooms.setColumnWidth(0, 100)
        self.rooms.setColumnWidth(1, 100)
        self.rooms.setColumnWidth(2, 100)
        self.rooms.setHorizontalHeaderLabels([
            "Room ID", "Nights", "Price"
        ])
        self.rooms.setRowCount(100)

        self.services.setColumnWidth(0, 100)
        self.services.setColumnWidth(1, 100)
        self.services.setHorizontalHeaderLabels([
            "Room ID", "Price"
        ])
        self.services.setRowCount(100)

        invoice.get_all_foods(self, reserve.reservation_id)
        invoice.get_all_rooms(self, reserve.reservation_id)
        invoice.get_services(self, reserve.reservation_id)
        invoice.set_total()
        invoice.submit_bill(reserve.reservation_id)
        self.foodprice.setText(str(invoice.foods_price))
        self.serviceprice.setText(str(invoice.services_price))
        self.roomprice.setText(str(invoice.rooms_price))
        self.total.setText(str(invoice.total))

    def back_to_main_menu(self):
        main_menu = MainMenu()
        widget.addWidget(main_menu)
        widget.setCurrentIndex(widget.currentIndex() + 1)


invoice = Invoice()
reserve = Reservation()
restaurants = Restaurants()
auth = Authenticate()
app = QApplication(sys.argv)
welcome_screen = WelcomeScreen()
widget = QStackedWidget()
widget.addWidget(welcome_screen)
widget.setFixedHeight(640)
widget.setFixedWidth(820)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print('Exit')
