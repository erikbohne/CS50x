import os
import pytz
import csv
import pandas as pd

from cs50 import SQL
from flask import Flask, flash, render_template, redirect, request, session
from flask_session import Session
from tempfile import mkdtemp
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology, date_from_weekday, weekday

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 library to use SQLite database
db = SQL("sqlite:///sykkel.db")

@app.route("/")
@login_required
def index():
    """ Show available bikes and handle submitting a booking"""

    # Handle the GET request: showing the available bikes:
    day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    # Get info about the current day
    date = datetime.now()
    week = date.strftime("%W")
    year = date.strftime("%Y")

    # Query for any bookings the current week
    bookings = db.execute("SELECT * FROM booking WHERE week = ? AND year = ?", week, year)

    # Query for status on bikes
    status = db.execute("SELECT * FROM bikes")

    available = [None] * 3
    for i in range(3):
        available[i] = {
            0: None,
            1: None,
            2: None,
            3: None,
            4: None
        }

    # Add the booked bikes to a list
    for i in range(len(bookings)):
        bike = int(bookings[i]["bikeID"])
        weekday = int(bookings[i]["day"]) - 1
        available[bike][weekday] = "red"


    return render_template("index.html", day=day, week=week, available=available, status=status)


@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    """A page for admins"""

    # Handle a POST request (submitted a form)
    if request.method == "POST":

        # Check which bike was submitted
        if request.form.get("0"):
            bike = 0
        elif request.form.get("1"):
            bike = 1
        elif request.form.get("2"):
            bike = 2

        # Query for current status
        curr = db.execute("SELECT status FROM bikes WHERE bikeID = ?", bike)

        # Change status
        if curr[0]["status"] == 0:
            db.execute("UPDATE bikes SET status = 1 WHERE bikeID = ?", bike)
        elif curr[0]["status"] == 1:
            db.execute("UPDATE bikes SET status = 0 WHERE bikeID = ?", bike)

        return redirect("/admin")

    else:

        # Ensure user has admin access
        admin_ID = [1]
        user_ID = session["user_id"]
        if user_ID not in admin_ID:
            return redirect("/")

        # Query for all bike bookings
        booking = db.execute("SELECT booking.bookingID, users.firstname, users.surname, booking.bikeID, booking.day, booking.week, users.mail, booking.date, booking.time FROM users JOIN booking ON users.id = booking.userID ORDER BY bookingID DESC")

        # Query for reports
        reports = db.execute("SELECT date, time, bikeID, message, users.mail, users.firstname, users.surname FROM reports JOIN users ON reports.userID = users.id WHERE status = 0 ORDER BY reportID")

        # Query for bike status
        status = db.execute("SELECT * FROM bikes")

        return render_template("admin.html", booking=booking, n=len(booking), active=reports, m=len(reports), status=status)

@app.route("/book", methods=["GET", "POST"])
@login_required
def book():
    """Adds the booking to the database and sends confirmation"""

    # Ensure route was requested via POST (form was submitted)
    if request.method == "POST":

        # Add booking to sykkel.db
        GMT = pytz.timezone('Europe/Oslo')
        timestamp = datetime.now(GMT)
        time = timestamp.strftime("%X")
        db.execute("INSERT INTO booking (userID, bikeID, day, week, month, year, date, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   session["user_id"], int(request.form.get("bike")) - 1, int(request.form.get("weekday")) + 1, request.form.get("week"),
                   request.form.get("month"), request.form.get("year"), timestamp, time)

        return redirect("/")

    # If route requested via GET (no form submitted)
    else:
        return redirect("/")


@app.route("/changepass", methods=["GET", "POST"])
@login_required
def changepass():
    """Change users password"""

    # Ensure route was requested via POST (submitted form)
    if request.method == "POST":

        # Query for old password
        old = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])

        # Ensure user has submitted the former password and it's correct
        if not request.form.get("old_pass") or not check_password_hash(old[0]["hash"], request.form.get("old_pass")):
            return apology("The old password was incorrect")

        # Ensure user has submitted the new password
        if not request.form.get("new_pass") or not request.form.get("conf_pass"):
            return apology("You need to enter a new password")

        # Ensure new passwords match
        if request.form.get("new_pass") != request.form.get("conf_pass"):
            return apology("New password do not match...")

        # Change the password
        db.execute("UPDATE users SET hash = ? WHERE id = ?",
                   generate_password_hash(request.form.get("new_pass")), session["user_id"])

        return redirect("/")

    # If the route was requested via GET
    else:
        return render_template("changepass.html")


@app.route("/confirmation", methods=["GET", "POST"])
@login_required
def confirmation():
    """ Confirms the booking """

    # Ensure route was requested via POST (submitted a form)
    if request.method == "POST":

        # Check which bike was submitted
        if request.form.get("bike1"):
            bike = 1
        elif request.form.get("bike2"):
            bike = 2
        elif request.form.get("bike3"):
            bike = 3

        # Figure out which day they want to book
        day = request.form.get(f"bike{bike}")
        date = date_from_weekday(day)

        # Ensure the booking date is not in the past
        if not date:
            return apology("You cannot book a day in the past.")


        return render_template("confirmation.html", bike=bike, day=day.lower(), date=date)

    # If the route was requested via GET (not submitted a form)
    else:
        return redirect("/")


@app.route("/report", methods=["GET", "POST"])
@login_required
def report():
    """Report faults"""

    # Ensure route was requested via POST (report submitted)
    if request.method == "POST":

        # Ensure bike was submitted
        if not request.form.get("bike"):
            return apology("You need to enter bike.")

        # Ensure message was submitted
        if not request.form.get("message"):
            return apology("Report not completed.")

        # Insert report into database
        GMT = pytz.timezone('Europe/Oslo')
        timestamp = datetime.now(GMT)
        message = request.form.get("message")
        bike_id = request.form.get("bike")
        db.execute("INSERT INTO reports (userID, bikeID, message, date, time, status) VALUES (?, ?, ?, ?, 0, 0)",
                   session["user_id"], bike_id, message, timestamp)

        return redirect("/")

    # If route was requested via GET
    else:
        return render_template("report.html")


@app.route("/login", methods=["GET", "POST"])    # Inspired by cs50 staff's pset9: finance
def login():
    """ Log user in """

    # Forget any user_id
    session.clear()

    # If user reached route via POST
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Please enter a username.")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Please enter a password.")

        # Get user info from database
        user = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exist and the submitted password hash
        if len(user) != 1 or not check_password_hash(user[0]["hash"], request.form.get("password")):
            return apology("Username or password is wrong.")

        # Remember which user has logged in
        session["user_id"] = user[0]["id"]

        # Redirect logged in user to homepage
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """ Log user out """

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Shows users bookings and user settings"""

    # Query for the users bookings this current week
    GMT = pytz.timezone('Europe/Oslo')
    curr_datetime = datetime.now(GMT)
    curr_week = curr_datetime.strftime("%W")
    booking = db.execute("SELECT bikeID, day, date, time FROM booking WHERE userID = ? AND week = ?",
                          session["user_id"], curr_week)

    # Insert relevant data into a dict-list
    book = [None] * len(booking)
    for i in range(len(booking)):
        book[i] = {
            "bike": int(booking[i]["bikeID"]) + 1,
            "rent": weekday(booking[i]["day"]),
            "book": booking[i]["date"]
        }

    # Query for the users complete booking history
    history = db.execute("SELECT bikeID, day, date, week, time FROM booking WHERE userID = ? ORDER BY bookingID DESC",
                         session["user_id"])

    # Insert relevant data into a dict-list
    hist = [None] * len(history)
    for i in range(len(history)):
        hist[i] = {
            "bike": int(history[i]["bikeID"]) + 1,
            "rent": weekday(history[i]["day"]),
            "week": history[i]["week"],
            "book": history[i]["date"]
        }

    # Query for number of booking per bike
    statistics = db.execute("SELECT COUNT(bookingID) AS num, bikeID FROM booking WHERE userID = ? GROUP BY bikeID ORDER BY num DESC",
                            session["user_id"])

    # Insert into a dict-list
    stats = [None] * len(statistics)
    total = 0
    for i in range(len(statistics)):
        stats[i] = {
            "bike": int(statistics[i]["bikeID"]) + 1,
            "num": int(statistics[i]["num"])
        }
        total += int(statistics[i]["num"])

    # Query for number of bookings per weekday
    weekday_db = db.execute("SELECT COUNT(bookingID) AS num, day FROM booking WHERE userID = ? GROUP BY day ORDER BY num DESC",
                         session["user_id"])

    # Insert into a dict-list
    wd = [None] * len(weekday_db)
    for i in range(len(weekday_db)):
        wd[i] = {
            "weekday": weekday(int(weekday_db[i]["day"])),
            "num": weekday_db[i]["num"]
        }


    return render_template("profile.html", n=len(booking), booking=book, m=len(history), history=hist,
                           o=len(stats), stats=stats, total=total, p=len(weekday_db), weekday=wd)


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Register user """

    # Ensure a form is submitted
    if request.method == "POST":

        # Ensure username is submitted
        if not request.form.get("username"):
            return apology("Please enter a username.", 400)

        # Ensure firstname is submitted
        if not request.form.get("firstname"):
            return apology("Please enter a first name.", 400)

        # Ensure surname is submitted
        if not request.form.get("surname"):
            return apology("Please enter a surname.", 400)

        # Ensure mail is submitted and contains "@"
        if not request.form.get("mail"):
            return apology("Please enter a mail.", 400)
        elif "@bohne.no" not in request.form.get("mail"):
            return apology("Please enter a valid mail.")

        # Ensure password is submitted
        if not request.form.get("password"):
            return apology("Please enter a password.", 400)

        # Ensure password confirmation is submitted
        if not request.form.get("confirmation"):
            return apology("Please confirm password.", 403)

        # Ensure passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match.", 400)

        # Ensure username is not already registered
        check = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(check) > 0:
            return apology("Username already in use.", 400)

        # Ensure the mail is in the mails csv list
        emails = []
        with open("static/mails.csv") as file:
            reader = csv.reader(file)
            for word in reader:
                emails.append(word[0])
        print(emails)
        if request.form.get("mail") not in emails:
            return apology("Invalid @bohne.no mail. Please contact support if you should have access.")

        # Registers the user in the system
        db.execute("INSERT INTO users (username, hash, firstname, surname, mail) VALUES (?, ?, ?, ?, ?)",
            request.form.get("username"), generate_password_hash(request.form.get("password")),
            request.form.get("firstname"), request.form.get("surname"), request.form.get("mail"))

        # Returns the user to the login page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")



