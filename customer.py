from db import conn, cursor

def add_customer():
    name = input("Enter Customer Name: ")
    phone = input("Enter Phone Number: ")
    email = input("Enter Email: ")
    address = input("Enter Address: ")
    aadhaar = input("Enter Aadhaar Number: ")
    plan_id = int(input("Enter Plan ID: "))

    sql = """
    INSERT INTO customer
    (name, phone, email, address, aadhaar, plan_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        name,
        phone,
        email,
        address,
        aadhaar,
        plan_id
    )

    cursor.execute(sql, values)
    conn.commit()

    print("\nCustomer added successfully!")

def view_customers():
    cursor.execute("SELECT * FROM customer")
    customers = cursor.fetchall()

    if not customers:
        print("\nNo customers found.")
        return

    print("\n---------------- CUSTOMER LIST ----------------")
    print("{:<5} {:<20} {:<15} {:<25} {:<15}".format(
        "ID", "Name", "Phone", "Email", "Plan ID"))
    print("-" * 85)

    for customer in customers:
        print("{:<5} {:<20} {:<15} {:<25} {:<15}".format(
            customer[0],
            customer[1],
            customer[2],
            customer[3],
            customer[6]
        ))


def update_customer():
    customer_id = int(input("Enter Customer ID to update: "))

    cursor.execute(
        "SELECT * FROM customer WHERE customer_id=%s",
        (customer_id,)
    )
    customer = cursor.fetchone()

    if customer is None:
        print("Customer not found!")
        return

    print("\nEnter new details:")

    name = input("New Name: ")
    phone = input("New Phone: ")
    email = input("New Email: ")
    address = input("New Address: ")
    aadhaar = input("New Aadhaar: ")
    plan_id = int(input("New Plan ID: "))

    sql = """
    UPDATE customer
    SET name=%s,
        phone=%s,
        email=%s,
        address=%s,
        aadhaar=%s,
        plan_id=%s
    WHERE customer_id=%s
    """

    values = (
        name,
        phone,
        email,
        address,
        aadhaar,
        plan_id,
        customer_id
    )

    cursor.execute(sql, values)
    conn.commit()

    print("Customer updated successfully!")


def delete_customer():
    customer_id = int(input("Enter Customer ID to deactivate: "))

    cursor.execute(
        "SELECT customer_id, status FROM customer WHERE customer_id=%s",
        (customer_id,)
    )
    customer = cursor.fetchone()

    if customer is None:
        print("Customer not found!")
        return

    if customer[1] == "Inactive":
        print("Customer is already inactive!")
        return

    cursor.execute(
        """
        UPDATE customer
        SET status = 'Inactive'
        WHERE customer_id=%s
        """,
        (customer_id,)
    )

    conn.commit()

    print("Customer deactivated successfully!")
