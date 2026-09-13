# Book Sharing Platform

## Project Overview

**Book Sharing Platform** is a web-based application developed as a Final Year Project to provide a simple and convenient platform for users to **share, lend, borrow, and access books**.

The platform allows users to list books they own and make them available to other users. Users can browse available books and request books for borrowing. The platform supports both **physical books** and **digital books**, allowing users to share physical copies as well as digital versions.

The system is designed to encourage **book sharing and community-based access to knowledge**, making it easier for users to find and share books without having to purchase every book individually.

## Key Features

### User Features

* User registration and login
* Secure user authentication
* Browse available books
* Search and discover books
* View book details
* Share books with other users
* Borrow available books
* Support for physical books
* Support for digital books
* Manage shared books
* Manage borrowed books
* User-friendly web interface

### Physical Book Sharing

Users can list their **physical books** on the platform and make them available for other users to borrow.

Users can browse available physical books and request to borrow them from the respective book owner.

### Digital Book Sharing

The platform also supports **digital books**. Users can share digital book resources through the platform, allowing other users to access available digital books according to the platform's functionality.

## Technologies Used

The project is built using the following technologies:

* **Python** – Main programming language
* **Flask** – Web application framework
* **Jinja2** – Template engine
* **HTML5** – Web page structure
* **CSS3** – Styling
* **Bootstrap** – Responsive user interface and styling
* **SQLite** – Database management
* **SQL** – Database queries and data management

## Application Architecture

The application follows a Flask-based web architecture.

```text
User
  │
  ▼
Web Browser
  │
  ▼
Flask Application
  │
  ├── Routes / Application Logic
  │
  ├── Jinja2 Templates
  │
  ├── Bootstrap / CSS
  │
  ▼
SQLite Database
```

## How the Platform Works

### 1. User Registration

A new user can create an account on the platform by providing the required information.

### 2. User Login

Registered users can log in to access the platform's features.

### 3. Share a Book

A user can add a book to the platform and provide relevant information such as:

* Book title
* Author
* Description
* Book type
* Availability
* Other required book information

The book can be listed as either a **physical** or **digital** book.

### 4. Browse Books

Users can browse the available books listed by other users.

### 5. Borrow a Book

When a user finds a book they want to read, they can request or borrow the book according to its availability.

For physical books, the users can arrange the exchange or return of the physical copy according to the platform's implemented borrowing process.

### 6. Digital Books

Digital books can be shared through the platform, allowing users to access available digital resources according to the permissions and functionality implemented by the system.

## Project Setup and Run Instructions

Follow the steps below to set up and run the project on your computer.

### 1. Make Sure Python Is Installed

Make sure **Python** is installed on your system.

Check the installed Python version:

```bash
python --version
```

If `python` does not work, use:

```bash
python3 --version
```

### 2. Create a Virtual Environment

Creating a virtual environment is **optional but recommended**.

Run:

```bash
python -m venv venv
```

This will create a virtual environment named `venv`.

### 3. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Mac / Linux

```bash
source venv/bin/activate
```

After successful activation, you should see `(venv)` in your terminal.

### 4. Install Required Packages

Install all required dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

If `pip` does not work, use:

```bash
pip3 install -r requirements.txt
```

### 5. Run the Project

Start the application using:

```bash
python run.py
```

If `python` does not work, use:

```bash
python3 run.py
```

The Flask application should then start successfully.

## Quick Setup

The complete setup can be summarized as follows:

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Mac / Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python run.py
```

If necessary:

```bash
python3 run.py
```

## Requirements

Before running the project, make sure the following are installed:

* Python 3.x
* pip
* A web browser
* Project source code
* Internet connection for installing Python dependencies

## Database

The application uses **SQLite** as its database.

SQLite provides a lightweight relational database solution suitable for this project. The database is used to store application data such as:

* User information
* Book information
* Book availability
* Borrowing information
* Sharing information
* Other application-related records

## Project Benefits

The Book Sharing Platform provides several benefits:

* Encourages people to share books with others
* Makes books easier to discover
* Provides a platform for borrowing physical books
* Supports digital book sharing
* Reduces the need to purchase every book individually
* Promotes community-based knowledge sharing
* Provides an easy-to-use web-based platform

## Future Improvements

The platform can be further improved by adding features such as:

* Book rating and review system
* Advanced book search and filtering
* User-to-user messaging
* Notifications for borrowing requests
* Book return reminders
* Location-based physical book sharing
* Book recommendation system
* Improved digital book management
* Admin dashboard
* Email notifications
* More advanced user profiles
* Deployment to a cloud server

## Project Purpose

This application was developed as a **Final Year Project** to demonstrate practical knowledge of web application development using Python and Flask.

The project combines backend development, frontend design, database management, authentication, and template rendering to create a functional **book sharing and borrowing platform**.

## Author

**M Sabeel Aslam**

Final Year Project
**Virtual University Of Pakistan**
**Bachelor's degree of Computer science**

## License

This project was developed for academic and educational purposes.
