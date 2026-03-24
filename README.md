# English Irregular Verbs Learning App

A modern Django-based web application for learning English irregular verbs. Features include interactive quizzes, progress tracking, and a beautiful responsive UI similar to Duolingo-style learning platforms.

![Django](https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3+-7952B3?style=for-the-badge&logo=bootstrap)

## ✨ Features

- **User Authentication**: Login/Register system with Django's built-in auth
- **Three Quiz Types**:
  - Fill in the Past Forms
  - Multiple Choice
  - Translation (EN → UZ)
- **Progress Tracking**: View statistics and test history
- **Modern UI**: Beautiful, responsive design with animations
- **Admin Panel**: Manage verbs and users

## 📚 Irregular Verbs

The app includes **80+ common English irregular verbs** with:
- Base Form
- Past Simple
- Past Participle
- UK Pronunciation
- Uzbek Translation

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Installation

1. **Clone or download the project**

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows (cmd.exe):
     ```cmd
     venv\Scripts\activate
     ```
   - Windows (PowerShell):
     ```powershell
     venv\Scripts\Activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Load irregular verbs data**:
   ```bash
   python manage.py load_verbs
   ```

7. **Create default users**:
   ```bash
   python manage.py create_users
   ```
   
   This creates:
   - **Test User**: username: `test`, password: `test`
   - **Admin User**: username: `admin`, password: `admin`

8. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

9. **Open your browser**:
   Navigate to `http://127.0.0.1:8000`

## 🔧 Development Commands

### Available Management Commands

| Command | Description |
|---------|-------------|
| `python manage.py migrate` | Apply database migrations |
| `python manage.py load_verbs` | Load 80+ irregular verbs |
| `python manage.py create_users` | Create test and admin users |
| `python manage.py createsuperuser` | Create admin superuser |
| `python manage.py runserver` | Start development server |

### Ngrok Support

The app is configured to work with ngrok for public deployment. The following settings are already in `config/settings.py`:
```python
CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.dev',
    'https://*.ngrok.io',
]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

## 📁 Project Structure

```
english/                    # Project root
├── config/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py         # Main settings
│   ├── urls.py            # URL routing
│   └── wsgi.py            # WSGI config
├── verbs/                  # Main app
│   ├── __init__.py
│   ├── admin.py           # Admin configuration
│   ├── models.py          # Database models
│   ├── urls.py            # App URLs
│   ├── views.py           # Views
│   └── management/
│       └── commands/
│           ├── load_verbs.py    # Load verbs data
│           └── create_users.py  # Create default users
├── templates/              # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Home page
│   ├── quiz.html          # Quiz selection
│   ├── quiz_play.html     # Quiz play
│   ├── result.html        # Results page
│   ├── profile.html       # User profile
│   ├── verbs_list.html    # All verbs
│   └── registration/      # Auth templates
├── static/                # Static files
│   ├── css/style.css      # Custom styles
│   └── js/main.js         # JavaScript
├── media/                 # User uploads
├── manage.py              # Django CLI
├── requirements.txt       # Dependencies
├── .gitignore            # Git ignore
└── README.md             # This file
```

## 🎯 Quiz Types

### 1. Fill in Past Forms
- Write the past simple and past participle forms
- Example: `base: go` → answer: `went / gone`

### 2. Multiple Choice
- Choose the correct past simple form
- 4 options to choose from

### 3. Translation
- Translate from English to Uzbek
- Based on the verb's translation

## 🔐 Default Accounts

| Username | Password | Role |
|----------|----------|------|
| test     | test     | Regular user |
| admin    | admin    | Admin (superuser) |

## 🎨 UI Features

- Responsive design (mobile-friendly)
- Bootstrap 5 integration
- Custom CSS animations
- Progress tracking
- Score visualization
- Clean, modern interface

## 🛠️ Technologies Used

- **Backend**: Django 5.0
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5
- **Database**: SQLite (default)
- **Icons**: Font Awesome 6

## 📝 License

This project is for educational purposes.

## 👨‍💻 Credits

Created with ❤️ for learning English irregular verbs.
