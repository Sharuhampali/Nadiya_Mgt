from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        rid = request.form.get('rid')

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                # Assign role based on rid
                if rid == '100':
                    user.rid = 'admin'
                elif '@nadiya.in' in rid:
                    user.rid = 'team'
                else:
                    user.rid = 'client'

                # Commit the role change to the database
                db.session.commit()

                # Login user
                login_user(user, remember=True)
                flash('Logged in successfully!', category='success')
                return redirect(url_for('views.main'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Project does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        rfid = request.form.get('rid')
        project_type = request.form.get('project_type')  # Retrieve the new field

        if rfid is None:
            rfid = ''  # Set rfid to an empty string if it's None to avoid TypeError

        if rfid == '100':
            rid = 'admin'
        elif '@nadiya.in' in rfid:
            rid = 'team'
        else:
            rid = 'client'

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Project already exists.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 1:
            flash('Password must be at least 7 characters.', category='error')
        elif rid != 'team':
            return render_template('naah.html')
        else:
            # Create a new user
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='scrypt'), rid=rid, p_type=project_type)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.main'))

    # Render the sign-up form
    return render_template("sign_up.html", user=current_user)