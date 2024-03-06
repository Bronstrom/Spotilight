from flask import Flask, Blueprint, redirect, session, jsonify
from datetime import datetime
import requests

# Define "auth" blueprint
user_bp = Blueprint("user", __name__)

# Define Spotify base endpoint
API_BASE_ENDPOINT = "https://api.spotify.com/v1/"

# "/display-name" endpoint: Get a user's display name
@user_bp.route("/display-name", methods=["GET"])
def get_display_name():
    # User will need to be logged in to aquire user data - attempt sign in again when no token
    if "access_token" not in session:
        return redirect("/auth/login")
    # Token has expired and token should be refreshed
    if datetime.now().timestamp() > session["expires_at"]:
        return redirect("/auth/refresh-token")
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {session['access_token']}"
    }
    response = requests.get(API_BASE_ENDPOINT + "me", headers=headers)
    display_name = response.json()["display_name"]
    return display_name

# "/display-name" endpoint: Get a user's profile photo
@user_bp.route("/profile-photo", methods=["GET"])
def get_profile_photo():
    # User will need to be logged in to aquire user data - attempt sign in again when no token
    if "access_token" not in session:
        return redirect("/auth/login")
    # Token has expired and token should be refreshed
    if datetime.now().timestamp() > session["expires_at"]:
        return redirect("/auth/refresh-token")
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {session['access_token']}"
    }
    response = requests.get(API_BASE_ENDPOINT + "me", headers=headers)
    profile_photo = response.json()["images"][0]["url"]
    return profile_photo
