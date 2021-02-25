from flask import Flask

from my_lol_api.lol_api import lol_api

app = Flask(__name__)

app.register_blueprint(lol_api, url_prefix='/')


if __name__ == '__main__':
    app.run(debug=True)
