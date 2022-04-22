import os

from flask import Flask, render_template, send_file, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.exceptions import abort
from werkzeug.utils import redirect, secure_filename

from data import db_session
from data.chats import Chat
from data.comments import Comment
from data.posts import Post
from data.users import User
from forms.loginform import LoginForm
from forms.new_chat_form import NewChatForm
from forms.new_comment_form import NewCommentForm
from forms.newpostform import NewPostForm
from forms.registerform import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'diamond_app_socialnet_blogger'

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init()
db_sess = db_session.create_session()


@login_manager.user_loader
def load_user(user_id):
    user = db_sess.query(User).get(user_id)
    return user


def load_post_content(post_id):
    post = db_sess.query(Post).get(post_id)
    return post


@app.template_filter('hide_email')
def hide_email(email):
    return f"{email[0]}...@{email.split('@')[-1]}"


@app.template_filter('check_like_post')
def check_like_post(liked):
    list_of_liked = liked.split(',')
    if current_user.is_authenticated and str(current_user.id) in list_of_liked:
        return True
    return False


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
    if extra_blog is not None:
        all_blogs = db_sess.query(Post).filter(Post.id != extra_blog.id).all()
    else:
        all_blogs = db_sess.query(Post).all()
    return all_blogs


def get_one_blog(_id):
    return load_post_content(_id)


@app.route('/')
@app.route('/index')
@app.route('/blogs')
def index():
    all_blogs = get_all_blogs()
    return render_template('index.html', blogs=all_blogs, **get_all_info(0), current_user=current_user)


@app.route('/blog/<int:blog_id>', methods=['GET', 'POST'])
def one_blog(blog_id):
    form = NewCommentForm()
    if form.validate_on_submit():
        comment = Comment(text=form.text.data,
                          post_id=blog_id,
                          user_id=current_user.id)
        db_sess.add(comment)
        db_sess.commit()
        return redirect(f'/blog/{blog_id}')
    cur_blog = get_one_blog(blog_id)
    all_blogs = get_all_blogs(extra_blog=cur_blog)
    comments = db_sess.query(Comment).filter(Comment.post_id == blog_id).all()
    return render_template('one_blog.html', blog=cur_blog, recommend=all_blogs, comments=comments, form=form,
                           **get_all_info(0))


@app.route('/chats')
def chats():
    chats = [
        {
            'name': 'mashkaamaria',
            'last_msg': 'любим обожаем скорбим радуемся лучшая !!!!!!!! кто сомневается, '
                        'тот пидр пидорок пидорас и просто гомосексуалист',
            'img': 'https://sun1-21.userapi.com/s/v1/ig2/DPYDRjae_riTgMsLIQIJ2CDjIvebXm8M2N0jSfZJvcGXENxeq0NqhnRd60CSIItgu2c73s6ivRUNrDfkEC6twcdL.jpg?size=200x200&quality=95&crop=64,182,1429,1429&ava=1'
        },
        {
            'name': 'mashkaamaria',
            'last_msg': 'тоже маша, ну типа крутая она дохуя и зе бест оф бест, одного чата ей мало',
            'img': 'https://sun1-21.userapi.com/s/v1/ig2/DPYDRjae_riTgMsLIQIJ2CDjIvebXm8M2N0jSfZJvcGXENxeq0NqhnRd60CSIItgu2c73s6ivRUNrDfkEC6twcdL.jpg?size=200x200&quality=95&crop=64,182,1429,1429&ava=1'
        }
    ]
    return render_template('chats.html', chats=chats, **get_all_info(1))


@app.route('/tasks')
def tasks():
    return render_template('tasks.html', **get_all_info(2))


@app.route('/profile/<int:user_id>')
@login_required
def personal_profile(user_id):
    user = db_sess.query(User).get(user_id)
    all_blogs = db_sess.query(Post).filter(Post.user_id == user_id)
    return render_template('profile.html', **get_all_info(-1), recommend=all_blogs, user=user)
    # all_blogs = get_all_blogs()
    # return render_template('profile.html', **get_all_info(-1), recommend=sample(all_blogs, randint(1, 3)))


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
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   **get_all_info(-1))
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   **get_all_info(-1))
        if db_sess.query(User).filter(User.username == form.username.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь с таким сокращенным именем уже есть",
                                   **get_all_info(-1))
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            username=form.username.data,
            email=form.email.data,
            about=form.about.data
        )
        filename = secure_filename(form.avatar.data.filename)
        form.avatar.data.save(os.path.join('static/img/avatars', filename))
        user.generate_blob(filename)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/users_list')
    return render_template('register.html', title='Регистрация', form=form, **get_all_info(-1))


@app.route("/users_list")
def all_users_list():
    users = db_sess.query(User).filter()
    return render_template('all_users_list.html', title='Список пользователей', all_users=users, **get_all_info(-1))


@login_required
@app.route('/new_post', methods=['GET', 'POST'])
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        post = Post(text=form.text.data,
                    user_id=current_user.id,
                    liked="")
        filename = secure_filename(form.file.data.filename)
        form.file.data.save(os.path.join('static/img/posts', filename))
        post.generate_blob(filename)
        db_sess.add(post)
        db_sess.commit()
        return redirect('/')
    return render_template('new_post.html', form=form)


@login_required
@app.route('/new_chat', methods=['GET', 'POST'])
def new_chat():
    form = NewChatForm()
    if form.validate_on_submit():
        chat = Chat(text=form.text.data,
                    user=form.user.data)
        db_sess.add(chat)
        db_sess.commit()
        return redirect('/chats')
    return render_template('new_chat.html', form=form)


@login_required
@app.route('/api/blogs/change_like/<post_id>')
def set_like_for_post(post_id):
    cur_post = db_sess.query(Post).get(post_id)
    list_of_liked = cur_post.liked.split(',')
    if not current_user.is_authenticated:
        abort(401)
    if not str(current_user.id) in list_of_liked:
        list_of_liked.append(str(current_user.id))
    else:
        del list_of_liked[list_of_liked.index(str(current_user.id))]
    cur_post.liked = ','.join(list_of_liked)
    db_sess.commit()
    return jsonify({
        'result': 'success'
    })


@app.route('/chat/<int:chat_id>')
def one_chat(chat_id):
    return render_template('one_chat.html', **get_all_info(0))


if __name__ == '__main__':
    # db_session.global_init()
    # db_sess = db_session.create_session()
    app.run(port=8000, host='127.0.0.1')
