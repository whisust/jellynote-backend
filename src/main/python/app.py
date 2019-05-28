from flask import Flask
import argparse
import config

parser = argparse.ArgumentParser()
parser.add_argument("--conf", help="path to conf file")

app = Flask(__name__)


if __name__ == '__main__':
    args = parser.parse_args()

    conf = config.load(args.conf)

    app.run(port=conf["server"]["port"], debug=True)