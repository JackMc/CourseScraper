from flask import render_template

@main.app.route('/')
def index():
    return render_template('index.html')

@main.app.route('/nav/home')
def home():
    return render_template('home.html')

@main.app.route('/nav/contact')
def contact():
    return render_template('contact.html')

@main.app.route('/nav/about')
def about():
    return render_template('about.html')
