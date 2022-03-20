from flask import Flask, render_template

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


@app.route('/')
@app.route('/index')
@app.route('/blogs')
def index():
    all_blogs = [
        {
            'text': 'post 1',
            'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149071.png',
            'visual_content': 'https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885__480.jpg',
            'liked': False
        },
        {
            'text': 'post 2',
            'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149452.png',
            'liked': True
        },
        {
            'text': 'post 3',
            'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149071.png',
            'visual_content': 'https://images.unsplash.com/photo-1453728013993-6d66e9c9123a?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8dmlld3xlbnwwfHwwfHw%3D&w=1000&q=80',
            'liked': False
        },
        {
            'text': 'post 4',
            'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149995.png',
            'liked': True
        },
        {
            'text': 'post 5',
            'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149071.png',
            'visual_content': 'https://cdn.pixabay.com/photo/2017/02/08/17/24/fantasy-2049567__480.jpg',
            'liked': False
        },
        {
            'text': 'post 6',
            'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149995.png',
            'liked': True
        },
        {
            'text': 'post 7',
            'avatar': 'https://cdn-icons-png.flaticon.com/512/149/149995.png',
            'liked': True
        }
    ]
    return render_template('index.html', blogs=all_blogs, services=get_services(0))


@app.route('/chats')
def chats():
    return render_template('chats.html', services=get_services(1))


@app.route('/tasks')
def tasks():
    return render_template('tasks.html', services=get_services(2))


if __name__ == '__main__':
    app.run(port=8000, host='127.0.0.1')