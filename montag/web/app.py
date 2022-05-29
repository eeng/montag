from flask import Flask, session
from montag.config import Config
from montag.web import api, spotify_auth, ytmusic_auth


def create_app():
    app = Flask(__name__)
    app.secret_key = Config.flask_secret_key
    app.register_blueprint(spotify_auth.bp)
    app.register_blueprint(ytmusic_auth.bp)
    app.register_blueprint(api.bp)

    # Not very secure, but works for now without a full-fledged authentication solution
    @app.before_request
    def make_session_permanent():
        session.permanent = True

    return app
