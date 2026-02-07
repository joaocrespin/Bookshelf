# 📚 Bookshelf

**Bookshelf** is a web application designed to help readers manage and organize the books and comics they have read or are currently reading.

## Motivation & Learning Goals

This project was born from two main inspirations:
1.  **Practical Need:** The difficulty of keeping track of book and comic progress during busy academic periods, such as exams and college projects.
2.  **Learning Journey:** This project served as a **hands-on exercise to learn the Flask web framework and SQLAlchemy** for efficient database management and web development.

## Tech Stack
*   **Back-end:** Python using the **Flask** framework.
*   **ORM/Database:** **SQLAlchemy** and SQLite for data persistence.
*   **Front-end:** HTML, CSS, and JavaScript.

## Getting Started

Follow these steps to set up and run the project locally:

### Prerequisites
Ensure you have **Python** installed on your machine.

### Installation & Execution
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/joaocrespin/Bookshelf.git
    cd Bookshelf
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *This installs all necessary libraries, including Flask and SQLAlchemy.*

3.  **Initialize the database:**
    ```bash
    python createdb.py
    ```
    *This script sets up the initial database structure using the defined models.*

4.  **Run the application:**
    ```bash
    flask run
    ```
    *The server will start, and you can access the app in your web browser.*

## Project Structure

*   `/static`: Contains CSS and JavaScript files.
*   `/templates`: Contains the HTML interface files.
*   `app.py`: The main application logic and routes.
*   `models.py`: Database schema definitions using SQLAlchemy.
*   `createdb.py`: Script for database initialization.
