from flask import Flask
from dotenv import dotenv_values
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Import secrets
secrets = dotenv_values(".env")
secret_key = secrets["SECRET_KEY"]

client_id = secrets["CLIENT_ID"]
client_secret = secrets["CLIENT_SECRET"]

FRONT_END_URL = secrets["FRONT_END_URL"]

# Establish cross-origin support with pre-flight request
CORS(app, supports_credentials=True, resources={r"/*": {"origins": FRONT_END_URL}})

# "/" and "/home" endpoint: Landing page
@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def index():
    return f"Welcome to Spotilight!"

# Register blueprints
from auth import auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")

from playlist import playlist_bp
app.register_blueprint(playlist_bp, url_prefix="/playlist")

from playlists import playlists_bp
app.register_blueprint(playlists_bp, url_prefix="/playlists")

from search import search_bp
app.register_blueprint(search_bp, url_prefix="/search")

from showcase import showcase_bp
app.register_blueprint(showcase_bp, url_prefix="/showcase")

from user import user_bp
app.register_blueprint(user_bp, url_prefix="/user")

# Initialize Flask app
if __name__ == "__main__":
    app.secret_key = secret_key
    app.config["SESSION_TYPE"] = "filesystem"
    app.run(debug=True)
