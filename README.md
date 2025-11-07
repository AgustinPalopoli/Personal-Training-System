
# 🏋️ Personal Trainer Web App

A complete fullstack web application developed with **Django**, **PostgreSQL**, and **JavaScript**, designed for a **personal trainer** to manage client routines, exercises, and progress.
It includes multiple user roles (Admin, Premium User, Free User), RESTful CRUD operations, and a responsive minimalist UI.

---

## 🧩 Distinctiveness and Complexity

This project satisfies distinctiveness and complexity requirements by combining:

* A **unique, minimalist design** with full mobile responsiveness.
* **Multiple data models** and complex backend logic for role-based features.
* **Dynamic frontend interactions** powered by JavaScript for an engaging user experience.

Overall, it provides a complete and realistic gym management system that balances usability with technical depth.

---

## ⚙️ Main Features

### 🔐 General Functions

* User authentication (register, login, logout)
* Password recovery via email
* Permission decorators to prevent unauthorized access
* Role-based access control (Admin / Premium / Free)

---

### 👑 Admin Panel

Admins can:

* **Manage exercises** (CRUD): type, muscle, name, sets, reps, rest, weight, image
* **Manage routines** (CRUD): name, user type, target gender
* **Manage users**: list, add, delete, reset password, upgrade account, view weights
* **Upload motivational phrases** from `.txt` files
* **Create chalkboards** assigning 5 routines and custom messages per user

---

### 💪 Premium User

Premium users can:

* View **assigned routines** (with AI-generated images + custom messages)
* Perform exercises **progressively**:

  * Start sets
  * Rest timer with auto-increment counter
  * Completion message at the end
* View and update lifted weights in real time
* View all weight-based exercises
* Access stretching exercises

---

### 🧍 Free User

Free users can:

* View **preloaded routines** (with AI-generated images)
* Perform exercises progressively using the same timer system
* See **premium benefits** and contact the staff for upgrade information

---

## 🎨 Style & File Structure

```
📦 project_root
 ┣ 📂 inicio/                # Static files for the homepage  
 ┣ 📂 css/                   # All CSS files  
 ┣ 📂 imagenes/              # Exercise images  
 ┣ 📂 imageDesign/           # Design images  
 ┣ 📂 js/                    # JavaScript files for user interaction  
 ┣ 📂 sonido/                # Audio files (rest & finish sounds)
```

---

## 🧠 Template Tags

Custom Python filters for Django templates:

1. Returns a random integer to display a random design image.
2. Returns a boolean to check if time equals `0:00:00`.

---

## 🧱 Templates Overview

| Folder           | Description                       |
| ---------------- | --------------------------------- |
| `base_`          | Base templates extended by others |
| `admin_`         | Templates for the admin interface |
| `inicio`         | Homepage template                 |
| `iniciar_sesion` | Login page                        |
| `redireccion`    | Redirects users by role           |
| `resetear_`      | Password reset templates          |
| `usuario_`       | Premium user templates            |
| `usuario_g_`     | Free user templates               |

---

## 🚀 How to Run the Application

1. Set up **PostgreSQL** and configure the connection in `settings.py`.
2. Add your email in `EMAIL_HOST_USER`.
3. Generate an **App Password** for that email and paste it into `EMAIL_HOST_PASSWORD`.
4. Run migrations and create a superuser:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```
5. Log in and create an admin account through the UI.

---

## 🛠️ Tech Stack

* **Backend:** Django (Python)
* **Database:** PostgreSQL
* **Frontend:** HTML, CSS, JavaScript
* **Architecture:** MVC, REST APIs, CRUD
* **Deployment:** Virtualized environments

---
