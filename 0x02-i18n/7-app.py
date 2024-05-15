#!/usr/bin/env python3
'''Simple Flask app'''
from typing import Dict, Optional

from flask import Flask, g, render_template, request
from flask_babel import Babel  # type: ignore
import pytz
from pytz.exceptions import UnknownTimeZoneError  # type: ignore


class Config():
    '''Configuration class for the Flask <app>'''
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


users: Dict[int, Dict] = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Optional[Dict]:
    '''Returns the user dictionary, if "login_as" url parameter was passed in
    with valid "user_id"'''
    user_id = request.args.get("login_as")
    if user_id:
        return users.get(int(user_id), None)
    return None


def validate_tz(tz: str) -> bool:
    '''Validate timezone string "tz" using pytz.timezone'''
    try:
        pytz.timezone(tz)
        return True
    except UnknownTimeZoneError:
        return False


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale() -> Optional[str]:
    '''This function is used to get the approperiate locale'''
    locale = request.args.get('locale')
    if locale and locale in app.config["LANGUAGES"]:
        return locale

    user = g.user
    if user and user.get("locale") in app.config["LANGUAGES"]:
        return user.get("locale")

    return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone() -> str:
    '''This function is used to get the approperiate timezone'''
    timezone = request.args.get('timezone')
    if timezone and validate_tz(timezone):
        return timezone

    user = g.user
    if user and validate_tz(user.get("timezone")):
        return user.get("timezone", app.config["BABEL_DEFAULT_TIMEZONE"])

    return app.config["BABEL_DEFAULT_TIMEZONE"]


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
    return render_template("6-index.html", username=username)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
