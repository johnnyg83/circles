from flask.templating import render_template
from . import app, db, login_manager
from .models import BannedUser, BlockedUser, Friend, Match, User, get_banned_users
from .models import Interest
from .models import ban_user, unban_user, get_banned_users
from .util import credentials_to_dict
from flask_login import current_user, login_user, logout_user, login_required
from flask import request, redirect, json, url_for, session
import requests
from datetime import datetime as dt
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

@app.route("/")
def home():
    return render_template('home.html', authenticated=current_user.is_authenticated)

@app.route('/login')
def login():
    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        app.config['GOOGLE_CLIENT_SECRET'],
        scopes=app.config['SCOPES'])

    flow.redirect_uri = url_for('callback', _external=True)

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')
    session['state'] = state

    return redirect(authorization_url)
@app.route("/login/callback")
def callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        app.config['GOOGLE_CLIENT_SECRET'], scopes=app.config['SCOPES'], state=state)
    flow.redirect_uri = url_for('callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    google_session = flow.authorized_session()

    user_data = google_session.get('https://www.googleapis.com/userinfo/v2/me').json()
    unique_id = user_data['id']
    existing_user = User.query.get(unique_id)
    if existing_user is None:
        user = User(
            id=unique_id, name=user_data['name'], email=user_data['email'], image=user_data['picture'], 
            authenticated=True, credentials=credentials_to_dict(credentials)
        )
        db.session.add(user)
        login_user(user)
    else:
        # Begin user session by logging the user in
        existing_user.authenticated=True
        existing_user.credentials = credentials_to_dict(credentials)
        login_user(existing_user)
    db.session.commit()
    return redirect(url_for("home"))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/test') 
def test():
    db.drop_all()
    db.create_all()
    db.session.commit()
    user = User(id = "John Smith", name="John Smith", email = "john.smith@example.com", image="/static/images/johnsmith.jpg")
    user.add_interests_from_list(["meat tenderizing", "colonizing", "being a soldier", "writing", "surfing"])
    db.session.add(user)
    db.session.commit()
    print(user.get_interests())
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/match')
def match():
    return render_template('match.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', authenticated=current_user.is_authenticated)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)