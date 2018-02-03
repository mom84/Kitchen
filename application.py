from cs50 import SQL
import urllib.request
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology

from helpers import login_required
from helpers import isUserExsist , getUserHash ,isPasswordFormated
from helpers import addUser


# Configure application
app = Flask(__name__)

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///kitchen.db")



@app.route("/")
def index():
        flash("WELCOME TO Nordbahnhale Kitchen");
        return render_template("index.html")


@app.route("/changePassword", methods=["GET", "POST"])
def changePassword():
    """change user Password"""

    if request.method == "POST":
        if request.form.get("oldpassword") == '':
            return apology("Please enter old Password", 400)

        if request.form.get("password") == '':
            return apology("Please enter the new Password", 400)

        if request.form.get("confirmation") == '':
            return apology("Please enter the Confirmation", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Password and confirmation not match", 400)

        currentUserId = session["user_id"]

        if check_password_hash(getUserHash(currentUserId), generate_password_hash(request.form.get("oldpassword"))):
            return apology("the old Password not correct", 400)

        hashp = generate_password_hash(request.form.get("password"))
        changeUserHash(currentUserId, hashp)

        flash("Password changed!")
        return redirect("/")
    else:
        flash("Please Password must include Numbers & Lowercase & Uppercase charchter...!")
        return render_template("changePassword.html")


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("layout.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        if request.form.get("username") == '':
            return apology("Please enter User Name", 400)

        if request.form.get("password") == '':
            return apology("Please enter User Name", 400)

        if request.form.get("confirmation") == '':
            return apology("Please enter User Name", 400)

        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Password and confirmation not match")

        if isUserExsist(request.form.get("username")) == 1:
            return apology("username already exsist", 400)

        passowrd = request.form.get("password")

        if isPasswordFormated(passowrd) == False:
                return apology("Please Password must include Numbers & Lowercase & Uppercase charchter...!", 400)


        hashPassword = generate_password_hash(request.form.get("password"))

        addUser(request.form.get("username"), hashPassword)
        flash("Registered!")
        return redirect("/")
    else:
        flash("Please Password must include Numbers & Lowercase & Uppercase charchter...!")
        return render_template("register.html")



def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)