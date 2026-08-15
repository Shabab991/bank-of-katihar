# 🏦 Bank of Katihar — Bank Management System

A modern web-based **Bank Management System** built with **Python Flask, SQLite, HTML, CSS, and JavaScript**.

The application provides a complete banking-style workflow including user authentication, account management, balance tracking, transactions, and money transfers through a responsive web interface.

## 🌐 Live Demo

🔗 https://bank-of-katihar.onrender.com

---

## ✨ Features

* 🔐 User Registration & Login
* 👤 User Profile Management
* 📊 Interactive Banking Dashboard
* 💰 Account Balance Management
* 💸 Money Transfer
* 🧾 Transaction Management
* 🗄️ SQLite Database Integration
* 🎨 Modern Responsive UI
* 🔒 Protected User Functionality
* ☁️ Cloud Deployment with Render

---

## 🖥️ Application Preview

<img width="1887" height="903" alt="Bank of Katihar Dashboard" src="https://github.com/user-attachments/assets/c9fcc84b-7781-4e6d-aef8-3ac3734d1694" />

---

## 🛠️ Tech Stack

| Technology   | Purpose                  |
| ------------ | ------------------------ |
| Python       | Backend programming      |
| Flask        | Web framework            |
| SQLite       | Database                 |
| HTML5        | Application structure    |
| CSS3         | UI and responsive design |
| JavaScript   | Client-side interactions |
| Git & GitHub | Version control          |
| Render       | Cloud deployment         |

---

## 📂 Project Structure

```text
bank-of-katihar/
│
├── app.py
├── bank.db
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── profile.html
│   └── transfer.html
│
└── static/
    └── style.css
```

---

## 🔄 Application Flow

```text
                    ┌─────────────────┐
                    │      User       │
                    └────────┬────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Registration / Login│
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │     Dashboard       │
                  └──────────┬──────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        View Balance    View Profile   Transactions
              │              │              │
              └──────────────┼──────────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Transfer Money  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ SQLite Database │
                    └─────────────────┘
```

---

## 🔐 Security

The application includes authentication and protected banking functionality.

For a real production banking application, additional security measures would be required, including:

* CSRF protection
* Secure password hashing and password policies
* Rate limiting
* Secure secret-key management
* Strong session management
* Input validation and sanitization
* HTTPS enforcement
* Production-grade database
* Audit logging
* Role-based access control

> **Note:** This project is an educational/demo banking application and is not intended for handling real financial transactions or sensitive banking data.

---

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/Shabab991/bank-of-katihar.git
cd bank-of-katihar
```

### 2. Create a virtual environment

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in your browser

```text
http://127.0.0.1:5000
```

---

## ☁️ Deployment

The application is deployed using **Render**.

### Live Application

https://bank-of-katihar.onrender.com

The project can be deployed by connecting the GitHub repository to Render and configuring the required Python environment and start command.

---

## 🚀 Future Improvements

Planned improvements include:

* 🗄️ PostgreSQL production database
* 📧 OTP / Email verification
* 🔑 Password reset functionality
* 👨‍💼 Admin dashboard
* 🧾 Transaction receipt generation
* 📄 Account statement download
* 🔌 REST API
* 🔐 Advanced security and monitoring
* 💾 Persistent production storage
* 📱 Mobile application

---

## 🎯 Project Highlights

This project demonstrates practical experience with:

* Backend development using Flask
* CRUD operations
* Database management with SQLite
* User authentication
* Session-based application flow
* Financial transaction logic
* Responsive web development
* Git/GitHub workflow
* Cloud deployment
* Basic web application security considerations

---

## 👨‍💻 Author

**Shabab Ahmad**

MCA Student | Aspiring Data Engineer | Python • SQL • AWS • ML/AI

GitHub: https://github.com/Shabab991

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
