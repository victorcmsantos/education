from flask import render_template, flash, redirect, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm, RegistrationFormClass, MyForm
from app.models import Role, User, UserRoles, Course, Classe, Enrolled
from app.mgmt_users import list_rules, get_admin, get_student, get_tutor, get_course_id, get_classe_name, get_course_name
import os

def ls_path(path):
  lst = os.listdir( os.path.join( www_path, path))
  return lst

www_path = '/var/www/html3/app/templates/'
url='http://127.0.0.1:81'

@app.route('/')
@app.route('/index')
def index():
  lst = ls_path('home')
  return render_template('index.html', 
    title='Home', 
    files=lst, 
    Course=Course,
    url=url, 
    get_admin=get_admin, 
    get_tutor=get_tutor, 
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
    if get_admin(current_user.email) == True:
      return redirect('/admin/roles')
    elif get_student(current_user.email) == True:
      return redirect('/student/my_curses')
    elif get_tutor(current_user.email) == True:
      return redirect('/tutor/my_classes')
  return render_template( 'login.html', 
    title='login', 
    files=lst, 
    Course=Course,
    url=url, 
    form=form, 
    get_admin=get_admin, 
    get_tutor=get_tutor, 
    get_student=get_student)

@app.route('/register', methods=['GET', 'POST'])
def register():
  lst = ls_path('home')
  if current_user.is_authenticated:
    return redirect('/index')
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    u = User.query.filter_by(email=form.email.data).first().id
    r = Role.query.filter_by(type='student').first().id
    a = UserRoles(user_id=u, role_id=r)
    db.session.add(a)
    db.session.commit()
    flash('Congratulations, you are now a registered user!')
    return redirect('/login')
  return render_template('register.html', 
    title='Register', 
    files=lst,
    Course=Course,
    User=User, 
    Role=Role, 
    UserRoles=UserRoles,
    form=form,
    get_admin=get_admin, 
    get_tutor=get_tutor, 
    get_student=get_student)

@app.route('/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
  ls_adm = ls_path('admin')
  lst = ls_path('home')
  if not get_admin(current_user.email) == True:
    return render_template('errors_page/unauthorized.html',
      title='unauthorized',
      files=lst,
      Course=Course,
      url=url,
      get_admin=get_admin,
      get_tutor=get_tutor, 
      get_student=get_student)
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    u = User.query.filter_by(email=form.email.data).first().id
    r = Role.query.filter_by(type='tutor').first().id
    a = UserRoles(user_id=u, role_id=r)
    db.session.add(a)
    db.session.commit()
    flash('Congratulations, registered a new user!')
    return redirect('/add_user')
  return render_template('add_user.html', 
    title='add a new user', 
    files=lst,
    fbase=ls_adm, 
    Course=Course,
    User=User, 
    Role=Role, 
    UserRoles=UserRoles,
    form=form,
    get_admin=get_admin, 
    get_tutor=get_tutor, 
    get_student=get_student)

@app.route('/add_class', methods=['GET', 'POST'])
@login_required
def add_class():
  ls_adm = ls_path('tutor')
  lst = ls_path('home')
  if not get_tutor(current_user.email) == True:
    return render_template('errors_page/unauthorized.html',
    title='unauthorized',
    files=lst,
    Course=Course,
    url=url,
    get_admin=get_admin,
    get_tutor=get_tutor, 
    get_student=get_student)
  form = RegistrationFormClass()
  if form.validate_on_submit():
    selectValue = get_course_id(request.form.get('select1'))
    add_class = Classe(name=form.classname.data, course_id=selectValue, tutor_id=current_user.id )
    db.session.add(add_class)
    db.session.commit()
    flash('Congratulations, registered a new Class!')
    return redirect('/add_class')
  return render_template('add_class.html', 
    title='add a new class', 
    files=lst,
    fbase=ls_adm, 
    Course=Course,
    Classe=Classe,
    User=User, 
    Role=Role, 
    UserRoles=UserRoles,
    form=form,
    get_admin=get_admin, 
    get_tutor=get_tutor, 
    get_student=get_student)

@app.route("/classes/<int:class_id>/index")
def class_id(class_id):
  lst = ls_path('home')
  ls_std = ls_path('tutor')
  if not current_user.id == Classe.query.filter_by(id=class_id).first().tutor_id:
    return render_template('errors_page/unauthorized.html',
      title='unauthorized',
      files=lst,
      Course=Course,
      url=url,
      get_admin=get_admin,
      get_tutor=get_tutor, 
      get_student=get_student)
  return render_template('classes/index.html', 
    title='classe %s' % (class_id), 
    files=lst,
    Course=Course,
    User=User,
    Enrolled=Enrolled,
    fbase=ls_std, 
    class_id=class_id,
    url=url, 
    get_classe_name=get_classe_name,
    get_admin=get_admin, 
    get_tutor=get_tutor, 
    get_student=get_student )

@app.route("/classes/<int:class_id>/add_user_class" , methods=['GET', 'POST'])
def add_user_class(class_id):
  lst = ls_path('home')
  ls_std = ls_path('tutor')
  if not current_user.id == Classe.query.filter_by(id=class_id).first().tutor_id:
    return render_template('errors_page/unauthorized.html',
      title='unauthorized',
      files=lst,
      Course=Course,
      url=url,
      get_admin=get_admin,
      get_tutor=get_tutor, 
      get_student=get_student)
  form = MyForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.autocplt.data).first().id
    add_user = Enrolled(user_id=user, classe_id=class_id)
    db.session.add(add_user)
    db.session.commit()
    flash('Congratulations, user Enrolled into a Class!')
    return redirect('/classes/%s/add_user_class' % class_id)
  return render_template('classes/add_user_class.html', 
    title='classe %s' % (class_id), 
    files=lst,
    Course=Course,
    User=User,
    Enrolled=Enrolled,
    fbase=ls_std, 
    class_id=class_id,
    url=url, 
    form=form, 
    get_classe_name=get_classe_name,
    get_admin=get_admin, 
    get_tutor=get_tutor, 
    get_student=get_student )


@app.route('/search/', methods=['GET'])
def search():
	r = request.args['q']
	schools = User.query.with_entities(User.username, User.email).filter(User.email.ilike('%' + r + '%')).all()
	data = [{'username': i[0], 'email': i[1]} for i in schools]
	return jsonify(results=data)


@app.route('/countries')
def countrydic():
	res = User.query.all()
	list_countries = [r.as_dict() for r in res]
	return jsonify(list_countries)

#@app.route('/autocomplete', methods=['GET'])
#def autocomplete():
#    search = request.args.get('q')
#    query = db_session.query(Movie.title).filter(Movie.title.like('%' + str(search) + '%'))
#    results = [mv[0] for mv in query.all()]
#    return jsonify(matching_results=results)

#
#@app.route('/countries')
#def countrydic():
#  tag = request.form["q"]
#  search = "%{}%".format(tag)
#  result = User.query.filter(Post.tags.like(search)).all()
#  return jsonify(matching_results=results)








@app.route("/home/<path:subpath_home>")
def take_to_subpath(subpath_home):
  lst = ls_path('home')
  return render_template('home/%s.html' % (subpath_home), 
  title='%s' % (subpath_home), 
  files=lst, 
  Course=Course,
  url=url, 
  get_admin=get_admin, 
  get_tutor=get_tutor, 
  get_student=get_student )

@app.route("/admin/<path:subpath_adm>", methods=['GET', 'POST'])
@login_required
def adm(subpath_adm):
  ls_adm = ls_path('admin')
  lst = ls_path('home')
  if get_admin(current_user.email) == True:
    return render_template('admin/%s.html' % (subpath_adm), 
      title='%s' % (subpath_adm), 
      fbase=ls_adm, 
      files=lst, 
      Course=Course,
      url=url, 
      list_rules=list_rules, 
      User=User, 
      Role=Role, 
      get_admin=get_admin, 
      get_tutor=get_tutor, 
      get_student=get_student )
  else:
    return render_template('errors_page/unauthorized.html',
    title='unauthorized',
    files=lst,
    Course=Course,
    url=url,
    get_admin=get_admin,
    get_tutor=get_tutor, 
    get_student=get_student)

@app.route("/student/<path:subpath_myc>", methods=['GET', 'POST'])
@login_required
def student(subpath_myc):
  ls_std = ls_path('student')
  lst = ls_path('home')
  return render_template('student/%s.html' % (subpath_myc), 
    title='%s' % (subpath_myc), 
    fbase=ls_std, 
    files=lst, 
    Enrolled=Enrolled,
    Course=Course,
    Classe=Classe,
    url=url, 
    User=User, 
    Role=Role, 
    get_admin=get_admin, 
    get_tutor=get_tutor, 
    get_student=get_student )

@app.route("/tutor/<path:subpath_tutor>", methods=['GET', 'POST'])
@login_required
def tutor(subpath_tutor):
  ls_std = ls_path('tutor')
  lst = ls_path('home')
  return render_template('tutor/%s.html' % (subpath_tutor), 
    title='%s' % (subpath_tutor), 
    fbase=ls_std, 
    files=lst, url=url, 
    Course=Course,
    Classe=Classe,
    User=User, 
    Role=Role, 
    get_course_name=get_course_name,
    get_admin=get_admin, 
    get_tutor=get_tutor, 
    get_student=get_student)

@app.route("/courses/<path:subpath_courses>/presentation/index", methods=['GET', 'POST'])
def courses(subpath_courses):
  ls_std = ls_path('courses')
  lst = ls_path('home')
  return render_template('courses/%s/presentation/index.html' % (subpath_courses), 
    title='%s' % (subpath_courses), 
    fbase=ls_std, 
    files=lst, 
    url=url, 
    Course=Course,
    User=User, 
    Role=Role, 
    get_admin=get_admin, 
    get_tutor=get_tutor, 
    get_student=get_student)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')

