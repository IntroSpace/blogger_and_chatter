from random import randint, sample

from flask import Flask, render_template
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from data import db_session
from data.users import User
from forms.loginform import LoginForm
from forms.registerform import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'diamond_app_socialnet_blogger'


def get_services(current_pos):
    services = [
        {
            'name': 'Blog.ger',
            'url': 'blogs'
        },
        {
            'name': 'Chat.ter',
            'url': 'chats'
        },
        {
            'name': 'Cobra Tasks',
            'url': 'tasks'
        }
    ]
    if 0 <= current_pos < len(services):
        services[current_pos]['cur'] = True
    return services


def get_all_info(current_pos):
    params = {
        'services': get_services(current_pos),
        'avatar': 'vk_avatar.jpg'
    }
    return params


def get_all_blogs(extra_blog=None):
    all_blogs = [
        {
            'id': 1,
            'text': 'post 1',
            'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149071.png',
            'visual_content': 'https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__480.jpg',
            'liked': False
        },
        {
            'id': 2,
            'text': 'post 2',
            'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149452.png',
            'liked': True
        },
        {
            'id': 3,
            'text': 'post 3',
            'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149071.png',
            'visual_content': 'https://images.unsplash.com/photo-1453728013993-6d66e9c9123a?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8dmlld3xlbnwwfHwwfHw%3D&w=1000&q=80',
            'liked': False
        },
        {
            'id': 4,
            'text': 'post 4',
            'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149995.png',
            'liked': True
        },
        {
            'id': 5,
            'text': 'post 5',
            'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149071.png',
            'visual_content': 'https://cdn.pixabay.com/photo/2017/02/08/17/24/fantasy-2049567__480.jpg',
            'liked': False
        },
        {
            'id': 6,
            'text': 'post 6',
            'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149995.png',
            'liked': True
        },
        {
            'id': 7,
            'text': 'post 7',
            'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149995.png',
            'liked': True
        }
    ]
    if extra_blog is not None:
        all_blogs = list(filter(lambda x: x.get('id', -1) != extra_blog, all_blogs))
    return all_blogs


def get_one_blog(_id):
    all_blogs = get_all_blogs()
    if 0 < _id <= len(all_blogs):
        return all_blogs[_id - 1]
    abort(404)


@app.route('/')
@app.route('/index')
@app.route('/blogs')
def index():
    all_blogs = get_all_blogs()
    return render_template('index.html', blogs=all_blogs, **get_all_info(0))


@app.route('/blog/<int:blog_id>')
def one_blog(blog_id):
    cur_blog = get_one_blog(blog_id)
    all_blogs = get_all_blogs(extra_blog=blog_id)
    return render_template('one_blog.html', blog=cur_blog, recommend=sample(all_blogs, randint(1, 3)), **get_all_info(0))


@app.route('/chats')
def chats():
    return render_template('chats.html', **get_all_info(1))


@app.route('/tasks')
def tasks():
    return render_template('tasks.html', **get_all_info(2))


@app.route('/profile')
def personal_profile():
    params = {
        'user': {
            'id': 1,
            'name': 'Creator',
            'surname': 'Diamond'
        },
        'quote': {
            'name': 'Creator',
            'surname': 'Diamond',
            'text': 'This app is my :) hehe'
        }
    }
    all_blogs = get_all_blogs()
    return render_template('profile.html', **get_all_info(-1), **params, recommend=sample(all_blogs, randint(1, 3)))


@app.route('/avatar/<name>')
def get_profile_avatar(name):
    from flask import send_file
    return send_file(f'static/img/avatars/{name}', mimetype='image/gif')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(f'/success/{form.data.get("username")}')
    return render_template('login.html', title='Авторизация', form=form, **get_all_info(-1))


@app.route('/success/<username>')
def success_login_page(username):
    user = {
        'username': username
    }
    return render_template('success_login.html', user=user, **get_all_info(-1))


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   **get_all_info(-1))
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   **get_all_info(-1))
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form, **get_all_info(-1))


if __name__ == '__main__':
    db_session.global_init("db/social_net.db")
    app.run(port=8000, host='127.0.0.1')