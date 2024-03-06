from flask import Flask, Blueprint, redirect, request, session, jsonify
from dotenv import dotenv_values
from datetime import datetime
import random, string, urllib.parse, requests

# Define "auth" blueprint
auth_bp = Blueprint("auth", __name__)

# Import secrets
secrets = dotenv_values(".env")

client_id = secrets["CLIENT_ID"]
client_secret = secrets["CLIENT_SECRET"]

FRONT_END_URL = secrets["FRONT_END_URL"]
BACK_END_URL = secrets["BACK_END_URL"]

# Define Spotify endpoints
AUTH_ENDPOINT = "https://accounts.spotify.com/authorize"
TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
API_BASE_ENDPOINT = "https://api.spotify.com/v1/"
ACCOUNT_URL = "https://accounts.spotify.com"
LOGOUT_URL = "https://accounts.spotify.com/logout"
# Define callback URI
# NOTE: Callback URIs are defined in the Spotify for Developers app dashboard
REDIRECT_URI = BACK_END_URL + "/auth/callback"

# Generate random string for protection against cross-site request forgery
STATE = "".join(random.choices(string.digits + string.ascii_letters, k=16))
# Define param info
SCOPES = ("user-read-private", "user-read-email", "playlist-read-private", "user-top-read")
SPACE_DELIMITER = " "

# Helper function to set the session token
def set_session_token(token):
    # Parse token json response and store in session
    session["access_token"] = token["access_token"]
    session["token_type"] = token["token_type"]
    session["scope"] = token["scope"]
    # Get timestamp for exactly when token will expire for simple refresh
    session["expires_at"] = datetime.now().timestamp() + token["expires_in"]
    session["refresh_token"] = token["refresh_token"]

# "/login" endpoint: Redirect to Spotify's login page with scopes outlined
@auth_bp.route("/login", methods=["GET"])
def login():
    scope_param = SPACE_DELIMITER.join(SCOPES)
    # Define auth endpoint parameters
    # NOTE: Use show_dialog for testing shown scopes and user information
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "state": STATE,
        "scope": scope_param,
        "show_dialog": True
    }
    auth_complete_endpoint = f"{AUTH_ENDPOINT}?{urllib.parse.urlencode(params)}"
    return {"url": auth_complete_endpoint}

# "/account" endpoint: Configure settings and logout
@auth_bp.route("/account", methods=["GET"])
def account():
    return {"url": ACCOUNT_URL}

# "/logout" endpoint: Completely logs the user out and removes cookies
@auth_bp.route("/logout", methods=["GET"])
def logout():
    return {"url": LOGOUT_URL}

# "/callback" endpoint
@auth_bp.route("/callback", methods=["GET"])
def callback():
    # User login unsuccessful: State mismatch
    if request.args["state"] != STATE:
        return jsonify({"error": "state_mismatch"})
    # User login unsuccessful: Return error back to user
    if "error" in request.args:
        return jsonify({"error": request.args["error"]})
    # User login successful: use Spotify code for access token
    if "code" in request.args:
        req_body = {
            "grant_type": "authorization_code",
            "code": request.args["code"],
            "redirect_uri": REDIRECT_URI,
            "client_id": client_id,
            "client_secret": client_secret
        }
        # Aquire token response and update session
        response = requests.post(TOKEN_ENDPOINT, data=req_body)
        token = response.json()
        set_session_token(token)
        response = redirect(FRONT_END_URL + "/user-profile")
        return response

# "/refresh-token" endpoint: Creates a new token if current token expired
@auth_bp.route("/refresh-token", methods=["GET"])
def refresh_token():
    if "refresh_token" not in session:
        return redirect("/login")
    # Token has expired and token should be refreshed
    if datetime.now().timestamp() > session["expires_at"]:
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {session['access_token']}"
        }
        req_body = {
            "grant_type": "refresh_token",
            "refresh_token": session["refresh_token"],
            "client_id": client_id,
            "client_secret": client_secret
        }
        # Aquire new refresh_token and update session
        response = requests.post(TOKEN_ENDPOINT, headers=headers, data=req_body)
        new_token = response.json()
        set_session_token(new_token)

        return redirect("/user-profile")

# "/user-profile" endpoint: retrive the user's profile
@auth_bp.route("/user-profile", methods=["GET"])
def get_user_profile():
    # User will need to be logged in to aquire profile data - attempt sign in again
    if "access_token" not in session:
        return redirect("/login")
    # Token has expired and token should be refreshed
    if datetime.now().timestamp() > session["expires_at"]:
        return redirect("/refresh-token")
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {session['access_token']}"
    }
    response = requests.get(API_BASE_ENDPOINT + "me", headers=headers)
    profile = response.json()
    return jsonify(profile)
