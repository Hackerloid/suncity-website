# SUNCITY TECHNOLOGY - Django Website

This is a Django-based web application for SUNCITY TECHNOLOGY.

## How to Launch the Application

1. **Open Terminal**: Open your terminal or Command Prompt.
2. **Navigate to the Project Directory**: Ensure you are in `c:\Users\HACKERLOID\Desktop\suncity-website`.
3. **Run the Server**: Execute the following command:
   ```bash
   python manage.py runserver
   ```
4. **View the Website**: Open your browser and go to:
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## How to Access the Admin Panel

The admin panel allows you to view contact form submissions.

1. **Create a Superuser**: In your terminal, run:
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to set a username, email, and password.
2. **Login to Admin**: Once the server is running, go to:
   [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
3. **View Submissions**: Look for the "Contact Submissions" section under the "Website" app.

## Project Structure

- `suncity_project/`: Project configuration (settings, URLs).
- `website/`: The main web application (views, models, templates).
- `static/`: Frontend assets (CSS, JS, Images).
- `templates/`: HTML templates.
