from flask import Flask

from config import conf
import routes


def create_app():
    app = Flask(__name__)
    print("Starting app with conf")
    print(app.config)
    print(conf)
    app.register_blueprint(routes.users, url_prefix='/users')
    app.register_blueprint(routes.songs, url_prefix='/songs')
    app.register_blueprint(routes.notifications, url_prefix='/notifications')
    return app


app = create_app()

if __name__ == '__main__':
    app.run(port=conf.server.port, host=conf.server.host, debug=conf.env.lower() == 'dev')
