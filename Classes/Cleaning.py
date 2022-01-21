from DB_Modules.CleaningService_DB import add_cleaning_service_database
from DB_Modules.DataBaseConnection import connect_to_database
from DB_Modules.Reservation_DB import get_reservation_details_id


class CleaningService:
    reservation_id = 0
    room_id = 0
    cleaning_time = ''
    cleaning_date = ''
    cleaning_description = ''

    def __init__(self, reservation_id, room_id, cleaning_time, cleaning_date, cleaning_description):
        self.reservation_id = reservation_id
        self.room_id = room_id
        self.cleaning_time = cleaning_time
        self.cleaning_date = cleaning_date
        self.cleaning_description = cleaning_description

    def confirm_cleaning_service(self):
        conn, cursor = connect_to_database()
        reservation_details_id = get_reservation_details_id(cursor, self.room_id, self.reservation_id)
        add_cleaning_service_database(conn, cursor, reservation_details_id, self.cleaning_time, self.cleaning_date,
                                      self.cleaning_description)
