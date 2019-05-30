import argparse

from flask import Flask

import config
import routes

parser = argparse.ArgumentParser()
parser.add_argument("--conf", help="path to conf file", default=None)


def parse_conf():
    global conf
    args = parser.parse_args()
    conf = config.load(args.conf)


def create_app():
    app = Flask(__name__)
    # TODO
    # app.config.from_pyfile(config_filename)
    app.register_blueprint(routes.users, url_prefix='/users')
    app.register_blueprint(routes.songs, url_prefix='/songs')
    return app


def run():
    parse_conf()
    app = create_app()
    app.run(port=conf["server"]["port"], debug=True)

    # todo configure for prod run and not only debug


if __name__ == '__main__':
    run()
