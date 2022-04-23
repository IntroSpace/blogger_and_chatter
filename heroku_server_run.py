import os

from data import db_session, posts_api
from main import app

if __name__ == '__main__':
    db_session.global_init()
    port = int(os.environ.get("PORT", 5000))
    app.register_blueprint(posts_api.blueprint)
    app.run(host='0.0.0.0', port=port)
