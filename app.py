from flask import Flask, render_template, request, redirect, url_for, flash

from helpers import store

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if store.check_user(email, password, is_login=False):
            flash('User already exists. Please login.')
        else:
            store.registration(email, password)
        return redirect(url_for('login'))
    return render_template('registration.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    context = {}
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        context['success'] = store.check_user(email, password)
        context['error'] = not context['success']
    return render_template('login.html', **context)
