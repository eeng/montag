from flask import Blueprint, request
from montag.domain.entities import Provider
from montag.use_cases.fetch_playlists import FetchPlaylists
from montag.web.serializers import list_of_models
from montag.web.spotify_auth import is_spotify_authorized
from montag.web.support import as_json, system

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/me")
def me():
    authorized_providers = []
    if is_spotify_authorized():
        authorized_providers.append(Provider.SPOTIFY.value)
    return {"authorized_providers": authorized_providers}


@bp.route("/playlists")
def fetch_playlists():
    provider = Provider(request.args["provider"])
    response = system().fetch_playlists_use_case.execute(provider)
    return as_json(response, serializer=list_of_models)
