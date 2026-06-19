# Bookmark Saver

Bookmark Saver is a feature-rich Flask web application designed for users to efficiently organize their web bookmarks. The application provides a secure environment where users can manage their URLs through a personalized dashboard.

## Features

* **User Authentication**: Secure sign-up and sign-in functionality to keep bookmarks private.
* **Bookmark Management**: Easily create, view, edit, and delete bookmarks.
* **Organization**: Categorize your links by creating custom folders.
* **Favorites**: Mark specific bookmarks as favorites for quick access.
* **Search**: Built-in search functionality to help you find your bookmarks instantly.
* **Sharing**: Easily share bookmark URLs by copying them to your clipboard.

## Technical Stack

* **Backend**: Flask (Python)
* **Server**: Gunicorn (for deployment)
* **Frontend**: HTML5, CSS3, and JavaScript (with Font Awesome icons)
* **Data Storage**: In-memory database

## Installation and Usage

1.  **Clone the repository.**
2.  **Install dependencies**:
    ```bash
    pip install Flask==3.0.3 gunicorn==22.0.0
    ```
3.  **Run the application**:
    ```bash
    python app.py
    ```
4.  **Access the app**: Open your browser and navigate to the local development server (typically `http://127.0.0.1:5000`).

## Deployment

This application is designed for easy deployment on cloud platforms like Render, utilizing Gunicorn as the production server.
