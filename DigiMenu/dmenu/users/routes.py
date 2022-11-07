from flask import Blueprint
from flask import render_template,redirect,url_for,flash,request,abort
from dmenu.users.forms import (RegistrationForm,LoginForm,
                             UpdateAccountForm,
                             RequestResetForm,
                             ResetPasswordForm)

from dmenu.models import User,Menu
from flask_login import login_user,current_user,logout_user,login_required
from dmenu import db,bcrypt
from dmenu.users.utils import send_reset_email


users = Blueprint('users',__name__)

@users.route('/',methods=['GET','POST'])
def home():
    return render_template("index.html",title="Home")

@users.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("users.admin_page"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(rest_name=form.rest_name.data,rest_address=form.rest_address.data,table_count=form.table_count.data,
                    email=form.email.data,password=hashed_password,terms_cond=form.terms_cond.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created, you can now log in!','success')
        return redirect(url_for('users.login'))
    elif form.validate_on_submit() is None:
        flash('invalid credentials, please try again','danger')
    return render_template("reg.html",title="Register",form=form)






@users.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("users.admin_page"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page=request.args.get('next')
            flash('Successfully logged in!','success')
            return redirect(next_page) if next_page else redirect(url_for('users.admin_page'))
        else:
            flash('Login Unsuccessful. Please check your credentials','danger')
    return render_template("log.html",title="Login",form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.home'))


@users.route('/admin',methods=['GET','POST'])
@login_required
def admin_page():
    menus=Menu.query.filter_by(user_id=current_user.id).all()
    return render_template("admin.html",menus=menus)


@users.route('/update',methods=['GET','POST'])
@login_required
def update_admin_page():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.rest_address.data and form.email.data:
            current_user.email=form.email.data
            current_user.rest_address=form.rest_address.data
            db.session.commit()
            flash('Account has been updated','success')
            return redirect(url_for('users.admin_home'))
        else:
            flash('No change has been made.')
            return redirect(url_for('users.admin_home'))
    return render_template("update_admin_page.html",title='Update',form=form)



@users.route('/adminHome',methods=['GET','POST'])
@login_required
def admin_home():
    return render_template("admin_home.html",title="Home")


@users.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("users.admin_page"))
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password','info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title='Reset Password',form=form)



@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("users.admin_page"))
    user=User.verify_reset_token(token)
    if user is None:
        flash('That is an expired token','warning')
        return redirect(url_for('users.reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash('Your password has been updated!','success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',title='Reset Password',form=form)



