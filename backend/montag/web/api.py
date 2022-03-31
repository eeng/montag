from flask import Blueprint, request
from montag.domain.entities import Provider
from montag.use_cases.fetch_playlists import FetchPlaylists
from montag.web.support import system

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/me")
def me():
    pass


@bp.route("/playlists")
def fetch_playlists():
    provider = Provider(request.args["provider"])
    response = FetchPlaylists(system().repos).execute(provider)
    return {"status": "success", "playlists": len(response.value)}
