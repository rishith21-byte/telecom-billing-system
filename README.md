# Telecom Billing System

A Python and MySQL based Telecom Billing System designed to manage customers, telecom plans, billing operations, and reports through a simple dashboard interface.

## 📌 Project Overview

The Telecom Billing System automates basic telecom service management and billing activities.

The system allows users to:

* Add, view, update, and delete customer records
* Add and view telecom plans
* Manage plan details such as price, validity, and data limit
* Generate customer bills
* View billing and system reports
* Manage data through a MySQL database
* Access the system through a dashboard interface

## 🚀 Features

### Customer Management

* Add new customers
* View existing customers
* Update customer information
* Delete customer records

### Plan Management

* Add new telecom plans
* View available plans
* Store plan price
* Store plan validity
* Store data limits

### Billing Management

* Generate bills for customers
* Calculate billing information based on the selected plan
* Store billing records in the database

### Reports

* View billing-related information
* Display system records through the reports section
* Provide a centralized view of system data

### Dashboard

The dashboard provides a centralized interface for accessing the major modules of the Telecom Billing System.

## 🛠️ Technologies Used

* **Python** – Application development and business logic
* **MySQL** – Database management and data storage
* **Pyside6** – Dashboard and user interface
* **MySQL Connector for Python** – Database connectivity

## 📂 Project Structure

```text
telecom-billing-system/
│
├── dashboard.py        # Main dashboard/interface
├── customer.py         # Customer management operations
├── plans.py            # Telecom plan management
├── billing.py          # Billing and bill generation
├── reports.py          # Reports module
├── db.py               # MySQL database connection
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── .gitignore          # Files excluded from Git
```

> File names may differ slightly depending on the final version of the project.

## 🗄️ Database

The system uses **MySQL** to store and manage application data.

Typical database entities include:

* Customers
* Plans
* Bills / Billing Records

The Python application communicates with MySQL using a database connector.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/rishith21-byte/telecom-billing-system.git
```

### 2. Open the project folder

```bash
cd telecom-billing-system
```

### 3. Install the required Python packages

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

Install MySQL and create the required database.

Update the database configuration in `db.py` with your own MySQL credentials.

**Do not upload your actual database password to GitHub.**

### 5. Run the application

```bash
python dashboard.py
```

## 🔄 System Workflow

```text
Start Application
       ↓
    Dashboard
       ↓
 ┌─────┼──────────┬──────────┐
 ↓     ↓          ↓          ↓
Customer Plans   Billing   Reports
Management       ↓
                 ↓
          Generate Bill
                 ↓
              MySQL
```

## 🎯 Project Objectives

* Automate basic telecom billing operations
* Reduce manual customer and billing record management
* Centralize customer and plan information
* Provide a simple graphical interface for system operations
* Maintain billing data using a relational database

## 🔮 Future Enhancements

The project can be extended with:

* Customer login and authentication
* Admin and user roles
* Bill generation
* Email/SMS bill notifications
* Payment status tracking
* Advanced billing analytics
* Customer churn prediction using machine learning
* Interactive charts and dashboards
* Cloud database integration

## 👨‍💻 Skills Demonstrated

This project demonstrates practical experience with:

* Python programming
* MySQL database management
* CRUD operations
* Database connectivity
* GUI development
* Modular Python programming
* Billing logic
* Software project structure

## 📄 License

This project is developed for educational and portfolio purposes.
