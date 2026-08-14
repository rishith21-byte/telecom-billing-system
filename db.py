import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Telecom@123!",
        database="telecom"
    )

    cursor = conn.cursor()

    print("Connected to MySQL successfully!")

except mysql.connector.Error as err:
    print("Error:", err)
