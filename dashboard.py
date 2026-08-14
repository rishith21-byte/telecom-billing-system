import sys

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QLineEdit,
    QFormLayout,
    QDialog,
    QDialogButtonBox,
    QComboBox,
    QDoubleSpinBox,
    QSpinBox,
)

from PySide6.QtCore import Qt

from db import conn, cursor

from plans import (
    get_all_plans,
    add_plan_db,
    update_plan_db,
    delete_plan_db,
)

from billing import generate_bill_db

from theme import apply_theme, toggle_theme

from reports import ReportsPage


class DashboardWindow(QMainWindow):

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(self):
        super().__init__()

        self.current_theme = "dark"

        self.setWindowTitle(
            "Telecom Billing Management System"
        )

        self.resize(1200, 700)

        self.setup_ui()

        self.load_dashboard_data()

    # =====================================================
    # SETUP UI
    # =====================================================

    def setup_ui(self):

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QHBoxLayout(
            central_widget
        )

        main_layout.setContentsMargins(
            0, 0, 0, 0
        )

        main_layout.setSpacing(0)

        # =================================================
        # SIDEBAR
        # =================================================

        sidebar = QFrame()

        sidebar.setFixedWidth(
            220
        )

        sidebar_layout = QVBoxLayout(
            sidebar
        )

        sidebar_layout.setContentsMargins(
            15, 20, 15, 20
        )

        title = QLabel(
            "TELECOM\nSYSTEM"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            padding: 15px;
        """)

        sidebar_layout.addWidget(
            title
        )

        self.dashboard_btn = QPushButton(
            "Dashboard"
        )

        self.customer_btn = QPushButton(
            "Customers"
        )

        self.plan_btn = QPushButton(
            "Plans"
        )

        self.billing_btn = QPushButton(
            "Generate Bill"
        )

        self.bills_btn = QPushButton(
            "Bills & Payments"
        )

        self.report_btn = QPushButton(
            "Reports"
        )

        buttons = [
            self.dashboard_btn,
            self.customer_btn,
            self.plan_btn,
            self.billing_btn,
            self.bills_btn,
            self.report_btn,
        ]

        for button in buttons:

            button.setMinimumHeight(
                45
            )

            sidebar_layout.addWidget(
                button
            )

        sidebar_layout.addStretch()

        # =================================================
        # THEME BUTTON
        # =================================================

        self.theme_button = QPushButton(
            "☀ Light Mode"
        )

        self.theme_button.setMinimumHeight(
            45
        )

        self.theme_button.clicked.connect(
            self.toggle_application_theme
        )

        sidebar_layout.addWidget(
            self.theme_button
        )

        # =================================================
        # EXIT BUTTON
        # =================================================

        exit_button = QPushButton(
            "Exit"
        )

        exit_button.setMinimumHeight(
            45
        )

        sidebar_layout.addWidget(
            exit_button
        )

        exit_button.clicked.connect(
            self.close
        )

        # =================================================
        # STACKED PAGES
        # =================================================

        self.pages = QStackedWidget()

        self.dashboard_page = (
            self.create_dashboard_page()
        )

        self.customer_page = (
            self.create_customer_page()
        )

        self.plan_page = (
            self.create_plan_page()
        )

        self.billing_page = (
            self.create_billing_page()
        )

        self.bills_page = (
            self.create_bills_page()
        )

        self.report_page = ReportsPage()

        self.pages.addWidget(
            self.dashboard_page
        )

        self.pages.addWidget(
            self.customer_page
        )

        self.pages.addWidget(
            self.plan_page
        )

        self.pages.addWidget(
            self.billing_page
        )

        self.pages.addWidget(
            self.bills_page
        )

        self.pages.addWidget(
            self.report_page
        )

        # =================================================
        # BUTTON CONNECTIONS
        # =================================================

        self.dashboard_btn.clicked.connect(
            self.show_dashboard
        )

        self.customer_btn.clicked.connect(
            self.show_customers
        )

        self.plan_btn.clicked.connect(
            self.show_plans
        )

        self.billing_btn.clicked.connect(
            self.show_billing
        )

        self.bills_btn.clicked.connect(
            self.show_bills
        )

        self.report_btn.clicked.connect(
            self.show_reports
        )

        main_layout.addWidget(
            sidebar
        )

        main_layout.addWidget(
            self.pages
        )

    # =====================================================
    # THEME SWITCH
    # =====================================================

    def toggle_application_theme(self):

        app = QApplication.instance()

        self.current_theme = toggle_theme(
            app,
            self.current_theme
        )

        if self.current_theme == "dark":

            self.theme_button.setText(
                "☀ Light Mode"
            )

        else:

            self.theme_button.setText(
                "🌙 Dark Mode"
            )

    # =====================================================
    # NAVIGATION
    # =====================================================

    def show_dashboard(self):

        self.load_dashboard_data()

        self.pages.setCurrentIndex(
            0
        )

    def show_customers(self):

        self.load_customers()

        self.pages.setCurrentIndex(
            1
        )

    def show_plans(self):

        self.load_plans()

        self.pages.setCurrentIndex(
            2
        )

    def show_billing(self):

        self.load_billing_customers()

        self.pages.setCurrentIndex(
            3
        )

    def show_bills(self):

        self.load_bills()

        self.pages.setCurrentIndex(
            4
        )

    def show_reports(self):

        self.pages.setCurrentIndex(
            5
        )

    # =====================================================
    # DASHBOARD PAGE
    # =====================================================

    def create_dashboard_page(self):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        layout.setContentsMargins(
            30, 30, 30, 30
        )

        heading = QLabel(
            "Dashboard"
        )

        heading.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)

        layout.addWidget(
            heading
        )

        subtitle = QLabel(
            "Telecom Billing Management Overview"
        )

        subtitle.setStyleSheet("""
            font-size: 16px;
        """)

        layout.addWidget(
            subtitle
        )

        # =================================================
        # STATISTICS
        # =================================================

        stats_layout = QHBoxLayout()

        # -------------------------------------------------
        # CUSTOMER CARD
        # -------------------------------------------------

        customer_card = QFrame()

        customer_card.setFrameShape(
            QFrame.StyledPanel
        )

        customer_layout = QVBoxLayout(
            customer_card
        )

        customer_title = QLabel(
            "Total Customers"
        )

        customer_title.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
        """)

        self.customer_count_label = QLabel(
            "0"
        )

        self.customer_count_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        customer_layout.addWidget(
            customer_title
        )

        customer_layout.addWidget(
            self.customer_count_label
        )

        stats_layout.addWidget(
            customer_card
        )

        # -------------------------------------------------
        # BILLS CARD
        # -------------------------------------------------

        bills_card = QFrame()

        bills_card.setFrameShape(
            QFrame.StyledPanel
        )

        bills_layout = QVBoxLayout(
            bills_card
        )

        bills_title = QLabel(
            "Total Bills"
        )

        bills_title.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
        """)

        self.bills_count_label = QLabel(
            "0"
        )

        self.bills_count_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        bills_layout.addWidget(
            bills_title
        )

        bills_layout.addWidget(
            self.bills_count_label
        )

        stats_layout.addWidget(
            bills_card
        )

        # -------------------------------------------------
        # PAID CARD
        # -------------------------------------------------

        paid_card = QFrame()

        paid_card.setFrameShape(
            QFrame.StyledPanel
        )

        paid_layout = QVBoxLayout(
            paid_card
        )

        paid_title = QLabel(
            "Paid Bills"
        )

        paid_title.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
        """)

        self.paid_count_label = QLabel(
            "0"
        )

        self.paid_count_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        paid_layout.addWidget(
            paid_title
        )

        paid_layout.addWidget(
            self.paid_count_label
        )

        stats_layout.addWidget(
            paid_card
        )

        # -------------------------------------------------
        # UNPAID CARD
        # -------------------------------------------------

        unpaid_card = QFrame()

        unpaid_card.setFrameShape(
            QFrame.StyledPanel
        )

        unpaid_layout = QVBoxLayout(
            unpaid_card
        )

        unpaid_title = QLabel(
            "Unpaid Bills"
        )

        unpaid_title.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
        """)

        self.unpaid_count_label = QLabel(
            "0"
        )

        self.unpaid_count_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        unpaid_layout.addWidget(
            unpaid_title
        )

        unpaid_layout.addWidget(
            self.unpaid_count_label
        )

        stats_layout.addWidget(
            unpaid_card
        )

        layout.addLayout(
            stats_layout
        )

        # =================================================
        # REVENUE
        # =================================================

        revenue_frame = QFrame()

        revenue_frame.setFrameShape(
            QFrame.StyledPanel
        )

        revenue_layout = QVBoxLayout(
            revenue_frame
        )

        revenue_title = QLabel(
            "Total Revenue"
        )

        revenue_title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)

        self.revenue_value = QLabel(
            "₹ 0.00"
        )

        self.revenue_value.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
        """)

        revenue_layout.addWidget(
            revenue_title
        )

        revenue_layout.addWidget(
            self.revenue_value
        )

        layout.addWidget(
            revenue_frame
        )

        layout.addStretch()

        return page

    # =====================================================
    # LOAD DASHBOARD DATA
    # =====================================================

    def load_dashboard_data(self):

        try:

            cursor.execute("""
                SELECT COUNT(*)
                FROM customer
                WHERE status = 'Active'
            """)

            total_customers = (
                cursor.fetchone()[0]
            )

            self.customer_count_label.setText(
                str(total_customers)
            )

            cursor.execute(
                "SELECT COUNT(*) FROM bills"
            )

            total_bills = (
                cursor.fetchone()[0]
            )

            self.bills_count_label.setText(
                str(total_bills)
            )

            cursor.execute("""
                SELECT COUNT(*)
                FROM bills
                WHERE payment_status = 'Paid'
            """)

            paid_bills = (
                cursor.fetchone()[0]
            )

            self.paid_count_label.setText(
                str(paid_bills)
            )

            cursor.execute("""
                SELECT COUNT(*)
                FROM bills
                WHERE payment_status = 'Unpaid'
            """)

            unpaid_bills = (
                cursor.fetchone()[0]
            )

            self.unpaid_count_label.setText(
                str(unpaid_bills)
            )

            cursor.execute("""
                SELECT COALESCE(
                    SUM(total_amount),
                    0
                )
                FROM bills
                WHERE payment_status = 'Paid'
            """)

            revenue = cursor.fetchone()[0]

            self.revenue_value.setText(
                f"₹ {float(revenue):,.2f}"
            )

        except Exception as e:

            print(
                "Dashboard error:",
                e
            )

    # =====================================================
    # CUSTOMER PAGE
    # =====================================================

    def create_customer_page(self):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        layout.setContentsMargins(
            30, 30, 30, 30
        )

        heading = QLabel(
            "Customer Management"
        )

        heading.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)

        layout.addWidget(
            heading
        )

        button_layout = QHBoxLayout()

        add_button = QPushButton(
            "Add Customer"
        )

        update_button = QPushButton(
            "Update Customer"
        )

        delete_button = QPushButton(
            "Delete Customer"
        )

        refresh_button = QPushButton(
            "Refresh"
        )

        for button in [
            add_button,
            update_button,
            delete_button,
            refresh_button
        ]:

            button.setMinimumHeight(
                40
            )

            button_layout.addWidget(
                button
            )

        button_layout.addStretch()

        layout.addLayout(
            button_layout
        )

        add_button.clicked.connect(
            self.show_add_customer_form
        )

        update_button.clicked.connect(
            self.show_update_customer_form
        )

        delete_button.clicked.connect(
            self.delete_customer
        )

        refresh_button.clicked.connect(
            self.load_customers
        )

        self.customer_table = QTableWidget()

        self.customer_table.setColumnCount(
            5
        )

        self.customer_table.setHorizontalHeaderLabels([
            "Customer ID",
            "Name",
            "Phone",
            "Email",
            "Plan ID"
        ])

        self.customer_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.customer_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.customer_table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        layout.addWidget(
            self.customer_table
        )

        self.load_customers()

        return page

    # =====================================================
    # LOAD CUSTOMERS
    # =====================================================

    def load_customers(self):

        try:

            cursor.execute("""
                SELECT
                    customer_id,
                    name,
                    phone,
                    email,
                    plan_id
                FROM customer
                WHERE status = 'Active'
                ORDER BY customer_id
            """)

            customers = cursor.fetchall()

            self.customer_table.setRowCount(
                len(customers)
            )

            for row, customer in enumerate(
                customers
            ):

                for column, value in enumerate(
                    customer
                ):

                    self.customer_table.setItem(
                        row,
                        column,
                        QTableWidgetItem(
                            str(value)
                        )
                    )

            self.customer_table.resizeColumnsToContents()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not load customers:\n{e}"
            )

    # =====================================================
    # GET PLANS
    # =====================================================

    def get_plans_for_customer(self):

        try:

            return get_all_plans()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not load plans:\n{e}"
            )

            return []

    # =====================================================
    # ADD CUSTOMER
    # =====================================================

    def show_add_customer_form(self):

        plans = self.get_plans_for_customer()

        if not plans:

            QMessageBox.warning(
                self,
                "No Plans",
                "Add a plan before adding a customer."
            )

            return

        dialog = QDialog(
            self
        )

        dialog.setWindowTitle(
            "Add Customer"
        )

        dialog.setMinimumWidth(
            450
        )

        layout = QVBoxLayout(
            dialog
        )

        form = QFormLayout()

        name_input = QLineEdit()

        phone_input = QLineEdit()

        email_input = QLineEdit()

        plan_combo = QComboBox()

        for plan in plans:

            plan_combo.addItem(
                f"{plan[1]} - ₹{plan[2]}",
                plan[0]
            )

        form.addRow(
            "Name:",
            name_input
        )

        form.addRow(
            "Phone:",
            phone_input
        )

        form.addRow(
            "Email:",
            email_input
        )

        form.addRow(
            "Plan:",
            plan_combo
        )

        layout.addLayout(
            form
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(
            dialog.accept
        )

        buttons.rejected.connect(
            dialog.reject
        )

        layout.addWidget(
            buttons
        )

        if dialog.exec() != QDialog.Accepted:

            return

        name = name_input.text().strip()

        phone = phone_input.text().strip()

        email = email_input.text().strip()

        plan_id = plan_combo.currentData()

        if not name or not phone or not email:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please fill in all fields."
            )

            return

        try:

            cursor.execute("""
                INSERT INTO customer
                (
                    name,
                    phone,
                    email,
                    plan_id
                )
                VALUES (%s, %s, %s, %s)
            """, (
                name,
                phone,
                email,
                plan_id
            ))

            conn.commit()

            QMessageBox.information(
                self,
                "Success",
                "Customer added successfully."
            )

            self.load_customers()

            self.load_billing_customers()

            self.load_dashboard_data()

        except Exception as e:

            conn.rollback()

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not add customer:\n{e}"
            )

    # =====================================================
    # UPDATE CUSTOMER
    # =====================================================

    def show_update_customer_form(self):

        row = (
            self.customer_table.currentRow()
        )

        if row < 0:

            QMessageBox.warning(
                self,
                "Select Customer",
                "Select a customer first."
            )

            return

        customer_id = (
            self.customer_table.item(
                row,
                0
            ).text()
        )

        current_name = (
            self.customer_table.item(
                row,
                1
            ).text()
        )

        current_phone = (
            self.customer_table.item(
                row,
                2
            ).text()
        )

        current_email = (
            self.customer_table.item(
                row,
                3
            ).text()
        )

        current_plan = (
            self.customer_table.item(
                row,
                4
            ).text()
        )

        plans = self.get_plans_for_customer()

        dialog = QDialog(
            self
        )

        dialog.setWindowTitle(
            "Update Customer"
        )

        dialog.setMinimumWidth(
            450
        )

        layout = QVBoxLayout(
            dialog
        )

        form = QFormLayout()

        name_input = QLineEdit(
            current_name
        )

        phone_input = QLineEdit(
            current_phone
        )

        email_input = QLineEdit(
            current_email
        )

        plan_combo = QComboBox()

        selected_index = 0

        for index, plan in enumerate(
            plans
        ):

            plan_combo.addItem(
                f"{plan[1]} - ₹{plan[2]}",
                plan[0]
            )

            if str(plan[0]) == current_plan:

                selected_index = index

        plan_combo.setCurrentIndex(
            selected_index
        )

        form.addRow(
            "Name:",
            name_input
        )

        form.addRow(
            "Phone:",
            phone_input
        )

        form.addRow(
            "Email:",
            email_input
        )

        form.addRow(
            "Plan:",
            plan_combo
        )

        layout.addLayout(
            form
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(
            dialog.accept
        )

        buttons.rejected.connect(
            dialog.reject
        )

        layout.addWidget(
            buttons
        )

        if dialog.exec() != QDialog.Accepted:

            return

        name = name_input.text().strip()

        phone = phone_input.text().strip()

        email = email_input.text().strip()

        plan_id = plan_combo.currentData()

        if not name or not phone or not email:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please fill in all fields."
            )

            return

        try:

            cursor.execute("""
                UPDATE customer
                SET
                    name = %s,
                    phone = %s,
                    email = %s,
                    plan_id = %s
                WHERE customer_id = %s
            """, (
                name,
                phone,
                email,
                plan_id,
                customer_id
            ))

            conn.commit()

            QMessageBox.information(
                self,
                "Success",
                "Customer updated successfully."
            )

            self.load_customers()

            self.load_billing_customers()

        except Exception as e:

            conn.rollback()

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not update customer:\n{e}"
            )

    # =====================================================
    # DELETE / DEACTIVATE CUSTOMER
    # =====================================================

    def delete_customer(self):

        row = (
            self.customer_table.currentRow()
        )

        if row < 0:

            QMessageBox.warning(
                self,
                "Select Customer",
                "Select a customer first."
            )

            return

        customer_id = (
            self.customer_table.item(
                row,
                0
            ).text()
        )

        customer_name = (
            self.customer_table.item(
                row,
                1
            ).text()
        )

        answer = QMessageBox.question(
            self,
            "Confirm Deactivation",
            f"Deactivate customer '{customer_name}'?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:

            return

        try:

            cursor.execute("""
                UPDATE customer
                SET status = 'Inactive'
                WHERE customer_id = %s
            """, (
                customer_id,
            ))

            conn.commit()

            QMessageBox.information(
                self,
                "Success",
                "Customer deactivated successfully."
            )

            self.load_customers()

            self.load_billing_customers()

            self.load_dashboard_data()

        except Exception as e:

            conn.rollback()

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not deactivate customer:\n{e}"
            )

    # =====================================================
    # PLAN PAGE
    # =====================================================

    def create_plan_page(self):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        layout.setContentsMargins(
            30, 30, 30, 30
        )

        heading = QLabel(
            "Plan Management"
        )

        heading.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)

        layout.addWidget(
            heading
        )

        button_layout = QHBoxLayout()

        add_button = QPushButton(
            "Add Plan"
        )

        update_button = QPushButton(
            "Update Plan"
        )

        delete_button = QPushButton(
            "Delete Plan"
        )

        refresh_button = QPushButton(
            "Refresh"
        )

        for button in [
            add_button,
            update_button,
            delete_button,
            refresh_button
        ]:

            button.setMinimumHeight(
                40
            )

            button_layout.addWidget(
                button
            )

        button_layout.addStretch()

        layout.addLayout(
            button_layout
        )

        add_button.clicked.connect(
            self.show_add_plan_form
        )

        update_button.clicked.connect(
            self.show_update_plan_form
        )

        delete_button.clicked.connect(
            self.delete_plan
        )

        refresh_button.clicked.connect(
            self.load_plans
        )

        self.plan_table = QTableWidget()

        self.plan_table.setColumnCount(
            7
        )

        self.plan_table.setHorizontalHeaderLabels([
            "Plan ID",
            "Plan Name",
            "Price",
            "Validity",
            "Data Limit",
            "Call Limit",
            "SMS Limit"
        ])

        self.plan_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.plan_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.plan_table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        layout.addWidget(
            self.plan_table
        )

        self.load_plans()

        return page

    # =====================================================
    # LOAD PLANS
    # =====================================================

    def load_plans(self):

        try:

            plans = get_all_plans()

            self.plan_table.setRowCount(
                len(plans)
            )

            for row, plan in enumerate(
                plans
            ):

                for column, value in enumerate(
                    plan
                ):

                    self.plan_table.setItem(
                        row,
                        column,
                        QTableWidgetItem(
                            str(value)
                        )
                    )

            self.plan_table.resizeColumnsToContents()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not load plans:\n{e}"
            )

    # =====================================================
    # ADD PLAN
    # =====================================================

    def show_add_plan_form(self):

        dialog = QDialog(
            self
        )

        dialog.setWindowTitle(
            "Add Plan"
        )

        dialog.setMinimumWidth(
            450
        )

        layout = QVBoxLayout(
            dialog
        )

        form = QFormLayout()

        plan_name = QLineEdit()

        price = QDoubleSpinBox()

        price.setMaximum(
            1000000
        )

        price.setDecimals(
            2
        )

        validity = QSpinBox()

        validity.setMinimum(
            1
        )

        validity.setMaximum(
            3650
        )

        data_limit = QLineEdit()

        call_limit = QLineEdit()

        sms_limit = QLineEdit()

        form.addRow(
            "Plan Name:",
            plan_name
        )

        form.addRow(
            "Price:",
            price
        )

        form.addRow(
            "Validity:",
            validity
        )

        form.addRow(
            "Data Limit:",
            data_limit
        )

        form.addRow(
            "Call Limit:",
            call_limit
        )

        form.addRow(
            "SMS Limit:",
            sms_limit
        )

        layout.addLayout(
            form
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(
            dialog.accept
        )

        buttons.rejected.connect(
            dialog.reject
        )

        layout.addWidget(
            buttons
        )

        if dialog.exec() != QDialog.Accepted:

            return

        if not plan_name.text().strip():

            QMessageBox.warning(
                self,
                "Missing Information",
                "Enter a plan name."
            )

            return

        try:

            add_plan_db(
                plan_name.text().strip(),
                price.value(),
                validity.value(),
                data_limit.text().strip(),
                call_limit.text().strip(),
                sms_limit.text().strip()
            )

            QMessageBox.information(
                self,
                "Success",
                "Plan added successfully."
            )

            self.load_plans()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not add plan:\n{e}"
            )

    # =====================================================
    # UPDATE PLAN
    # =====================================================

    def show_update_plan_form(self):

        row = (
            self.plan_table.currentRow()
        )

        if row < 0:

            QMessageBox.warning(
                self,
                "Select Plan",
                "Select a plan first."
            )

            return

        plan_id = (
            self.plan_table.item(
                row,
                0
            ).text()
        )

        current_name = (
            self.plan_table.item(
                row,
                1
            ).text()
        )

        current_price = (
            self.plan_table.item(
                row,
                2
            ).text()
        )

        current_validity = (
            self.plan_table.item(
                row,
                3
            ).text()
        )

        current_data = (
            self.plan_table.item(
                row,
                4
            ).text()
        )

        current_calls = (
            self.plan_table.item(
                row,
                5
            ).text()
        )

        current_sms = (
            self.plan_table.item(
                row,
                6
            ).text()
        )

        dialog = QDialog(
            self
        )

        dialog.setWindowTitle(
            "Update Plan"
        )

        dialog.setMinimumWidth(
            450
        )

        layout = QVBoxLayout(
            dialog
        )

        form = QFormLayout()

        plan_name = QLineEdit(
            current_name
        )

        price = QDoubleSpinBox()

        price.setMaximum(
            1000000
        )

        price.setDecimals(
            2
        )

        price.setValue(
            float(current_price)
        )

        validity = QSpinBox()

        validity.setMinimum(
            1
        )

        validity.setMaximum(
            3650
        )

        validity.setValue(
            int(current_validity)
        )

        data_limit = QLineEdit(
            current_data
        )

        call_limit = QLineEdit(
            current_calls
        )

        sms_limit = QLineEdit(
            current_sms
        )

        form.addRow(
            "Plan Name:",
            plan_name
        )

        form.addRow(
            "Price:",
            price
        )

        form.addRow(
            "Validity:",
            validity
        )

        form.addRow(
            "Data Limit:",
            data_limit
        )

        form.addRow(
            "Call Limit:",
            call_limit
        )

        form.addRow(
            "SMS Limit:",
            sms_limit
        )

        layout.addLayout(
            form
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(
            dialog.accept
        )

        buttons.rejected.connect(
            dialog.reject
        )

        layout.addWidget(
            buttons
        )

        if dialog.exec() != QDialog.Accepted:

            return

        try:

            update_plan_db(
                int(plan_id),
                plan_name.text().strip(),
                price.value(),
                validity.value(),
                data_limit.text().strip(),
                call_limit.text().strip(),
                sms_limit.text().strip()
            )

            QMessageBox.information(
                self,
                "Success",
                "Plan updated successfully."
            )

            self.load_plans()

            self.load_billing_customers()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not update plan:\n{e}"
            )

    # =====================================================
    # DELETE PLAN
    # =====================================================

    def delete_plan(self):

        row = (
            self.plan_table.currentRow()
        )

        if row < 0:

            QMessageBox.warning(
                self,
                "Select Plan",
                "Select a plan first."
            )

            return

        plan_id = (
            self.plan_table.item(
                row,
                0
            ).text()
        )

        plan_name = (
            self.plan_table.item(
                row,
                1
            ).text()
        )

        answer = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Delete plan '{plan_name}'?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:

            return

        try:

            delete_plan_db(
                int(plan_id)
            )

            QMessageBox.information(
                self,
                "Success",
                "Plan deleted successfully."
            )

            self.load_plans()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not delete plan:\n{e}"
            )

    # =====================================================
    # GENERATE BILL PAGE
    # =====================================================

    def create_billing_page(self):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        layout.setContentsMargins(
            30, 30, 30, 30
        )

        heading = QLabel(
            "Generate Bill"
        )

        heading.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)

        layout.addWidget(
            heading
        )

        subtitle = QLabel(
            "Generate a new telecom bill for a customer"
        )

        subtitle.setStyleSheet("""
            font-size: 16px;
        """)

        layout.addWidget(
            subtitle
        )

        # =================================================
        # CUSTOMER SELECTION
        # =================================================

        form_frame = QFrame()

        form_frame.setFrameShape(
            QFrame.StyledPanel
        )

        form_layout = QFormLayout(
            form_frame
        )

        self.billing_customer_combo = QComboBox()

        self.billing_customer_combo.setMinimumHeight(
            35
        )

        form_layout.addRow(
            "Customer:",
            self.billing_customer_combo
        )

        layout.addWidget(
            form_frame
        )

        # =================================================
        # GENERATE BUTTON
        # =================================================

        generate_button = QPushButton(
            "Generate Bill"
        )

        generate_button.setMinimumHeight(
            45
        )

        generate_button.clicked.connect(
            self.generate_bill_from_dashboard
        )

        layout.addWidget(
            generate_button
        )

        # =================================================
        # BILL RESULT
        # =================================================

        self.bill_result_frame = QFrame()

        self.bill_result_frame.setFrameShape(
            QFrame.StyledPanel
        )

        result_layout = QVBoxLayout(
            self.bill_result_frame
        )

        self.bill_result_label = QLabel(
            "Bill details will appear here."
        )

        self.bill_result_label.setStyleSheet("""
            font-size: 17px;
            padding: 15px;
        """)

        self.bill_result_label.setAlignment(
            Qt.AlignTop
        )

        result_layout.addWidget(
            self.bill_result_label
        )

        layout.addWidget(
            self.bill_result_frame
        )

        layout.addStretch()

        self.load_billing_customers()

        return page

    # =====================================================
    # LOAD BILLING CUSTOMERS
    # =====================================================

    def load_billing_customers(self):

        try:

            cursor.execute("""
                SELECT
                    customer_id,
                    name,
                    phone
                FROM customer
                WHERE status = 'Active'
                ORDER BY customer_id
            """)

            customers = cursor.fetchall()

            self.billing_customer_combo.clear()

            for customer in customers:

                customer_id = customer[0]

                name = customer[1]

                phone = customer[2]

                self.billing_customer_combo.addItem(
                    f"{customer_id} - {name} - {phone}",
                    customer_id
                )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not load billing customers:\n{e}"
            )

    # =====================================================
    # GENERATE BILL
    # =====================================================

    def generate_bill_from_dashboard(self):

        customer_id = (
            self.billing_customer_combo.currentData()
        )

        if customer_id is None:

            QMessageBox.warning(
                self,
                "No Customer",
                "Please select a customer."
            )

            return

        try:

            bill = generate_bill_db(
                int(customer_id)
            )

            if bill is None:

                QMessageBox.warning(
                    self,
                    "Customer Not Found",
                    "Customer not found or has no valid plan."
                )

                return

            bill_text = f"""
            <h2>TELECOM BILL</h2>

            <b>Customer ID:</b>
            {bill["customer_id"]}<br>

            <b>Customer Name:</b>
            {bill["customer_name"]}<br><br>

            <b>Plan:</b>
            {bill["plan_name"]}<br>

            <b>Plan Price:</b>
            ₹ {bill["amount"]:.2f}<br>

            <b>GST (18%):</b>
            ₹ {bill["gst"]:.2f}<br>

            <hr>

            <h2>
            Total:
            ₹ {bill["total"]:.2f}
            </h2>

            <b>Payment Status:</b>
            {bill["status"]}
            """

            self.bill_result_label.setText(
                bill_text
            )

            QMessageBox.information(
                self,
                "Bill Generated",
                "Bill generated successfully."
            )

            self.load_bills()

            self.load_dashboard_data()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Billing Error",
                f"Could not generate bill:\n{e}"
            )

    # =====================================================
    # BILLS & PAYMENTS PAGE
    # =====================================================

    def create_bills_page(self):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        layout.setContentsMargins(
            30, 30, 30, 30
        )

        # =================================================
        # HEADING
        # =================================================

        heading = QLabel(
            "Bills & Payments"
        )

        heading.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)

        layout.addWidget(
            heading
        )

        subtitle = QLabel(
            "View generated bills and manage payment status"
        )

        subtitle.setStyleSheet("""
            font-size: 16px;
        """)

        layout.addWidget(
            subtitle
        )

        # =================================================
        # BUTTONS
        # =================================================

        button_layout = QHBoxLayout()

        refresh_button = QPushButton(
            "Refresh"
        )

        refresh_button.setMinimumHeight(
            40
        )

        paid_button = QPushButton(
            "Mark as Paid"
        )

        paid_button.setMinimumHeight(
            40
        )

        button_layout.addWidget(
            refresh_button
        )

        button_layout.addWidget(
            paid_button
        )

        button_layout.addStretch()

        layout.addLayout(
            button_layout
        )

        refresh_button.clicked.connect(
            self.load_bills
        )

        paid_button.clicked.connect(
            self.mark_bill_paid
        )

        # =================================================
        # BILLS TABLE
        # =================================================

        self.bills_table = QTableWidget()

        self.bills_table.setColumnCount(
            9
        )

        self.bills_table.setHorizontalHeaderLabels([
            "Bill ID",
            "Customer",
            "Plan",
            "Amount",
            "GST",
            "Total",
            "Bill Date",
            "Status",
            "Customer ID"
        ])

        self.bills_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.bills_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.bills_table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        layout.addWidget(
            self.bills_table
        )

        self.load_bills()

        return page

    # =====================================================
    # LOAD BILLS
    # =====================================================

    def load_bills(self):

        try:

            cursor.execute("""
                SELECT
                    b.bill_id,
                    c.name,
                    p.plan_name,
                    b.amount,
                    b.gst,
                    b.total_amount,
                    b.bill_date,
                    b.payment_status,
                    b.customer_id
                FROM bills b

                JOIN customer c
                    ON b.customer_id = c.customer_id

                JOIN plans p
                    ON b.plan_id = p.plan_id

                ORDER BY b.bill_id DESC
            """)

            bills = cursor.fetchall()

            self.bills_table.setRowCount(
                len(bills)
            )

            for row, bill in enumerate(
                bills
            ):

                for column, value in enumerate(
                    bill
                ):

                    if column in [3, 4, 5]:

                        try:

                            value = (
                                f"₹ {float(value):.2f}"
                            )

                        except Exception:

                            pass

                    self.bills_table.setItem(
                        row,
                        column,
                        QTableWidgetItem(
                            str(value)
                        )
                    )

            self.bills_table.resizeColumnsToContents()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not load bills:\n{e}"
            )

    # =====================================================
    # MARK BILL AS PAID
    # =====================================================

    def mark_bill_paid(self):

        row = (
            self.bills_table.currentRow()
        )

        if row < 0:

            QMessageBox.warning(
                self,
                "Select Bill",
                "Please select a bill first."
            )

            return

        bill_id = (
            self.bills_table.item(
                row,
                0
            ).text()
        )

        current_status = (
            self.bills_table.item(
                row,
                7
            ).text()
        )

        if current_status == "Paid":

            QMessageBox.information(
                self,
                "Already Paid",
                "This bill is already marked as paid."
            )

            return

        answer = QMessageBox.question(
            self,
            "Confirm Payment",
            f"Mark Bill #{bill_id} as Paid?",
            QMessageBox.Yes |
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:

            return

        try:

            cursor.execute("""
                UPDATE bills
                SET payment_status = 'Paid'
                WHERE bill_id = %s
            """, (
                bill_id,
            ))

            conn.commit()

            QMessageBox.information(
                self,
                "Payment Updated",
                f"Bill #{bill_id} has been marked as Paid."
            )

            self.load_bills()

            self.load_dashboard_data()

        except Exception as e:

            conn.rollback()

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not update payment status:\n{e}"
            )

    # =====================================================
    # PLACEHOLDER PAGE
    # =====================================================

    def create_page(self, title):

        page = QWidget()

        layout = QVBoxLayout(
            page
        )

        layout.setContentsMargins(
            30, 30, 30, 30
        )

        heading = QLabel(
            title
        )

        heading.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)

        layout.addWidget(
            heading
        )

        layout.addStretch()

        return page


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )

    # Start with dark theme
    apply_theme(
        app,
        "dark"
    )

    window = DashboardWindow()

    window.show()

    sys.exit(
        app.exec()
    )
