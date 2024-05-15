#!/usr/bin/env python3
'''Simple Flask app'''
from typing import Optional

from flask import Flask, render_template, request
from flask_babel import Babel  # type: ignore


class Config():
    '''Configuration class for the Flask <app>'''
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> Optional[str]:
    '''This function is used to get the approperiate locale'''
    locale = request.args.get('locale')
    if locale and locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route("/", strict_slashes=False)
def index() -> str:
    '''The root route'''
    return render_template("4-index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
