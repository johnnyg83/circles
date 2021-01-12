from flask.templating import render_template
from . import app, db, login_manager, auth_client
from .models import BannedUser, BlockedUser, Friend, Match, User, get_banned_users
from .models import Interest
from .models import ban_user, unban_user, get_banned_users
from flask_login import current_user, login_user, logout_user, login_required
from flask import request, redirect, json, url_for
import requests
from datetime import datetime as dt


@app.route("/")
def home():
    return render_template('home.html', authenticated=current_user.is_authenticated)

@app.route('/login')
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = auth_client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri= request.base_url + '/callback',
        scope=['openid', 'email', 'profile'],
    )
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get('code')

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']

    # Prepare and send a request to get tokens
    token_url, headers, body = auth_client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(app.config['GOOGLE_CLIENT_ID'], app.config['GOOGLE_CLIENT_SECRET']),
    )

    # Parse the tokens!
    auth_client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email

    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = auth_client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # You want to make sure their email is verified.
    # The user authenticated with Google, authorized your
    # app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    
    existing_user = User.query.get(unique_id)
    if existing_user is None:
        user = User(
            id=unique_id, name=users_name, email=users_email, image=picture, authenticated=True
        )

        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("home"))
    else:
        # Begin user session by logging the user in
        existing_user.authenticated=True
        login_user(existing_user)
        db.session.commit()
        # Send user back to homepage
        return redirect(url_for("home"))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/test') 
def test():
    # db.drop_all()
    # db.create_all()

    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile')
def profile():
    return render_template('profile.html', authenticated=current_user.is_authenticated)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def get_google_provider_cfg():
    return requests.get(app.config['GOOGLE_DISCOVERY_URL']).json()
