from flask import Flask

from db import init_db, db

app = Flask(__name__)


# init_db(app)
# app.app_context().push()
# db.create_all()

def main():
    init_db(app)
    app.app_context().push()
    db.create_all()
    app.run()
#
# @app.route('/login')
# def login():
#     return render_template("login.html", title="Авторизация")


if __name__ == '__main__':
    main()
