import argparse

from flask import Flask

import config
import users

parser = argparse.ArgumentParser()
parser.add_argument("--conf", help="path to conf file")

app = Flask(__name__)

if __name__ == '__main__':
    args = parser.parse_args()

    conf = config.load(args.conf)
    app.register_blueprint(users.users_bp, url_prefix='/users')
    app.run(port=conf["server"]["port"], debug=True)
