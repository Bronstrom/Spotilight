from flask import Flask, Blueprint, redirect, request, jsonify, make_response
from dotenv import dotenv_values
from datetime import datetime
import random, string, urllib.parse, requests

# Define "auth" blueprint
spotlight_bp = Blueprint("spotlight", __name__)

# Import secrets
secrets=dotenv_values(".env")
client_id = secrets["CLIENT_ID"]
client_secret = secrets["CLIENT_SECRET"]
FRONT_END_URL = secrets["FRONT_END_URL"]
BACK_END_URL = secrets["BACK_END_URL"]

# Define import Spotify endpoints
AUTH_ENDPOINT = "https://accounts.spotify.com/authorize"
TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
API_BASE_ENDPOINT = "https://api.spotify.com/v1/"
ACCOUNT_URL = "https://accounts.spotify.com"
LOGOUT_URL = "https://accounts.spotify.com/logout"

# "/toptracks" endpoint: Get a users top tracks they've listened to
@spotlight_bp.route("/toptracks/<count>", methods=["GET"])
def login(count):
    refresh_token = request.cookies.get("refresh_token")
    expires_at = request.cookies.get("expires_at")
    access_token = request.cookies.get("access_token")

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(API_BASE_ENDPOINT + "me/top/tracks?offset=0&limit=" + count, headers=headers)
    toptracks = response.json()
    return jsonify(toptracks)

# "/refresh-token" endpoint: Creates a new token if current token expired
@spotlight_bp.route("/refresh-token", methods=["GET"])
def refresh_token():
    refresh_token = request.cookies.get("refresh_token")
    expires_at = request.cookies.get("expires_at")
    access_token = request.cookies.get("access_token")
    # Refresh token doesn't exist 
    if not "refresh_token":
        return {"error": "no_refresh_token"}
    # Token has expired and token should be refreshed
    if datetime.now().timestamp() > float(expires_at):
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {access_token}"
        }
        req_body = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret
        }
        # Aquire new refresh_token and update cookies
        response = requests.post(TOKEN_ENDPOINT, headers=headers, data=req_body)
        new_token = response.json()

        response = redirect(FRONT_END_URL + "/login")
        set_token_cookies(new_token, response)

        return response
