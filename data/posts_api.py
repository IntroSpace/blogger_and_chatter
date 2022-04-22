import flask
from flask import jsonify
from flask_login import login_required, current_user
from werkzeug.exceptions import abort

from . import db_session
from .posts import Post

blueprint = flask.Blueprint(
    'posts_api',
    __name__,
    template_folder='templates'
)


@login_required
@blueprint.route('/api/blogs/admin/del/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    if current_user.admin_status > 0:
        db_sess = db_session.create_session()
        blog = db_sess.query(Post).get(blog_id)
        if not blog:
            return jsonify({'error': 'Not found'})
        db_sess.delete(blog)
        db_sess.commit()
        return jsonify({'success': 'OK'})
    return jsonify({'error': 'Not enough permissions'})


@login_required
@blueprint.route('/api/blogs/change_like/<post_id>')
def set_like_for_post(post_id):
    db_sess = db_session.create_session()
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
