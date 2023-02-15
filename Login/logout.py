from flask import session, redirect, url_for, Blueprint

logout = Blueprint('logout',__name__)

@logout.route('/logout')
def logoutRoute():
    session.pop('loginP',None)
    session.pop('loginE',None)
    return redirect(url_for('accueil'))