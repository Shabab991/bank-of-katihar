"""
app.py — Bank of Katihar (Web Edition)
========================================
A web-based banking demo application built with Flask and SQLite.

Features:
- User registration and login
- Password hashing
- Session-based authentication
- Account dashboard
- Balance checking
- Money transfers
- Transaction history
- Profile page

Run locally:
    pip install -r requirements.txt
    python app.py

Then open:
    http://localhost:5000
"""

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

# Use an environment variable in production.
# Local development will use the fallback value.
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "dev-secret-key-change-this-in-production"
)

DB_PATH = Path(__file__).resolve().parent / "bank.db"


# ---------------------------------------------------------------------
# DATABASE
# ---------------------------------------------------------------------

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            father_name TEXT,
            mother_name TEXT,
            address TEXT,
            account_type TEXT NOT NULL,
            dob TEXT,
            aadhar_number TEXT,
            phone_number TEXT,
            account_number TEXT UNIQUE NOT NULL,
            balance REAL NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_username TEXT NOT NULL,
            to_username TEXT NOT NULL,
            amount REAL NOT NULL,
            note TEXT,
            created_at TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()


def generate_account_number(conn):
    """Generate a sequential-looking account number: BOK + 8 digits."""
    row = conn.execute(
        "SELECT COUNT(*) AS c FROM users"
    ).fetchone()

    seq = row["c"] + 1

    return f"BOK{seq:08d}"


# ---------------------------------------------------------------------
# AUTH HELPERS
# ---------------------------------------------------------------------

def current_user():
    if "username" not in session:
        return None

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (session["username"],)
    ).fetchone()

    conn.close()

    return user


def login_required(view):
    def wrapped(*args, **kwargs):

        if not current_user():
            flash("Please log in to continue.", "error")
            return redirect(url_for("login"))

        return view(*args, **kwargs)

    wrapped.__name__ = view.__name__

    return wrapped


# ---------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------

@app.route("/")
def index():

    if current_user():
        return redirect(url_for("dashboard"))

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template("register.html")

    form = request.form

    required = [
        "first_name",
        "last_name",
        "account_type",
        "username",
        "password",
        "confirm_password"
    ]

    for field in required:

        if not form.get(field, "").strip():

            flash(
                f"'{field.replace('_', ' ').title()}' is required.",
                "error"
            )

            return render_template(
                "register.html",
                form=form
            )

    if form["password"] != form["confirm_password"]:

        flash(
            "Passwords do not match.",
            "error"
        )

        return render_template(
            "register.html",
            form=form
        )

    if len(form["password"]) < 6:

        flash(
            "Password must be at least 6 characters.",
            "error"
        )

        return render_template(
            "register.html",
            form=form
        )

    conn = get_db()

    existing = conn.execute(
        "SELECT id FROM users WHERE username = ?",
        (form["username"],)
    ).fetchone()

    if existing:

        conn.close()

        flash(
            "That username is already taken.",
            "error"
        )

        return render_template(
            "register.html",
            form=form
        )

    account_number = generate_account_number(conn)

    conn.execute(
        """
        INSERT INTO users
        (
            username,
            password_hash,
            first_name,
            last_name,
            father_name,
            mother_name,
            address,
            account_type,
            dob,
            aadhar_number,
            phone_number,
            account_number,
            balance,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            form["username"],
            generate_password_hash(form["password"]),
            form["first_name"],
            form["last_name"],
            form.get("father_name", ""),
            form.get("mother_name", ""),
            form.get("address", ""),
            form["account_type"],
            form.get("dob", ""),
            form.get("aadhar_number", ""),
            form.get("phone_number", ""),
            account_number,
            1000.0,
            datetime.now(timezone.utc).isoformat(),
        ),
    )

    conn.commit()
    conn.close()

    flash(
        f"Account created! Your account number is {account_number}. Please log in.",
        "success"
    )

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get(
        "username",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    )

    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    conn.close()

    if user is None or not check_password_hash(
        user["password_hash"],
        password
    ):

        flash(
            "Invalid username or password.",
            "error"
        )

        return render_template(
            "login.html"
        )

    session["username"] = user["username"]

    flash(
        f"Welcome back, {user['first_name']}!",
        "success"
    )

    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You've been logged out.",
        "success"
    )

    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():

    user = current_user()

    conn = get_db()

    transactions = conn.execute(
        """
        SELECT *
        FROM transactions
        WHERE from_username = ?
           OR to_username = ?
        ORDER BY created_at DESC
        LIMIT 10
        """,
        (
            user["username"],
            user["username"]
        ),
    ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        user=user,
        transactions=transactions
    )


@app.route("/transfer", methods=["GET", "POST"])
@login_required
def transfer():

    user = current_user()

    if request.method == "GET":

        return render_template(
            "transfer.html",
            user=user
        )

    to_account = request.form.get(
        "to_account",
        ""
    ).strip()

    note = request.form.get(
        "note",
        ""
    ).strip()

    try:

        amount = float(
            request.form.get(
                "amount",
                "0"
            )
        )

    except ValueError:

        flash(
            "Enter a valid amount.",
            "error"
        )

        return render_template(
            "transfer.html",
            user=user
        )

    if amount <= 0:

        flash(
            "Amount must be greater than zero.",
            "error"
        )

        return render_template(
            "transfer.html",
            user=user
        )

    if amount > user["balance"]:

        flash(
            "Insufficient balance for this transfer.",
            "error"
        )

        return render_template(
            "transfer.html",
            user=user
        )

    conn = get_db()

    recipient = conn.execute(
        """
        SELECT *
        FROM users
        WHERE account_number = ?
           OR username = ?
        """,
        (
            to_account,
            to_account
        )
    ).fetchone()

    if recipient is None:

        conn.close()

        flash(
            "Recipient account not found.",
            "error"
        )

        return render_template(
            "transfer.html",
            user=user
        )

    if recipient["username"] == user["username"]:

        conn.close()

        flash(
            "You can't transfer money to yourself.",
            "error"
        )

        return render_template(
            "transfer.html",
            user=user
        )

    conn.execute(
        """
        UPDATE users
        SET balance = balance - ?
        WHERE username = ?
        """,
        (
            amount,
            user["username"]
        )
    )

    conn.execute(
        """
        UPDATE users
        SET balance = balance + ?
        WHERE username = ?
        """,
        (
            amount,
            recipient["username"]
        )
    )

    conn.execute(
        """
        INSERT INTO transactions
        (
            from_username,
            to_username,
            amount,
            note,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            user["username"],
            recipient["username"],
            amount,
            note,
            datetime.now(timezone.utc).isoformat()
        )
    )

    conn.commit()
    conn.close()

    flash(
        f"₹{amount:,.2f} sent to "
        f"{recipient['first_name']} "
        f"{recipient['last_name']} "
        f"({recipient['account_number']}).",
        "success"
    )

    return redirect(
        url_for("dashboard")
    )


@app.route("/profile")
@login_required
def profile():

    user = current_user()

    return render_template(
        "profile.html",
        user=user
    )


# ---------------------------------------------------------------------
# APPLICATION START
# ---------------------------------------------------------------------

if __name__ == "__main__":

    init_db()

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )