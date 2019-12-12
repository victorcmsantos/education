from flask import render_template, flash, redirect
from flask_login import current_user, login_user, logout_user
from app import app
from app.forms import LoginForm
from app.models import Role, User
from app.mgmt_users import list_rules, get_admin, get_student
import os

### arry pure
#from app.mgmt_users import list_users

def ls_path(path):
  lst = os.listdir( os.path.join( www_path, path))
  return lst

www_path = '/var/www/html3/app/templates/'
url='http://127.0.0.1:81'

@app.route('/')
@app.route('/index')
def index():
  lst = ls_path('home')
  user = {'username': 'Miguel'}
  return render_template('index.html', 
    title='Home', 
    user=user, 
    files=lst, 
    url=url, 
    get_admin=get_admin, 
    get_student=get_student  )

@app.route("/login", methods=['GET', 'POST'])
def login():
  lst = ls_path('home')
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect( "/login" )
    login_user(user, remember=form.remember_me.data)
    return redirect('/index')
  return render_template( 'login.html', 
    title='login', 
    files=lst, 
    url=url, 
    form=form, 
    get_admin=get_admin, 
    get_student=get_student)

@app.route("/home/<path:subpath_home>")
def take_to_subpath(subpath_home):
  lst = ls_path('home')
  return render_template('home/%s.html' % (subpath_home), 
  title='%s' % (subpath_home), 
  files=lst, url=url, 
  get_admin=get_admin, 
  get_student=get_student )

@app.route("/admin/<path:subpath_adm>", methods=['GET', 'POST'])
def adm(subpath_adm):
  ls_adm = ls_path('admin')
  lst = ls_path('home')
  return render_template('admin/%s.html' % (subpath_adm), 
    title='%s' % (subpath_adm), 
    fbase=ls_adm, 
    files=lst, 
    url=url, 
    list_rules=list_rules, 
    User=User, 
    Role=Role, 
    get_admin=get_admin, 
    get_student=get_student )

@app.route("/student/<path:subpath_myc>", methods=['GET', 'POST'])
def student(subpath_myc):
  ls_std = ls_path('student')
  lst = ls_path('home')
  return render_template('student/%s.html' % (subpath_myc), 
    title='%s' % (subpath_myc), fbase=ls_std, 
    files=lst, url=url, 
    list_rules=list_rules, 
    User=User, 
    Role=Role, 
    get_admin=get_admin, 
    get_student=get_student )

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')
