from flask import session, redirect, url_for, Blueprint

logo = Blueprint('logout',__name__)

@logo.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))