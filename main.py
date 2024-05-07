from flask import Flask, jsonify, abort, render_template, session, redirect, request, make_response
from data import db_session, projects_api
from data.projects import Projects
from data.users import User
from forms.user import RegisterForm
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from forms.autorization import LoginForm
import datetime
from forms.create_project import CreateForm
app = Flask(__name__)
app.config['SECRET_KEY'] = 'pallery_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
    days=100
)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    projects = db_sess.query(Projects)
    return render_template("index.html", title='Pallery', projects=projects,
                           image='../static/web_pict/background-eff.png')


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 месяца")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


def test_orm_user():
    db_session.global_init("db/projects_h.db")
    from data.users import User
    db_sess = db_session.create_session()
    user = User()
    user.name = '1 Пользователь'
    user.about = 'Информация о пользователе 1'
    user.email = 'email@ya.ru'
    user.hashed_password = 'password'
    db_sess.add(user)
    db_sess.commit()
    for user in db_sess.query(User).all():
        print(user)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contacts')
def contacts():
    return render_template('contacts.html')


@app.route("/create", methods=['GET', 'POST'])
def create():
    form = CreateForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        projects = Projects()
        projects.title = form.title.data
        projects.annotation = form.annotation.data
        projects.image_url = form.image_url.data
        projects.docs_url = form.docs_url.data
        current_user.projects.append(projects)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('create.html', title='Добавление проекта', form=form)


@app.route("/project", methods=['GET', 'POST'])
def about_the_same_project():
    return render_template('project.html')


@app.route('/projectss_delete/<int:id>', methods=['GET', 'POST'])
def projects_delete(id):
    db_sess = db_session.create_session()
    projects = db_sess.query(Projects).filter(Projects.id == id,
                                      Projects.user == current_user
                                      ).first()
    if projects:
        db_sess.delete(projects)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Registration - Pallery',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Registration - Pallery',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            social_network=form.social_network.data,
            scientific_mentor=form.scientific_mentor.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('registration.html', title='Registration - Pallery', form=form)


def main():
    db_session.global_init("db/projects_h.db")
    app.register_blueprint(projects_api.blueprint)
    app.run()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    main()
