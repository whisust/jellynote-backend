import argparse

from flask import Flask

import config
import routes

parser = argparse.ArgumentParser()
parser.add_argument("--conf", help="path to conf file", default=None)

flask_app = Flask(__name__)


def parse_conf():
    global conf
    args = parser.parse_args()
    conf = config.load(args.conf)


def build_app():
    global flask_app
    flask_app.register_blueprint(routes.users, url_prefix='/users')


def run():
    global flask_app
    parse_conf()
    build_app()
    flask_app.run(port=conf["server"]["port"], debug=True)

    # todo configure for prod run and not only debug


if __name__ == '__main__':
    run()
