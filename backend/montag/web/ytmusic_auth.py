from typing import Optional
from flask import Blueprint, g, redirect, request, session
from ytmusicapi import YTMusic

AUTH_TOKEN_SESSION_KEY = "ytmusic_auth_token"


bp = Blueprint("ytmusic", __name__, url_prefix="/providers/ytmusic")


@bp.route("/login", methods=["POST"])
def ytmusic_login():
    return_to = request.values["return_to"]
    headers = request.values["headers_raw"].replace("\r\n", "\n")
    auth_token = YTMusic.setup(headers_raw=headers)
    session[AUTH_TOKEN_SESSION_KEY] = auth_token
    return redirect(return_to)


def fetch_auth_token() -> Optional[str]:
    return session.get(AUTH_TOKEN_SESSION_KEY)


@bp.before_app_request
def set_ytmusic_client_opts():
    g.ytmusic_fetch_auth_token = fetch_auth_token


def is_ytmusic_authorized():
    return AUTH_TOKEN_SESSION_KEY in session
