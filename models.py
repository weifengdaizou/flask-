from datetime import datetime
from exts import db


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime(100), default=datetime.now)

    questions = db.relationship('QuestionModel', back_populates='author')
    details = db.relationship('DetailModel', back_populates='author_user')


class EmailcaptchaModel(db.Model):
    __tablename__ = 'email_captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    captcha = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


class QuestionModel(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime(100), default=datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # author = db.relationship('UserModel', backref='questions')
    author = db.relationship('UserModel', back_populates='questions')

    details = db.relationship('DetailModel', back_populates='author_question')


class DetailModel(db.Model):
    __tablename__ = 'detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime(100), default=datetime.now)

    author_question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_question = db.relationship('QuestionModel', back_populates='details')

    author_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_user = db.relationship('UserModel', back_populates='details')
