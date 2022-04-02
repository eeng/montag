from flask import Flask
from montag.config import Config
from montag.web import spotify_auth, ytmusic_auth, api


def create_app():
    app = Flask(__name__)
    app.secret_key = Config.flask_secret_key
    app.register_blueprint(spotify_auth.bp)
    app.register_blueprint(ytmusic_auth.bp)
    app.register_blueprint(api.bp)
    return app
