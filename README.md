
<div align="center">

# MultiVendorFoodEcom


</div>

This repository contains the code for a MultiVendorFoodEcom application. The purpose is to provide a platform where multiple vendors can offer food items, creating a diverse online marketplace for food enthusiasts.

## ✨ Features

-   User Authentication: Secure registration and login functionalities for both vendors and customers.
-   Vendor Management: Tools and interfaces for vendors to manage their profile, menu, and orders.
-   Menu Building: Vendors can create and manage food categories and items.
-   Customer Interface: Easy browsing and ordering experience for customers.
-   Order Management: System to handle order processing, tracking, and completion.
-   Close Vendors: Finding vendors close to you through google places API (coming soon)

## 📑 Table of Contents

-   [Installation](#-installation)
-   [Running the Project](#-running-the-project)
-   [Dependencies](#-dependencies)
-   [Contribution Guide](#-contribution-guide)


## ⚙️ Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/mayurexh/MutliVendorFoodEcom.git
    cd MutliVendorFoodEcom
    ```

2.  Create a virtual environment (recommended):

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # On Linux/macOS
    venv\Scripts\activate.bat  # On Windows
    ```

3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt # If you have a requirements.txt file
    pip install django decouple psycopg2 # Otherwise install listed dependencies
    ```

4.  Create a `.env` file in the project root directory.

    ```bash
    touch .env
    ```

5.  Add the following environment variables to your `.env` file:

    ```
    SECRET_KEY=your_django_secret_key
    DEBUG=True/False
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_HOST=your_db_host

    EMAIL_HOST=your_email_host
    EMAIL_PORT=your_email_port
    EMAIL_HOST_USER=your_email_host_user
    ```

    Ensure the `SECRET_KEY` is a strong, randomly generated string, especially for production.
    Adjust the `DEBUG` variable according to your environment. `True` for development, `False` for production.
    Database credentials should match your PostgreSQL database configuration.

## 🚀 Running the Project

1.  Apply the migrations:

    ```bash
    python manage.py migrate
    ```

2.  Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

3.  Run the development server:

    ```bash
    python manage.py runserver
    ```

    Open your browser and navigate to `http://127.0.0.1:8000/` to view the application.

## 🔩 Dependencies

-   **Django**: A high-level Python web framework that encourages rapid development and clean, pragmatic design.
-   **python-decouple**: Helps to organize settings so that you can change parameters without redeploying.
-   **psycopg2**: The most popular PostgreSQL adapter for Python.
-   **jquery**: A JavaScript library designed to simplify HTML DOM tree traversal and manipulation, as well as event handling, CSS animation, and Ajax.
-   **bootstrap**: A popular CSS framework for developing responsive and mobile-first websites.
-   
## 🤝 Contribution Guide

Contributions are welcome! Here's how you can contribute:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Implement your changes and ensure they are well-tested.
4.  Submit a pull request with a clear description of your changes.

