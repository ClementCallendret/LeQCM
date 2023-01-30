from flask import Blueprint, request,session, render_template

connect = Blueprint('connected',__name__)

@connect.route('/connected/')
def connected():
    return render_template("connected.html")

