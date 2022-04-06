import os
from random import randint, sample

from flask import Flask, render_template, session, send_file
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect, secure_filename

from data import db_session
from data.posts import Post
from data.users import User
from forms.loginform import LoginForm
from forms.newpostform import NewPostForm
from forms.registerform import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'diamond_app_socialnet_blogger'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def load_post_content(post_id):
    db_sess = db_session.create_session()
    return db_sess.query(Post).get(post_id)


@app.template_filter('hide_email')
def hide_email(email):
    return f"{email[0]}...@{email.split('@')[-1]}"


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
        'avatar': 'noname_avatar.png'
    }
    return params


def get_all_blogs(extra_blog=None):
    # all_blogs = [
    #     {
    #         'id': 1,
    #         'text': 'post 1',
    #         'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149071.png',
    #         'visual_content': 'https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__480.jpg',
    #         'liked': False
    #     },
    #     {
    #         'id': 2,
    #         'text': 'post 2',
    #         'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149452.png',
    #         'liked': True
    #     },
    #     {
    #         'id': 3,
    #         'text': 'post 3',
    #         'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149071.png',
    #         'visual_content': 'https://images.unsplash.com/photo-1453728013993-6d66e9c9123a?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8dmlld3xlbnwwfHwwfHw%3D&w=1000&q=80',
    #         'liked': False
    #     },
    #     {
    #         'id': 4,
    #         'text': 'post 4',
    #         'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149995.png',
    #         'liked': True
    #     },
    #     {
    #         'id': 5,
    #         'text': 'post 5',
    #         'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149071.png',
    #         'visual_content': 'https://cdn.pixabay.com/photo/2017/02/08/17/24/fantasy-2049567__480.jpg',
    #         'liked': False
    #     },
    #     {
    #         'id': 6,
    #         'text': 'post 6',
    #         'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149995.png',
    #         'liked': True
    #     },
    #     {
    #         'id': 7,
    #         'text': 'post 7',
    #         'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149995.png',
    #         'liked': True
    #     }
    # ]
    db_sess = db_session.create_session()
    all_blogs = db_sess.query(Post).all()
    # if extra_blog is not None:
    #     all_blogs = list(filter(lambda x: x.get('id', -1) != extra_blog, all_blogs))
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
    return render_template('index.html', blogs=all_blogs, **get_all_info(0), current_user=current_user)


@app.route('/blog/<int:blog_id>')
def one_blog(blog_id):
    cur_blog = get_one_blog(blog_id)
    all_blogs = get_all_blogs(extra_blog=blog_id)
    return render_template('one_blog.html', blog=cur_blog, recommend=sample(all_blogs, randint(1, 3)),
                           **get_all_info(0))


@app.route('/chats')
def chats():
    return render_template('chats.html', **get_all_info(1))


@app.route('/tasks')
def tasks():
    return render_template('tasks.html', **get_all_info(2))


@app.route('/profile')
@login_required
def personal_profile():
    # db_sess = db_session.create_session()
    # all_blogs = db_sess.query(Post).filter(Post.user_id == current_user.id)
    # return render_template('profile.html', **get_all_info(-1), recommend=all_blogs)
    all_blogs = get_all_blogs()
    return render_template('profile.html', **get_all_info(-1), recommend=sample(all_blogs, randint(1, 3)))


@app.route('/avatar/<name>')
def get_profile_avatar(name):
    with open(f'static/img/avatars/avatar_of_{name}.png', 'wb') as file:
        file.write(load_user(name).avatar)
    return send_file(f'static/img/avatars/avatar_of_{name}.png', mimetype='image/gif')


@app.route('/post_image/<name>')
def get_post_visual_content(name):
    with open(f'static/img/posts/image_of_{name}.png', 'wb') as file:
        file.write(load_post_content(name).visual_content)
    return send_file(f'static/img/posts/image_of_{name}.png', mimetype='image/gif')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         return redirect(f'/success/{form.data.get("username")}')
#     return render_template('login.html', title='Авторизация', form=form, **get_all_info(-1))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.username.data).first()
        if user and user.check_password(form.password.data):
            print(2, user.post)
            login_user(user, remember=form.remember_me.data)
            return redirect(f'/success')
        user = db_sess.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            print(1, user.post)
            print(login_user(user, remember=form.remember_me.data))
            return redirect(f'/success')
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form,
                               **get_all_info(-1))
    return render_template('login.html', title='Авторизация', form=form, **get_all_info(-1))


@app.route('/success')
def success_login_page():
    return render_template('success_login.html', **get_all_info(-1))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        print('checked')
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   **get_all_info(-1))
        print('checked')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   **get_all_info(-1))
        print('checked')
        if db_sess.query(User).filter(User.username == form.username.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с таким сокращенным именем уже есть",
                                   **get_all_info(-1))
        print('checked')
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            username=form.username.data,
            email=form.email.data,
            about=form.about.data
        )
        print('checked')
        print(form.avatar.data)
        filename = secure_filename(form.avatar.data.filename)
        print('checked')
        form.avatar.data.save(os.path.join('static/img/avatars', filename))
        print('checked')
        user.generate_blob(filename)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/users_list')
    return render_template('register.html', title='Регистрация', form=form, **get_all_info(-1))


@app.route("/users_list")
def all_users_list():
    db_sess = db_session.create_session()
    users = db_sess.query(User).filter()
    return render_template('all_users_list.html', title='Список пользователей', all_users=users, **get_all_info(-1))


@login_required
@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    db_sess = db_session.create_session()
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(text=form.text.data,
                    user_id=current_user.id)
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(os.path.join('static/img/posts', filename))
        post.generate_blob(filename)
        db_sess.add(post)
        db_sess.commit()
        return redirect('/')
    return render_template('new_post.html', form=form)


if __name__ == '__main__':
    db_session.global_init()
    app.run(port=8000, host='127.0.0.1')
