import pyodbc


def connect_to_database():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-K4D634H;'
                          'Database=DB_Project;'
                          'Trusted_Connection=yes;')
    cursor = conn.cursor()

    return conn, cursor
