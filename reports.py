from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)

from PySide6.QtCore import Qt

from db import cursor


class ReportsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()
        self.load_report_data()

    # =====================================================
    # SETUP UI
    # =====================================================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            30, 30, 30, 30
        )

        layout.setSpacing(15)

        # =================================================
        # HEADING
        # =================================================

        heading = QLabel("Reports")

        heading.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)

        layout.addWidget(heading)

        subtitle = QLabel(
            "Telecom billing system reports and statistics"
        )

        subtitle.setStyleSheet("""
            font-size: 16px;
        """)

        layout.addWidget(subtitle)

        # =================================================
        # SUMMARY CARDS
        # =================================================

        cards_layout = QHBoxLayout()

        # -----------------------------------------------
        # Customers
        # -----------------------------------------------

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

        self.customer_value = QLabel("0")

        self.customer_value.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        customer_layout.addWidget(
            customer_title
        )

        customer_layout.addWidget(
            self.customer_value
        )

        cards_layout.addWidget(
            customer_card
        )

        # -----------------------------------------------
        # Total Bills
        # -----------------------------------------------

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

        self.bills_value = QLabel("0")

        self.bills_value.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        bills_layout.addWidget(
            bills_title
        )

        bills_layout.addWidget(
            self.bills_value
        )

        cards_layout.addWidget(
            bills_card
        )

        # -----------------------------------------------
        # Paid Bills
        # -----------------------------------------------

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

        self.paid_value = QLabel("0")

        self.paid_value.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        paid_layout.addWidget(
            paid_title
        )

        paid_layout.addWidget(
            self.paid_value
        )

        cards_layout.addWidget(
            paid_card
        )

        # -----------------------------------------------
        # Unpaid Bills
        # -----------------------------------------------

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

        self.unpaid_value = QLabel("0")

        self.unpaid_value.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        unpaid_layout.addWidget(
            unpaid_title
        )

        unpaid_layout.addWidget(
            self.unpaid_value
        )

        cards_layout.addWidget(
            unpaid_card
        )

        layout.addLayout(
            cards_layout
        )

        # =================================================
        # REVENUE
        # =================================================

        revenue_card = QFrame()

        revenue_card.setFrameShape(
            QFrame.StyledPanel
        )

        revenue_layout = QVBoxLayout(
            revenue_card
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
            font-size: 30px;
            font-weight: bold;
        """)

        revenue_layout.addWidget(
            revenue_title
        )

        revenue_layout.addWidget(
            self.revenue_value
        )

        layout.addWidget(
            revenue_card
        )

        # =================================================
        # REPORT TABLE
        # =================================================

        table_title = QLabel(
            "Billing Summary"
        )

        table_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        layout.addWidget(
            table_title
        )

        self.report_table = QTableWidget()

        self.report_table.setColumnCount(5)

        self.report_table.setHorizontalHeaderLabels([
            "Bill ID",
            "Customer",
            "Plan",
            "Total Amount",
            "Payment Status"
        ])

        self.report_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.report_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.report_table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        layout.addWidget(
            self.report_table
        )

        # =================================================
        # REFRESH BUTTON
        # =================================================

        button_layout = QHBoxLayout()

        refresh_button = QPushButton(
            "Refresh Reports"
        )

        refresh_button.setMinimumHeight(
            40
        )

        refresh_button.clicked.connect(
            self.load_report_data
        )

        button_layout.addWidget(
            refresh_button
        )

        button_layout.addStretch()

        layout.addLayout(
            button_layout
        )

    # =====================================================
    # LOAD REPORT DATA
    # =====================================================

    def load_report_data(self):

        try:

            # ---------------------------------------------
            # TOTAL CUSTOMERS
            # ---------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM customer
            """)

            total_customers = cursor.fetchone()[0]

            self.customer_value.setText(
                str(total_customers)
            )

            # ---------------------------------------------
            # TOTAL BILLS
            # ---------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM bills
            """)

            total_bills = cursor.fetchone()[0]

            self.bills_value.setText(
                str(total_bills)
            )

            # ---------------------------------------------
            # PAID BILLS
            # ---------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM bills
                WHERE payment_status = 'Paid'
            """)

            paid_bills = cursor.fetchone()[0]

            self.paid_value.setText(
                str(paid_bills)
            )

            # ---------------------------------------------
            # UNPAID BILLS
            # ---------------------------------------------

            cursor.execute("""
                SELECT COUNT(*)
                FROM bills
                WHERE payment_status = 'Unpaid'
            """)

            unpaid_bills = cursor.fetchone()[0]

            self.unpaid_value.setText(
                str(unpaid_bills)
            )

            # ---------------------------------------------
            # REVENUE
            # ---------------------------------------------

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

            # ---------------------------------------------
            # BILL TABLE
            # ---------------------------------------------

            cursor.execute("""
                SELECT
                    b.bill_id,
                    c.name,
                    p.plan_name,
                    b.total_amount,
                    b.payment_status
                FROM bills b

                JOIN customer c
                    ON b.customer_id = c.customer_id

                JOIN plans p
                    ON b.plan_id = p.plan_id

                ORDER BY b.bill_id DESC
            """)

            bills = cursor.fetchall()

            self.report_table.setRowCount(
                len(bills)
            )

            for row, bill in enumerate(bills):

                bill_id = bill[0]
                customer_name = bill[1]
                plan_name = bill[2]
                total_amount = bill[3]
                status = bill[4]

                values = [
                    bill_id,
                    customer_name,
                    plan_name,
                    f"₹ {float(total_amount):.2f}",
                    status
                ]

                for column, value in enumerate(
                    values
                ):

                    item = QTableWidgetItem(
                        str(value)
                    )

                    item.setTextAlignment(
                        Qt.AlignCenter
                    )

                    self.report_table.setItem(
                        row,
                        column,
                        item
                    )

            self.report_table.resizeColumnsToContents()

        except Exception as e:

            QMessageBox.critical(
                self,
                "Report Error",
                f"Could not load reports:\n{e}"
            )
