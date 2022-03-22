from random import randint, sample

from flask import Flask, render_template
from werkzeug.exceptions import abort

app = Flask(__name__)


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
    user = {
        'id': 1,
        'name': 'Creator',
        'surname': 'Diamond',
        'description': 'This app is my :) hehe'
    }
    return render_template('profile.html', **get_all_info(-1), user=user)


@app.route('/avatar/<name>')
def get_profile_avatar(name):
    from flask import send_file
    return send_file(f'static/img/avatars/{name}', mimetype='image/gif')


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')