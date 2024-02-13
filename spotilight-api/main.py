from flask import Flask
from dotenv import dotenv_values
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Import secrets
secrets=dotenv_values(".env")
secret_key = secrets["SECRET_KEY"]
FRONT_END_URL = secrets["FRONT_END_URL"]

# Establish cross-origin support
CORS(app, supports_credentials=True, resources={r"/*": {"origins": FRONT_END_URL, 
    "allow_headers": "Access-Control-Allow-Origin"}})

# "/" and "/home" endpoint: Landing page
@app.route("/", methods=["GET"])
@app.route("/home", methods=["GET"])
def index():
    return f"Welcome to Spotilight!"

# Register blueprints
from auth import auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")

# Initialize Flask app
if __name__ == "__main__":
    app.secret_key = secret_key
    app.run(debug=True)
