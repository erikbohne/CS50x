import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from datetime import datetime
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Get the number of individual stocks the user has transacted
    stocks = db.execute("SELECT symbol, SUM(shares) AS shares FROM transactions WHERE id = ? GROUP BY symbol HAVING SUM(shares) > 0",
                        session["user_id"])

    info = [None] * len(stocks)

    for i in range(0, len(stocks), 1):
        data = lookup(stocks[i]["symbol"])
        total = float(data["price"]) * stocks[i]["shares"]

        info[i] = {
            "symbol": data["symbol"],
            "name": data["name"],
            "shares": stocks[i]["shares"],
            "price": usd(data["price"]),
            "total": usd(total),
            "total_int": total
        }

    total = 0
    for i in range(0, len(stocks), 1):
        total += info[i]["total_int"]

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    total += float(cash[0]["cash"])

    return render_template("index.html", stocks=info, lenght=len(stocks), total=usd(total), cash=usd(cash[0]["cash"]))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # Ensure the route is requested via POST (submitted a form)
    if request.method == "POST":

        # Ensure a symbol was submitted and it exists
        if not request.form.get("symbol") or lookup(request.form.get("symbol")) == None:
            return apology("You need to fill in a valid symbol...")

        # Handle fractional, negative and non-numeric shares
        try:
            int(request.form.get("shares"))
        except ValueError:
            return apology("Invalid number of shares", 400)
        if int(request.form.get("shares")) < 1:
            return apology("Invalid number of shares", 400)

        # Check if there is enough money to complete the transaction
        balance = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        info = lookup(request.form.get("symbol"))
        total = float(request.form.get("shares")) * info["price"]

        if balance[0]["cash"] < total:
            return apology("Not enough money for the transaction :/")

        # Complete the transaction (1/2): Record the transaction
        db.execute("INSERT INTO transactions (id, symbol, price, shares, date) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], info["symbol"], info["price"], request.form.get("shares"), datetime.now())

        # Complete the transaction (2/2): Update user balance
        db.execute("UPDATE users SET cash = ? WHERE id = ?", balance[0]["cash"] - total, session["user_id"])

        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/changepass", methods=["GET", "POST"])
@login_required
def changepass():
    """Change the user's password"""

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


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Aquire all user's transactions
    transactions = db.execute("SELECT * FROM transactions WHERE id = ?", session["user_id"])

    # Render history page with the information
    return render_template("history.html", transaction=transactions, n=len(transactions))


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # Ensure a form is submitted
    if request.method == "POST":

        # Ensure a stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("No stock symbol was submitted...", 400)

        # Ensure the symbol submitted is valid
        if not lookup(request.form.get("symbol")):
            return apology("No stock with that symbol :/", 400)

        # Workaround check50... (formerly had the "$" in the html file)
        stock = lookup(request.form.get("symbol"))
        price = usd(stock["price"])

        # Return answer from the lookup
        return render_template("quote_return.html", stock=lookup(request.form.get("symbol")), price=price)

    # Handle "GET" request
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Ensure a form is submitted
    if request.method == "POST":

        # Ensure username is submitted
        if not request.form.get("username"):
            return apology("You have to fill out username, you know...", 400)

        # Ensure password is submitted
        if not request.form.get("password"):
            return apology("You have to fill out password, you know...", 400)

        # Ensure password confirmation is submitted
        if not request.form.get("confirmation"):
            return apology("You do have to fill out passowrd confirmation, you know...", 400)

        # Ensure passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords not matching :/", 400)

        # Ensure username is not already registered
        check = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        if len(check) > 0:
            return apology("Username already taken :/", 400)

        # Registers the user in the system
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        # Returns the user to the login page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # Ensure user is requesting via POST (submitting a form)
    if request.method == "POST":

        # Ensure a symbol was submitted
        if not request.form.get("symbol"):
            return apology("Missing stock symbol :/")

        # Ensure the user has enough shares to sell
        current = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE id = ? AND symbol = ?",
                             session["user_id"], request.form.get("symbol"))
        shares = int(current[0]["shares"])
        if shares < int(request.form.get("shares")):
            return apology("You don't have enough shares :/")

        # Sell the shares at current price
        stock = lookup(request.form.get("symbol"))
        shares = int("-" + request.form.get("shares"))
        db.execute("INSERT INTO transactions (id, symbol, price, shares, date) VALUES (?, ?, ?, ?, ?)",
                   session["user_id"], stock["symbol"], stock["price"], shares, datetime.now())

        # Calculate new cash
        old_cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        new_cash = float(request.form.get("shares")) * float(stock["price"]) + float(old_cash[0]["cash"])

        # Update the users cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, session["user_id"])

        return redirect("/")

    else:
        stocks = db.execute(
            "SELECT symbol, SUM(shares) AS shares FROM transactions WHERE id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
        return render_template("sell.html", stock=stocks, n=len(stocks))


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

