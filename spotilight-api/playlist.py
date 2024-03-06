from flask import Flask, Blueprint, redirect, session, jsonify
from datetime import datetime
import requests

# Define "auth" blueprint
playlist_bp = Blueprint("playlist", __name__)

# Define Spotify base endpoint
API_BASE_ENDPOINT = "https://api.spotify.com/v1/"

# "/playlist" endpoint: Get a user's playlist with an id
@playlist_bp.route("<playlistId>", methods=["GET"])
def get_user_playlist_details(playlistId):
    # User will need to be logged in to aquire profile data - attempt sign in again
    if "access_token" not in session:
        return redirect("/auth/login")
    # Token has expired and token should be refreshed
    if datetime.now().timestamp() > session["expires_at"]:
        return redirect("/auth/refresh-token")
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {session['access_token']}"
    }
    response = requests.get(API_BASE_ENDPOINT + "playlists/" + playlistId, headers=headers)
    user_playlist = response.json()
    return jsonify(user_playlist)

# "/playlist" track endpoint: Get a user's tracks for a playlist with an id, offet, and specified count
@playlist_bp.route("<playlistId>/<offset>/<count>", methods=["GET"])
def get_user_playlist_tracks(playlistId, offset, count):
    # User will need to be logged in to aquire profile data - attempt sign in again
    if "access_token" not in session:
        return redirect("/auth/login")
    # Token has expired and token should be refreshed
    if datetime.now().timestamp() > session["expires_at"]:
        return redirect("/auth/refresh-token")
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {session['access_token']}"
    }
    response = requests.get(API_BASE_ENDPOINT + "playlists/" + playlistId + "/tracks?offset=" + offset + "&limit=" + count, headers=headers)
    user_playlist_tracks = response.json()
    return jsonify(user_playlist_tracks)