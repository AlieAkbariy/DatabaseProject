from DB_Modules.Authenticate_DB import create_user, get_user_password, complete_user_information, \
    get_user_id
from DB_Modules.DataBaseConnection import connect_to_database


class Authenticate:
    user_id = 0
    national_id = ""

    def login(self, parent_class, user_name, password):
        conn, cursor = connect_to_database()  # Set up database connection

        if len(user_name) == 0 or len(password) == 0:
            parent_class.error.setText('Please input all fields')
            return False
        else:
            sql_pass = get_user_password(cursor, user_name)
            if sql_pass is not None:
                if password == sql_pass[0]:
                    self.user_id = get_user_id(cursor, user_name, password)
                    self.national_id = user_name
                    return True
                else:
                    parent_class.error.setText('Invalid username or password')
            else:
                parent_class.error.setText('Invalid username or password')
        return False

    def signup(self, parent_class, user_name, password, confirm_password):
        conn, cursor = connect_to_database()  # Set up database connection
        temp = get_user_password(cursor, user_name)
        if len(user_name) == 0 or len(password) == 0 or len(confirm_password) == 0:
            parent_class.error.setText('Please input all fields')
        elif temp is not None:
            parent_class.error.setText('This user exists!')

        else:
            if password == confirm_password:
                create_user(conn, cursor, user_name, password)
                self.user_id = get_user_id(cursor, user_name, password)
                self.national_id = user_name
                return True
            else:
                parent_class.error.setText('Password and confirm password does not match!')

        conn.close()
        return False

    def fill_profile(self, parent_class, first_name, last_name, phone_number, address, birth_date, gender, user_name):
        conn, cursor = connect_to_database()  # Set up database connection
        if len(first_name) == 0 or len(last_name) == 0 or len(phone_number) == 0 or \
                len(address) == 0 or len(birth_date) == 0 or len(gender) == 0:
            parent_class.message.setText('Please input all fields')
        else:
            complete_user_information(conn, cursor, user_name, first_name, last_name, phone_number, address,
                                      birth_date, gender)
            conn.close()
            return True
        return False
