from flask import Blueprint, request, render_template, redirect, g, url_for
from .forms import Question, AnswerForm
from models import QuestionModel, UserModel, DetailModel
from exts import db
from decorators import login_required

bp = Blueprint('qa', __name__, url_prefix='/')


@bp.route('/')
def index():
    question = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()

    return render_template('index.html', questions=question)
    # return question


@bp.route('/qa/public', methods=['GET', 'POST'])
@login_required
def public_question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        form = Question(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author_id=g.user.id)
            db.session.add(question)
            db.session.commit()
            return redirect('/')
        else:
            print(form.errors)
            return redirect(url_for('qa.public_question'))


@bp.route('/qa/detail/<qa_id>')
@login_required
def dq_datil(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template('detail.html', question=question)


@bp.route('/answer/public', methods=['POST'])
@login_required
def answer_public():
    form = AnswerForm(request.form)
    print(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        user_id = g.user.id
        answer = DetailModel(content=content, author_question_id=question_id, author_user_id=user_id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('qa.dq_datil', qa_id=question_id))
    else:
        print(form.errors)
        # print(request.form.get('question_id'), 'asss')
        return redirect(url_for('qa.dq_datil', qa_id=request.form.get('question_id')))


@bp.route('/search')
def search():
    # request.args.get() get获取
    # request.form post获取
    # <q> 带参数
    q = request.args.get('q')
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    print(questions)
    return render_template('index.html', questions=questions)






