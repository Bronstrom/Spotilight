from flask import Flask, redirect, request
from dotenv import dotenv_values
from datetime import datetime
import random, string, urllib.parse, requests
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Import secrets
secrets=dotenv_values(".env")
secret_key = secrets["SECRET_KEY"]
client_id = secrets["CLIENT_ID"]
client_secret = secrets["CLIENT_SECRET"]
FRONT_END_URL = secrets["FRONT_END_URL"]
BACK_END_URL = secrets["BACK_END_URL"]

# TODO: May not need this line
CORS(app, supports_credentials=True, resources={r"/*": {"origins": FRONT_END_URL, "allow_headers": "Access-Control-Allow-Origin"}})

# Define import Spotify endpoints
AUTH_ENDPOINT = "https://accounts.spotify.com/authorize"
TOKEN_ENDPOINT = "https://accounts.spotify.com/api/token"
API_BASE_ENDPOINT = "https://api.spotify.com/v1/"
ACCOUNT_URL = "https://accounts.spotify.com"
# Define callback URI
REDIRECT_URI = BACK_END_URL + "/callback"
# Generate random string for protection against cross-site request forgery
STATE = "".join(random.choices(string.digits + string.ascii_letters, k=16))
# Define param info
SCOPES = ("user-read-private", "user-read-email")
SPACE_DELIMITER = " "

# Helper function to set token cookies
def set_token_cookies(token, response):
    # Parse token json response and store in cookies
    # TODO: Consider JWT Token in the future
    response.set_cookie("access_token", token["access_token"])
    response.set_cookie("token_type", token["token_type"])
    response.set_cookie("scope", token["scope"])
    # Get timestamp for exactly when token will expire for simple refresh
    token_expiration = datetime.now().timestamp() + token["expires_in"]
    response.set_cookie("expires_at", str(token_expiration))
    response.set_cookie("refresh_token", token["refresh_token"])

# "/" endpoint: Landing page
@app.route("/", methods=["GET"])
def index():
    return f"Welcome to Spotilight!"

# "/login" endpoint: Redirect to Spotify's login page with scopes outlined
@app.route("/login", methods=["GET"])
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
@app.route("/account", methods=["GET"])
def account():
    return {"url": ACCOUNT_URL}
 
# "/callback" endpoint
@app.route("/callback", methods=["GET"])
def callback():
    # User login unsuccessful: State mismatch
    if request.args["state"] != STATE:
        return {"error": "state_mismatch"}
    # User login unsuccessful: Return error back to user
    if "error" in request.args:
        return {"error": request.args["error"]}
    # User login successful: use Spotify code for access token
    if "code" in request.args:
        req_body = {
            "grant_type": "authorization_code",
            "code": request.args["code"],
            "redirect_uri": REDIRECT_URI,
            "client_id": client_id,
            "client_secret": client_secret
        }
        # Aquire token response and update cookies
        response = requests.post(TOKEN_ENDPOINT, data=req_body)
        token = response.json()

        response = redirect(FRONT_END_URL + "/user-profile")
        set_token_cookies(token, response)
        
        return response

# "/refresh-token" endpoint: Creates a new token if current token expired
@app.route("/refresh-token", methods=["GET"])
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

        response = redirect(FRONT_END_URL + "/user-profile")
        set_token_cookies(new_token, response)

        return response

# Initialize Flask app
if __name__ == "__main__":
    app.secret_key = secret_key
    app.run(debug=True)
