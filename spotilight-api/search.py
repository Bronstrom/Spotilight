from flask import Flask, Blueprint, redirect, request, session, jsonify
from datetime import datetime
import requests

# Define "auth" blueprint
search_bp = Blueprint("search", __name__)

# Define Spotify base endpoint
API_BASE_ENDPOINT = "https://api.spotify.com/v1/"

# "/search/artist" endpoint: Seach Spotify artist's from search query string
@search_bp.route("artist/<query>/<count>", methods=["GET"])
def search_artist(query, count):
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
    response = requests.get(API_BASE_ENDPOINT + "search?q=" + query + "&type=artist&limit=" + count, headers=headers)
    user_playlists = response.json()
    return jsonify(user_playlists)

# "/search/track" endpoint: Seach Spotify track's from search query string
@search_bp.route("track/<query>/<count>", methods=["GET"])
def search_track(query, count):
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
    response = requests.get(API_BASE_ENDPOINT + "search?q=" + query + "&type=track&limit=" + count, headers=headers)
    user_playlists = response.json()
    return jsonify(user_playlists)
