LIGHT_THEME = """
QMainWindow {
    background-color: #f5f7fa;
}

QWidget {
    font-family: Arial;
    font-size: 14px;
    color: #222222;
}

QFrame {
    background-color: #ffffff;
    border: 1px solid #d9dee7;
    border-radius: 8px;
}

QLabel {
    background-color: transparent;
    color: #222222;
}

QPushButton {
    background-color: #e9edf3;
    color: #222222;
    border: 1px solid #d9dee7;
    border-radius: 6px;
    padding: 10px;
}

QPushButton:hover {
    background-color: #d9e0ea;
}

QPushButton:pressed {
    background-color: #cbd4e0;
}

QLineEdit,
QComboBox,
QSpinBox,
QDoubleSpinBox {
    background-color: #ffffff;
    color: #222222;
    border: 1px solid #c5ccd6;
    border-radius: 5px;
    padding: 7px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #222222;
    selection-background-color: #cfe2ff;
    selection-color: #222222;
}

QTableWidget {
    background-color: #ffffff;
    color: #222222;
    gridline-color: #d9dee7;
    border: 1px solid #d9dee7;
    border-radius: 5px;
}

QTableWidget::item {
    padding: 5px;
}

QTableWidget::item:selected {
    background-color: #cfe2ff;
    color: #222222;
}

QHeaderView::section {
    background-color: #e9edf3;
    color: #222222;
    padding: 8px;
    border: none;
    font-weight: bold;
}

QDialog {
    background-color: #f5f7fa;
}

QMessageBox {
    background-color: #ffffff;
    color: #222222;
}

QMessageBox QLabel {
    color: #222222;
}

QDialogButtonBox QPushButton {
    min-width: 80px;
}
"""


# =========================================================
# DARK THEME
# =========================================================

DARK_THEME = """
QMainWindow {
    background-color: #121212;
}

QWidget {
    font-family: Arial;
    font-size: 14px;
    color: #eeeeee;
}

QFrame {
    background-color: #1e1e1e;
    border: 1px solid #333333;
    border-radius: 8px;
}

QLabel {
    background-color: transparent;
    color: #eeeeee;
}

QPushButton {
    background-color: #2b2b2b;
    color: #eeeeee;
    border: 1px solid #3a3a3a;
    border-radius: 6px;
    padding: 10px;
}

QPushButton:hover {
    background-color: #383838;
}

QPushButton:pressed {
    background-color: #444444;
}

QLineEdit,
QComboBox,
QSpinBox,
QDoubleSpinBox {
    background-color: #252525;
    color: #eeeeee;
    border: 1px solid #444444;
    border-radius: 5px;
    padding: 7px;
}

QComboBox QAbstractItemView {
    background-color: #252525;
    color: #eeeeee;
    selection-background-color: #3d5a80;
    selection-color: #ffffff;
}

QTableWidget {
    background-color: #1e1e1e;
    color: #eeeeee;
    gridline-color: #3a3a3a;
    border: 1px solid #333333;
    border-radius: 5px;
}

QTableWidget::item {
    padding: 5px;
}

QTableWidget::item:selected {
    background-color: #3d5a80;
    color: #ffffff;
}

QHeaderView::section {
    background-color: #2b2b2b;
    color: #eeeeee;
    padding: 8px;
    border: none;
    font-weight: bold;
}

QDialog {
    background-color: #1e1e1e;
}

QMessageBox {
    background-color: #1e1e1e;
    color: #eeeeee;
}

QMessageBox QLabel {
    color: #eeeeee;
}

QDialogButtonBox QPushButton {
    min-width: 80px;
}
"""


# =========================================================
# APPLY THEME
# =========================================================

def apply_theme(app, theme="dark"):
    """
    Apply the selected theme.

    theme can be:
        "dark"
        "light"
    """

    if theme.lower() == "light":
        app.setStyleSheet(LIGHT_THEME)
    else:
        app.setStyleSheet(DARK_THEME)


# =========================================================
# TOGGLE THEME
# =========================================================

def toggle_theme(app, current_theme):
    """
    Switch between light and dark themes.

    Returns the new theme name.
    """

    if current_theme == "dark":

        new_theme = "light"

    else:

        new_theme = "dark"

    apply_theme(
        app,
        new_theme
    )

    return new_theme
