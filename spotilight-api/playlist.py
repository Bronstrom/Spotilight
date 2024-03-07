from flask import Flask, Blueprint, redirect, request, session, jsonify
from datetime import datetime
import requests

# Define "auth" blueprint
playlist_bp = Blueprint("playlist", __name__)

# Define Spotify base endpoint
API_BASE_ENDPOINT = "https://api.spotify.com/v1/"

# "/playlist" endpoint: Get a user's playlist with an id
@playlist_bp.route("<playlist_id>", methods=["GET"])
def get_user_playlist_details(playlist_id):
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
    response = requests.get(API_BASE_ENDPOINT + "playlists/" + playlist_id, headers=headers)
    user_playlist = response.json()
    return jsonify(user_playlist)

# "/playlist" track endpoint: Get a user's tracks for a playlist with an id, offet, and specified count
@playlist_bp.route("<playlist_id>/<offset>/<count>", methods=["GET"])
def get_user_playlist_tracks(playlist_id, offset, count):
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
    response = requests.get(API_BASE_ENDPOINT + "playlists/" + playlist_id + "/tracks?offset=" + offset + "&limit=" + count, headers=headers)
    user_playlist_tracks = response.json()
    return jsonify(user_playlist_tracks)

# "/delete-tracks" endpoint: Delete a user's playlists
@playlist_bp.route("<playlist_id>/delete-tracks", methods=["DELETE"])
def delete_user_playlist_tracks(playlist_id):
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
    playlist_track_id_list = request.json.get("items")
    uri_list = []
    spotify_api_call_iterations = 0
    for index, playlist_id in enumerate(playlist_track_id_list):
        # appending instances to list
        uri_list.append({ "uri": "spotify:track:" + playlist_id })
         # Handle Spotify 100 delete limit
        if (len(uri_list) == 100 or (len(uri_list) + 100 * spotify_api_call_iterations == len(playlist_track_id_list))):
            spotify_api_call_iterations = spotify_api_call_iterations + 1
            tracks_object = { "tracks": uri_list, "snapshot_id": playlist_id + "_snapshot" }
            print(tracks_object)
            response = requests.delete(API_BASE_ENDPOINT + "playlists/" + playlist_id + "/tracks", headers=headers, data=tracks_object )
            print(response)
            # reset uri list for new 100 queue
            uri_list = []
    return { "status": "success" }
