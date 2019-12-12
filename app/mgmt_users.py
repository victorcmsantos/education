from app import db
from app.models import User, Role , Assignment

#def ls_users():
#  #ls = 'ola'
#  ls = User.query.all()
#  #print ls
#  return ls
#
#def list_users():
#  #sql_users = User.query.all()
#  users = []
#  for u in User.query.all():
#    users.append({u.username: u.email})
#  return users
#
#def list_roles():
#  #sql_users = User.query.all()
#  roles = []
#  for r in Role.query.all():
#    roles.append({r.name: r.type})
#  return roles

def list_rules(user):
  roles_arry = get_assig(user)
  new_array = []
  for i in roles_arry:
    new_array.append(str(i))
  new_array = ','.join(new_array)
  return new_array

def get_assig(user):
  assig = []
  u = User.query.filter_by(email=user).first()
  from_f = Assignment.query.filter_by(user_id=u.id).all()
  for i in from_f:
    assig.append(Role.query.filter_by(id=i.role_id).first().type)
  return assig

def get_admin(user):
  try:
    role_arry = get_assig(user)
    if 'admin' in role_arry:
      is_admin = True
      return is_admin
  except:
    is_admin = False
    return is_admin

def get_student(user):
  try:
    role_arry = get_assig(user)
    if 'student' in role_arry:
      is_admin = True
      return is_admin
  except:
    is_admin = False
    return is_admin
