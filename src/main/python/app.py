import argparse

from flask import Flask

import config
import routes

parser = argparse.ArgumentParser()
parser.add_argument("--conf", help="path to conf file")

app = Flask(__name__)


def run():
    args = parser.parse_args()
    conf = config.load(args.conf)

    app.register_blueprint(routes.users, url_prefix='/users')

    app.run(port=conf["server"]["port"], debug=True)

    #todo configure for prod run and not only debug


if __name__ == '__main__':
    run()
