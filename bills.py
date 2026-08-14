from db import conn, cursor
from datetime import date

def generate_bill():

    customer_id = int(input("Enter Customer ID: "))

    sql = """
    SELECT c.customer_id,
           c.name,
           p.plan_id,
           p.plan_name,
           p.price
    FROM customer c
    JOIN plans p
    ON c.plan_id = p.plan_id
    WHERE c.customer_id = %s
    """

    cursor.execute(sql, (customer_id,))
    result = cursor.fetchone()

    if result is None:
        print("Customer not found!")
        return

    customer_id = result[0]
    customer_name = result[1]
    plan_id = result[2]
    plan_name = result[3]
    amount = float(result[4])

    gst = amount * 0.18
    total = amount + gst

    insert_sql = """
    INSERT INTO bills
    (customer_id, plan_id, amount, gst, total_amount, bill_date, payment_status)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        customer_id,
        plan_id,
        amount,
        gst,
        total,
        date.today(),
        "Unpaid"
    )

    cursor.execute(insert_sql, values)
    conn.commit()

    print("\n========== TELECOM BILL ==========")
    print("Customer :", customer_name)
    print("Plan     :", plan_name)
    print("Amount   : ₹", amount)
    print("GST(18%) : ₹", round(gst,2))
    print("------------------------------")
    print("Total    : ₹", round(total,2))
    print("Status   : Unpaid")
    print("==================================")
