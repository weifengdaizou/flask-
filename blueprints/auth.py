import random
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from exts import mail
from flask_mail import Message
import string
from models import EmailcaptchaModel, UserModel
from exts import db
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            user = UserModel.query.filter_by(username=username, password=password).first()
            if not user:
                return redirect(url_for('auth.login'))
            else:
                # if check_password_hash(user.password, password):
                # cookie/session session 是经过加密存储在cookie中
                session['user_id'] = user.id

                return redirect('/')
        else:
            print(form.errors)
            # return redirect(url_for('auth.login'))
            return redirect('/')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))



@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        # print(request.form)
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password1.data
            # user = UserModel(email=email, username=username, password=generate_password_hash(password))
            user = UserModel(email=email, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.register'))


@bp.route('/mail/test')
def mail_test():
    message = Message(subject='邮箱测试', recipients=['2779328095@qq.com'], body='这是一条测试邮件')
    mail.send(message)
    return '成功'


@bp.route('/captcha/email')
def get_captcha_email():
    # /capt/cha/email/<email>
    # captcha/email?email=xxx@qq.com
    email = request.args.get('email')
    if not email:
        return jsonify({"code": 300, "message": "email输入失败", 'data': None})

    emali_captcha = EmailcaptchaModel.query.filter_by(email=email).first()
    if emali_captcha:
        print(emali_captcha.captcha)
        return jsonify({"code": 200, "message": "失败", 'data': emali_captcha.captcha})

    souurce = string.digits * 4
    captcha = ''.join(random.sample(souurce, 4))
    # message = Message(subject='知了验证码', recipients=[email], body=f"您的验证码是：{captcha}")
    # mail.send(message)
    print(captcha)
    email_captcha = EmailcaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({"code": 200, "message": "失败", 'data': '发送验证码'})








