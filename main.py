import flask
from flask import render_template, Flask, request, make_response
from server import *

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    index_page = make_response(render_template('index.html'))

    if "uname" in request.cookies:
        return flask.redirect("/home")
    else:
        return index_page


@app.route('/signup', methods=["GET", "POST"])
def sign_up():
    signed_in = False
    signup_page = make_response(render_template("signup.html"))
    if request.method == "POST":
        data = request.form
        if CheckIfUserExists(data["Uname"]):
            return "username exists try again"
        else:
            signup(data["Uname"], data["Name"], data["Password"])
            signup_page.set_cookie("uname", data["Uname"])
    return signup_page


@app.route("/login", methods=["GET", "POST"])
def log_in():
    login_page = make_response(render_template("login.html"))
    if request.method == "POST":
        data = request.form
        if login(data["Uname"], data["Password"]):
            login_page.set_cookie("uname", data["Uname"])
        else: return "Incorrect password try again"
    return login_page


@app.route('/home', methods=["GET", "POST"])
def home():
    name = request.cookies.get("uname")
    data = get_all_data('posts')
    return render_template("home.html", data=data)


@app.route("/create-post", methods = ["GET","POST"])
def create_post():
    ctp_page = make_response(render_template("ctp.html"))
    if request.method =="POST":
        data = request.form
        make_post(data)
    return ctp_page
