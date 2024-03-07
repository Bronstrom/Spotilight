from flask import Flask, Blueprint, redirect, request, session, jsonify
from datetime import datetime
import requests

# Define "auth" blueprint
playlists_bp = Blueprint("playlists", __name__)

# Define Spotify base endpoint
API_BASE_ENDPOINT = "https://api.spotify.com/v1/"

# "/playlists" endpoint: Get a user's playlists for an offset and specified count
@playlists_bp.route("<offset>/<count>", methods=["GET"])
def get_user_playlists(offset, count):
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
    response = requests.get(API_BASE_ENDPOINT + "me/playlists?offset=" + offset + "&limit=" + count, headers=headers)
    user_playlists = response.json()
    return jsonify(user_playlists)

# "/playlists" endpoint: Delete a user's playlists
@playlists_bp.route("delete", methods=["DELETE"])
def delete_user_playlists():
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
    playlist_id_list = request.json.get("items")
    for playlist_id in playlist_id_list:
        response = requests.delete(API_BASE_ENDPOINT + "playlists/" + playlist_id + "/followers", headers=headers)
        if errors in response:
            print(jsonify(response))
        # TODO: Catch error here if not 200 - test deleting a playlist that I have deleted on spotify (see if that returns error code)
    
    return { "status": "success" }
