import os

from data import db_session
from main import app

if __name__ == '__main__':
    db_session.global_init()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
