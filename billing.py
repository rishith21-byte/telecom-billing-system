from db import conn, cursor
from datetime import date


def generate_bill_db(customer_id):

    # =========================================================
    # GET CUSTOMER AND PLAN INFORMATION
    # =========================================================

    sql = """
        SELECT
            c.customer_id,
            c.name,
            p.plan_id,
            p.plan_name,
            p.price
        FROM customer c
        JOIN plans p
            ON c.plan_id = p.plan_id
        WHERE c.customer_id = %s
    """

    cursor.execute(
        sql,
        (customer_id,)
    )

    result = cursor.fetchone()

    # Customer or plan not found
    if result is None:
        return None

    customer_id = result[0]
    customer_name = result[1]
    plan_id = result[2]
    plan_name = result[3]
    amount = float(result[4])

    # =========================================================
    # CALCULATE GST
    # =========================================================

    gst = amount * 0.18

    total = amount + gst

    # =========================================================
    # INSERT BILL
    # =========================================================

    insert_sql = """
        INSERT INTO bills
        (
            customer_id,
            plan_id,
            amount,
            gst,
            total_amount,
            bill_date,
            payment_status
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
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

    try:

        cursor.execute(
            insert_sql,
            values
        )

        conn.commit()

    except Exception:

        conn.rollback()

        raise

    # =========================================================
    # RETURN BILL DETAILS
    # =========================================================

    return {
        "customer_id": customer_id,
        "customer_name": customer_name,
        "plan_id": plan_id,
        "plan_name": plan_name,
        "amount": amount,
        "gst": gst,
        "total": total,
        "status": "Unpaid"
    }
