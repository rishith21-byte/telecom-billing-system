import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Telecom@123!",
        database="telecom"
    )

    cursor = conn.cursor()

    cursor.execute("SHOW TABLES")

    print("Tables in telecom database:")

    for table in cursor:
        print(table[0])

except mysql.connector.Error as err:
    print(err)

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
