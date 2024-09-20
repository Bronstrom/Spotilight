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

# "/delete-tracks" endpoint: Delete a user's playlist tracks
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
    for index, track_id in enumerate(playlist_track_id_list):
        # appending instances to list
        uri_list.append({ "uri": "spotify:track:" + track_id })
        # Handle Spotify 100 delete limit
        if (len(uri_list) == 100 or (len(uri_list) + 100 * spotify_api_call_iterations == len(playlist_track_id_list))):
            spotify_api_call_iterations = spotify_api_call_iterations + 1
            tracks_object = { "tracks": uri_list }
            print(tracks_object)
            response = requests.delete(API_BASE_ENDPOINT + "playlists/" + playlist_id + "/tracks", headers=headers, json=tracks_object )
            print(response)
            # reset uri list for new 100 queue
            uri_list = []
    return { "status": "success" }

# post endpoint: Create a new user playlist with items
@playlist_bp.route("create/<playlist_name>", methods=["POST"])
def create_user_playlist(playlist_name):
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
    # Store inputs in list
    playlist_track_uri_list = request.json.get("items")
    # Aquire user id
    response_me = requests.get(API_BASE_ENDPOINT + "me", headers=headers)
    if response_me == None:
        return { "status": "Error: failed to get user info"}
    user_id = response_me.json()["id"]
    # Create a new playlist using user_id and playlist_name
    new_playlist_body = {
        "name": playlist_name,
        "public": False
    }
    playlists_url = API_BASE_ENDPOINT + "users/" + user_id + "/playlists"
    response_playlist = requests.post(playlists_url, headers=headers, json=new_playlist_body)
    if response_playlist == None:
        return { "status": "Error: failed to create playlist"}
    playlist_id = response_playlist.json()["id"]
    # Add tracks to new playlist
    i = 0
    # Handle Spotify 100 delete limit
    while (i < len(playlist_track_uri_list) / 100):
        hundredLimitSlice = slice(i * 100, (i + 1) * 100)
        tracks_object = { 
            "uris": playlist_track_uri_list[hundredLimitSlice],
            "position": 0
        }
        playlist_tracks_url = API_BASE_ENDPOINT + "playlists/" + playlist_id + "/tracks"
        response_add_tracks = requests.post(playlist_tracks_url, headers=headers, json=tracks_object)
        # Output final status message
        if response_add_tracks == None:
            return { "status": "Error: failed to add tracks to '" + playlist_name + "'" }
        i += 1
    return { "status": "success" }

# post endpoint: Add to an already created playlist with items
@playlist_bp.route("add-tracks/<playlist_id>", methods=["POST"])
def add_tracks_user_playlist(playlist_id):
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
    # Store inputs in list
    playlist_track_uri_list = request.json.get("items")
    # Add tracks to playlist
    i = 0
    # Handle Spotify 100 delete limit
    while (i < len(playlist_track_uri_list) / 100):
        hundredLimitSlice = slice(i * 100, (i + 1) * 100)
        tracks_object = { 
            "uris": playlist_track_uri_list[hundredLimitSlice],
            "position": 0
        }
        playlist_tracks_url = API_BASE_ENDPOINT + "playlists/" + playlist_id + "/tracks"
        response_add_tracks = requests.post(playlist_tracks_url, headers=headers, json=tracks_object)
        # Output final status message
        if response_add_tracks == None:
            return { "status": "Error: failed to add tracks to '" + playlist_name + "'" }
        i += 1
    return { "status": "success" }
