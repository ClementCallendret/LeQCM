from flask import session, redirect, url_for, Blueprint

logo = Blueprint('logout',__name__)

@logo.route('/logout')
def logout():
    session.pop('loginP',None)
    session.pop('loginE',None)
    return redirect(url_for('accueil'))