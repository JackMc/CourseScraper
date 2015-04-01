from flask import Flask, request, session, g, redirect, url_for, \
             abort, flash
import db
import routes

DATABASE = 'test.db'
DEBUG = True
SECRET_KEY = 'key'
USERNAME = 'admin'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)


if __name__ == '__main__':
    app.run()
