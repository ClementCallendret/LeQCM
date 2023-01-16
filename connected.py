from flask import Flask, redirect, url_for, request

@app.request('/connected/<login>')
def connected(login):
    return 'Bienvenue' + login
