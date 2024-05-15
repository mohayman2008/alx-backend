#!/usr/bin/env python3
'''Simple Flask app'''
from flask import Flask, g, render_template, request
from flask_babel import Babel  # type: ignore


class Config():
    '''Configuration class for the Flask <app>'''
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

def get_user():
    '''Returns the user dictionary, if "login_as" url parameter was passed in
    with valid "user_id"'''
    user_id = request.args.get("login_as")
    if user_id:
        return users.get(int(user_id), None)
    return None


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    '''This function is used to get the locale from the "request"'''
    locale = request.args.get('locale')
    if locale and locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.before_request
def before_request() -> None:
    '''Handler for tasks to be executed at the beginning of request handling
    '''
    g.user = get_user()


@app.route("/", strict_slashes=False)
def index() -> str:
    '''The root route'''
    if g.user:
        username = g.user.get("name")
    else:
        username = None
    return render_template("5-index.html", username=username)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
