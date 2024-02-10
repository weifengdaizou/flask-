import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailcaptchaModel
from exts import db


class RegisterForm(wtforms.Form):
    # email = wtforms.StringField(validators=[Email(message='邮箱格式错误')])
    email = wtforms.StringField()
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message='验证码格式错误')])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message='用户名格式错误')])
    password1 = wtforms.StringField(validators=[Length(min=3, max=20, message='密码格式错误')])
    password2 = wtforms.StringField(validators=[EqualTo('password1', message='两次密码不一致')])

    def validate_email(self, filed):
        email = filed.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message='改邮箱已被注册')

    def validate_captcha(self, filed):
        print(filed)
        captcha = filed.data
        email = self.email.data
        captcha_model = EmailcaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message='邮箱或验证码错误')
        else:
            db.session.delete(captcha_model)
            db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField()
    username = wtforms.StringField(validators=[Length(min=3, max=20, message='用户名格式错误')])
    password = wtforms.StringField(validators=[Length(min=3, max=20, message='密码格式错误')])


class Question(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3, max=100, message='标题格式错误')])
    content = wtforms.StringField(validators=[Length(min=3,  message='内容格式错误')])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=3,  message='内容格式错误')])
    question_id = wtforms.StringField(validators=[InputRequired(message='必须要输入id')])
