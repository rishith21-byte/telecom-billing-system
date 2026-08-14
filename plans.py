from db import conn, cursor


# =========================================================
# CONSOLE: ADD PLAN
# =========================================================

def add_plan():

    plan_name = input(
        "Enter Plan Name: "
    ).strip()

    try:
        price = float(
            input("Enter Plan Price: ")
        )

        validity = int(
            input("Enter Validity (days): ")
        )

    except ValueError:

        print(
            "Price must be a number and validity must be an integer."
        )

        return

    data_limit = input(
        "Enter Data Limit: "
    ).strip()

    call_limit = input(
        "Enter Call Limit: "
    ).strip()

    sms_limit = input(
        "Enter SMS Limit: "
    ).strip()

    if not plan_name:

        print(
            "Plan name cannot be empty."
        )

        return

    sql = """
        INSERT INTO plans
        (
            plan_name,
            price,
            validity,
            data_limit,
            call_limit,
            sms_limit
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        plan_name,
        price,
        validity,
        data_limit,
        call_limit,
        sms_limit
    )

    try:

        cursor.execute(
            sql,
            values
        )

        conn.commit()

        print(
            "Plan added successfully!"
        )

    except Exception as e:

        conn.rollback()

        print(
            "Error adding plan:",
            e
        )


# =========================================================
# CONSOLE: VIEW PLANS
# =========================================================

def view_plans():

    try:

        cursor.execute("""
            SELECT
                plan_id,
                plan_name,
                price,
                validity,
                data_limit,
                call_limit,
                sms_limit
            FROM plans
            ORDER BY plan_id
        """)

        plans = cursor.fetchall()

        if not plans:

            print(
                "No plans available."
            )

            return

        print(
            "\n---------------- PLANS ----------------"
        )

        print(
            "{:<5} {:<15} {:<10} {:<10}".format(
                "ID",
                "Plan",
                "Price",
                "Validity"
            )
        )

        print(
            "-" * 50
        )

        for plan in plans:

            print(
                "{:<5} {:<15} {:<10} {:<10}".format(
                    plan[0],
                    plan[1],
                    plan[2],
                    plan[3]
                )
            )

    except Exception as e:

        print(
            "Error viewing plans:",
            e
        )


# =========================================================
# DASHBOARD: GET ALL PLANS
# =========================================================

def get_all_plans():

    try:

        cursor.execute("""
            SELECT
                plan_id,
                plan_name,
                price,
                validity,
                data_limit,
                call_limit,
                sms_limit
            FROM plans
            ORDER BY plan_id
        """)

        return cursor.fetchall()

    except Exception:

        raise


# =========================================================
# DASHBOARD: ADD PLAN
# =========================================================

def add_plan_db(
    plan_name,
    price,
    validity,
    data_limit,
    call_limit,
    sms_limit
):

    sql = """
        INSERT INTO plans
        (
            plan_name,
            price,
            validity,
            data_limit,
            call_limit,
            sms_limit
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    values = (
        plan_name,
        price,
        validity,
        data_limit,
        call_limit,
        sms_limit
    )

    try:

        cursor.execute(
            sql,
            values
        )

        conn.commit()

        return True

    except Exception:

        conn.rollback()

        raise


# =========================================================
# DASHBOARD: UPDATE PLAN
# =========================================================

def update_plan_db(
    plan_id,
    plan_name,
    price,
    validity,
    data_limit,
    call_limit,
    sms_limit
):

    sql = """
        UPDATE plans
        SET
            plan_name = %s,
            price = %s,
            validity = %s,
            data_limit = %s,
            call_limit = %s,
            sms_limit = %s
        WHERE plan_id = %s
    """

    values = (
        plan_name,
        price,
        validity,
        data_limit,
        call_limit,
        sms_limit,
        plan_id
    )

    try:

        cursor.execute(
            sql,
            values
        )

        conn.commit()

        return True

    except Exception:

        conn.rollback()

        raise


# =========================================================
# DASHBOARD: DELETE PLAN
# =========================================================

def delete_plan_db(plan_id):

    # -----------------------------------------------------
    # Check whether customers are using this plan
    # -----------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM customer
        WHERE plan_id = %s
    """, (
        plan_id,
    ))

    customer_count = cursor.fetchone()[0]

    if customer_count > 0:

        raise Exception(
            f"Cannot delete this plan because "
            f"{customer_count} customer(s) are using it."
        )

    # -----------------------------------------------------
    # Check whether bills use this plan
    # -----------------------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM bills
        WHERE plan_id = %s
    """, (
        plan_id,
    ))

    bill_count = cursor.fetchone()[0]

    if bill_count > 0:

        raise Exception(
            f"Cannot delete this plan because "
            f"{bill_count} bill(s) are associated with it."
        )

    # -----------------------------------------------------
    # Delete plan
    # -----------------------------------------------------

    sql = """
        DELETE FROM plans
        WHERE plan_id = %s
    """

    try:

        cursor.execute(
            sql,
            (plan_id,)
        )

        conn.commit()

        return True

    except Exception:

        conn.rollback()

        raise


# =========================================================
# OPTIONAL: CONSOLE MENU
# =========================================================

def plan_menu():

    while True:

        print("\n========== PLAN MANAGEMENT ==========")

        print("1. Add Plan")
        print("2. View Plans")
        print("3. Exit")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            add_plan()

        elif choice == "2":

            view_plans()

        elif choice == "3":

            break

        else:

            print(
                "Invalid choice."
            )


# =========================================================
# RUN ONLY IF FILE IS EXECUTED DIRECTLY
# =========================================================

if __name__ == "__main__":

    plan_menu()
