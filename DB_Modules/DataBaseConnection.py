import mysql.connector


def connect_to_database():
    conn = mysql.connector.connect(
        host="localhost", user="root", passwd="", database="db_project", port='3307'
    )
    cursor = conn.cursor()

    return conn, cursor


def fetchone(cursor):
    temp = None
    for i in cursor:
        temp = i[0]

    return temp


def fetchoneObject(cursor):
    temp = None
    for i in cursor:
        temp = i
    return temp
