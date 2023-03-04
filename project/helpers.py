import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps
from datetime import datetime
from flask_mail import Mail, Message


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def apology(message, code=400):
    """Render message as an apology to user."""

    return render_template("apology.html", message=message)


def date_from_weekday(day):
    """Calculates date based on the weekday given"""

    # Calculate the integer for the weekday
    if "Monday" in day:
        weekday = 0
    if "Tuesday" in day:
        weekday = 1
    if "Wednesday" in day:
        weekday = 2
    if "Thursday" in day:
        weekday = 3
    if "Friday" in day:
        weekday = 4

    # Get the current date and weekday
    curr_date = datetime.now()
    curr_weekday = int(curr_date.weekday())

    # Ensure the day is not in the past
    if (weekday - curr_weekday) < 0:
        return None

    # Get current day, week, month and year
    curr_day = int(curr_date.strftime("%d"))
    curr_week = int(curr_date.strftime("%W"))
    curr_month = int(curr_date.strftime("%m"))
    curr_year = int(curr_date.strftime("%Y"))

    # Create list of all the long months and short months
    lm = [1, 3, 5, 6, 8, 10, 12]
    sm = [4, 7, 9, 11]

    # Calculate booking date
    book_day = curr_day + (weekday - curr_weekday)

    # Make sure the date is correct even if it is at the end of the month
    book_month = curr_month
    if curr_month in lm and book_day > 31:
        book_month += 1
        book_day = 31 - curr_day - (weekday - curr_weekday)
    if curr_month in sm and book_day > 30:
        book_month += 1
        book_day = 30 - curr_day - (weekday - curr_weekday)
    if curr_month == 2 and book_day > 28:
        book_month += 1
        book_day = 28 - curr_day - (weekday - curr_weekday)

    bookdate = {
        "weekday": weekday,
        "day": book_day,
        "week": curr_week,
        "month": book_month,
        "year": curr_year
    }

    return bookdate


def weekday(num):
    """Returns the weekday for the given number"""

    weekdays = ["Sunday", "Monday", "Tuesday", "Wednsday", "Thursday", "Friday", "Saturday"]

    return weekdays[num]



