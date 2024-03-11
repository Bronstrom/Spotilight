from flask import Flask, Blueprint, redirect, session, jsonify
from datetime import datetime
import requests

# Define "auth" blueprint
spotlight_bp = Blueprint("spotlight", __name__)

# Define Spotify base endpoint
API_BASE_ENDPOINT = "https://api.spotify.com/v1/"

# "/top-tracks" endpoint: Get a users top tracks they've listened to for a time range and specified count
@spotlight_bp.route("/top-tracks/<time_range>/<count>", methods=["GET"])
def get_top_tracks(time_range, count):
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
    response = requests.get(API_BASE_ENDPOINT + "me/top/tracks?time_range=" + time_range + "&offset=0&limit=" + count, headers=headers)
    top_tracks = response.json()
    return jsonify(top_tracks)

# "/top-artists" endpoint: Get a users top artists they've listened to for a time range, offset, and specified count
@spotlight_bp.route("/top-artists/<time_range>/<offset>/<count>", methods=["GET"])
def get_top_artists(time_range, offset, count):
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
    response = requests.get(API_BASE_ENDPOINT + "me/top/artists?time_range=" + time_range + "&offset=" + offset + "&limit=" + count, headers=headers)
    top_artists = response.json()
    return jsonify(top_artists)

# artist top tracks endpoint: Get an artist's top tracks
@spotlight_bp.route("/<artist_id>/top-tracks", methods=["GET"])
def get_artist_top_tracks(artist_id):
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
    response = requests.get(API_BASE_ENDPOINT + "artists/" + artist_id + "/top-tracks", headers=headers)
    artist_top_tracks = response.json()
    return jsonify(artist_top_tracks)
