# Developer Docs

This markdown file runs a developer through the steps to get get them set-up and running Spotilight in a development environment on their own machine. This allows them to test out Spotilight in their own local environement or even contribute to the project.

This documentation goes through the steps of [setting up an environment on a linux machine](#setting-up-the-development-environment) as well as getting a [Spotify Developer app configured](#spotify-for-developers-app-setup). To make the set up process as simple as possible, the default settings for the required tools are specified in this documentation (ex: default ports).

## Requirements

Ideally you will have a machine that can run a Python `pip` virtual environment with Flask v3.0.2 and Node v20.11.0. With Spotilight being a web app, you will need a web browser to view the client end of the application.

To configure a Spotify Developer app in the Spotify for Developers portal you will need a Spotify account. Any type of Spotify account will work for this process, although some features within the actual Spotilight account may be limited without a Spotify Premium account.

## Spotify for Developers App Setup

After following the [requirements](#requirements), login to your Spotify account on the [Spotify for Developers landing page](https://developer.spotify.com/).

Once successfully, logging in to your account, head to your user "Dashboard", which can be selected from the sub-menu after clicking on the user profile dropdown button in the upper right corner of the page.

Next, click the "Create App" button.

Fill in the "App name" field with something along the lines of "Spotilight dev app". Fill in the redirect URI with "http://localhost:5000/auth/callback". Tick the "Web API" multi-select box in the "Which API/SDKs are you planning to use?" section. Also tick the agreements box before the "Save" and "Cancel" buttons at the bottom of the page. Lastly, click the "Save" button.

You are now ready to set-up the development environment. Please note, that you will still need to get the "Client ID" from the app's "Settings" page, so you can leave the Spotify for Developers tab open in a browser window for convenience later.

## Spotilight Development Environment

The Spotilight development environment, is composed of two main directories, `spotilight-api` and `spotilight-vue`, which serve as the application's back-end and front-end, respectively. For the front-end and back-end to properly communicate with each other and the back-end to communicate with the Spotify Web API, we will need to configure two `.env` files within both of the directories.

You will need to open two terminal sessions in order to run the full application, one session with the back-end and the other session for the front-end.

When making changes to either the back-end or front-end, you will be able to make live-changes without the need to restart either environments.

### Setting up the development environment

Begin by, cloning/forking the [Spotilight repository (Bronstrom/Spotilight)](https://github.com/Bronstrom/Spotilight) to your local machine.

Next, include the following the following configurations for the two `.env` files below:

Create the following `.env` file within `spotilight-api`:

```
SECRET_KEY = [SECRET-KEY]

CLIENT_ID = [SPOTILIGHT-CLIENT-ID]
CLIENT_SECRET = [SPOTILIGHT-CLIENT-SECRET]

FRONT_END_URL = "http://localhost:8080"
BACK_END_URL = "http://localhost:5000"
```

In place of `SECRET-KEY` a random generated string or just any string will work here. This is just an extra layer of protection for the back-end's session.

In place of `SPOTILIGHT-SECRET-KEY`, grab the "Client ID" from your Spotify for Developers app Settings and for `SPOTILIGHT-CLIENT-SECRET` grab the "Client secret". Please note, you will have to click "View client secret" under the "Client ID" field in order to reveal the client secret.


Create the following `.env` file within `spotilight-vue`:

```
BACK_END_URL=http://localhost:5000/
```








TODO: DETERMINE IF SECRET_KEY is required for the local session to work properly.








### Flask Back-end

#### Running the back-end the first time

* On a fresh clone/fork of Spotilight, open a new terminal session and navigate to `spotilight-api` within your local clone of clone/fork of Spotilight. Install all of the required dependencies recursively with the following command:

```
pip install -r requirements.txt
```

#### Running the back-end after install

To start the Python virtual environment use the following command:

```
pipenv shell
```

Then, run the following command to start up the back-end:

```
python main.py
```

#### Adding new packages/dependencies to the back-end

If you plan to add a new dependencies to the back-end, use the following command to add them to `requirements.txt`:

```
pip freeze > requirements.txt
```

### Vue Front-end

#### Running the front-end the first time

You will also need to install the necessary packages and dependencies for the front-end. Open a second terminal window and navigate to `spotilight-vue`. Using the Node package manager run the following command:

```
npm install
```

#### Running the front-end after install

After installing the node dependencies, all you need to do is run the following command in `spotilight-vue`: 

```
npm run serve
```

### Opening the application in the browser

Once having the front-end and back-end running in a terminal session, you can navigate to `http://localhost:8080/` in your browser to interact with the full application.
