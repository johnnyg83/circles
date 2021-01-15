from flask import Blueprint, request, jsonify, json, session, redirect
from flask_login import current_user
from . import db
from .models import User, Interest, Match
from .util import fail, succ, remove_duplicates, credentials_to_dict
from Levenshtein import distance
from datetime import datetime as dt
from datetime import timedelta
from itertools import product
from uuid import uuid4
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient
import pickle
from googleapiclient.discovery import build
api_bp = Blueprint('api', __name__)
@api_bp.errorhandler(404)
def not_found(error):
    return fail('Not found.', 404)


@api_bp.errorhandler(401)
def unauthorized(error):
    return fail('You\'re not authorized to perform this action.', 401)


@api_bp.errorhandler(403)
def forbidden(error):
    return fail('You don\'t have permission to do this.', 403)


@api_bp.errorhandler(500)
def internal(error):
    return fail('Internal server error.', 500)

@api_bp.route('/')
def home():
    return "Hello API!"

@api_bp.route('/all/interests', methods=['POST'])
def get_all_interests():
    all_interests = Interest.query.all()
    all_interests = list(set([x.interest for x in all_interests]))
    data = {'all_interests': all_interests}
    return jsonify(data)
    #TODO show online users and total users with interest? 

#TODO: authentication

def get_user_from_request():
    if 'id' in request.args:
            id = request.args['id']
    else:
        return json.dumps("Error: No id field provided. Please specify an id.")
    
    if id == 'CURRENT':
        user = current_user
    else:
        user = User.query.get(id)
        if user is None:
            return json.dumps("Error: No user found with given id")
    return user
@api_bp.route('/user/data', methods=['POST'])
def user_data():
    user = get_user_from_request()
    data = user.get_all_data()
    return jsonify(data)

@api_bp.route('/user/addinterest', methods=['POST'])
def add_user_interest():
    user = get_user_from_request()
    if 'interest' in request.args:
        interest = request.args['interest']
    else:
        return json.dumps("Error: No interest field provided. Please specify an interest to add.")
    return json.dumps(user.add_interest(interest, 0))

@api_bp.route('/user/deleteinterest', methods=['POST'])
def delete_user_interest():
    user = get_user_from_request()
    if 'interest' in request.args:
        interest = request.args['interest']
    else:
        return json.dumps("Error: No interest field provided. Please specify an interest to add.")

    return json.dumps(user.delete_interest(interest, 0))
@api_bp.route('user/addmatch', methods=['POST'])
def add_match():
    user = get_user_from_request()
    if 'match_id' in request.args:
        matched_id = request.args['match_id']
    else:
        return json.dumps("Error: No match field provided. Please specify a match to add.")
    print(matched_id)
    match = Match(user_id=user.id, match_id=matched_id, time = dt.now())

    return json.dumps(user.add_match(match))
@api_bp.route('/user/match', methods=['POST'])
def match():
    user = get_user_from_request()
    
    threshold = 100 #max out for now
    #list of all other users
    all_users = User.query.all()
    all_users = [u for u in all_users if not u == user]
    #store (id, num_matching_interests, matching_interests)
    interest_matches = [(u.id,) + get_interest_matches(user.get_interests(), u.get_interests(), threshold) for u in all_users]
    sorted_matches = sorted(interest_matches, key= lambda x: x[1], reverse=True)
    common_interests = [remove_duplicates(t) for t in [x[2] for x in sorted_matches]]
    uncommon_interests = [list(reversed(remove_duplicates(t))) for t in [x[3] for x in sorted_matches]]

    data = {'ids':[x[0] for x in sorted_matches], 'n_matches': [x[1] for x in sorted_matches], 
     'common_interests': common_interests, 'uncommon_interests': uncommon_interests}
    return json.dumps(data)

def get_interest_matches(l1, l2, threshold):
    #return the number of matching interests between l1, l2 where a match is where distance(x, y) < threshold
    #and the matches themselves
    combinations = list(product(l1, l2))
    distances = [(distance(x[0], x[1]), x) for x in combinations]
    sorted_matches_with_distances = sorted(distances, key=lambda x:x[0])
    n_matches = 0
    matches_user = []
    matches_other = []
    for x in sorted_matches_with_distances:
        if x[0] < threshold:
            n_matches += 1
            matches_user.append(x[1][0]) # the first person's interest
            matches_other.append(x[1][1]) # the second person's interest
        else:
            break

    return n_matches, matches_user, matches_other

@api_bp.route('/user/changeprofile', methods=['POST'])
def change_profile():
    user = get_user_from_request()
    try:
        for attribute in request.args:
            if attribute != 'id':
                print(attribute, request.args[attribute])
                user.update(attribute, request.args[attribute])
    except NameError:
        return json.dumps("Error: No id")
    return json.dumps(True)

@api_bp.route('/createmeeting', methods=['POST'])
def create_meeting():
    user = get_user_from_request()
    if 'other_id' in request.args:
        other_id = request.args['other_id']
    else:
        return json.dumps("Error: No other id provided. Please specify the other person's id.")

    other_user = User.query.get(other_id)
    if other_user is None:
        return json.dumps("Error: Other user not found.")
    
    if user.credentials is None:
        return json.dumps('Error: No credentials.')
    creds = user.credentials
    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **user.credentials)

    calendar = build(
        'calendar', 'v3', credentials=credentials)

    now = dt.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    hour_from_now = (dt.utcnow() + timedelta(hours=1)).isoformat() + 'Z'
    event = {
        'summary': 'Circles Meeting',
        'location': '800 Howard St., San Francisco, CA 94103',
        'description': 'A chance to meet someone new.',
        'start': {
            'dateTime': now,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': hour_from_now,
            'timeZone': 'America/Los_Angeles',
        },
        "conferenceData": {"createRequest": {"requestId": f"{uuid4().hex}",
                                                      "conferenceSolutionKey": {"type": "hangoutsMeet"}}},
        'attendees': [
            {'email': user.email},
            {'email': 'chris.yao@yale.edu'},
        ],
        'reminders': {
            'useDefault': False,
        'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
        ],
        },
    }

    event = calendar.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
    uri = event.get('conferenceData')['entryPoints'][0]['uri']
    print(uri)
    print ('Event created' +  uri)
    user.credentials = credentials_to_dict(credentials)
    return json.dumps(uri)
