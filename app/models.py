from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  def __repr__(self):
    return '<User {}>'.format(self.username)  
  def set_password(self, password):
      self.password_hash = generate_password_hash(password)
  def check_password(self, password):
      return check_password_hash(self.password_hash, password)

class Role(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(140), index=True, unique=True)
  type = db.Column(db.String(140))
  def __repr__(self):
    return '<Role {}>'.format(self.name)

class UserRoles(db.Model):
  id = db.Column(db.Integer, primary_key=True)
#  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#  role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
  user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
  role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
  def __repr__(self):
    return '<UserRoles {}>'.format(self.user_id)


