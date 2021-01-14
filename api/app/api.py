from flask import Blueprint, request, jsonify, json
from flask_login import current_user
from . import db
from .models import User, Interest
from util import fail, succ
from Levenshtein import distance
from itertools import product
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

@api_bp.route('/user/data', methods=['POST'])
def user_data():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field provided. Please specify an id."
    
    if id == 'CURRENT':
        user = current_user
    else:
        user = User.query.get(id)
        if user is None:
            return "Error: No user found with given id"
    data = user.get_all_data()
    return jsonify(data)

@api_bp.route('/user/addinterest', methods=['POST'])
def add_user_interest():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return json.dumps("Error: No id field provided. Please specify an id.")
    if 'interest' in request.args:
        interest = request.args['interest']
    else:
        return json.dumps("Error: No interest field provided. Please specify an interest to add.")
    if id == 'CURRENT':
        user = current_user
    else:
        user = User.query.get(id)
    return json.dumps(user.add_interest(interest, 0))

@api_bp.route('/user/deleteinterest', methods=['POST'])
def delete_user_interest():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return json.dumps("Error: No id field provided. Please specify an id.")
    
    if 'interest' in request.args:
        interest = request.args['interest']
    else:
        return json.dumps("Error: No interest field provided. Please specify an interest to add.")

    if id == 'CURRENT':
        user = current_user
    else:
        user = User.query.get(id)

    return json.dumps(user.delete_interest(interest, 0))
    
@api_bp.route('/user/match', methods=['POST'])
def match():
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
    
    threshold = 4
    #list of all other users
    all_users = User.query.all()
    all_users = [u for u in all_users if not u == user]
    #store (id, num_matching_interests, matching_interests)
    interest_matches = [(u.id,) + get_interest_matches(user.get_interests(), u.get_interests(), threshold) for u in all_users]
    print(interest_matches)
    sorted_matches = sorted(interest_matches, key= lambda x: x[1], reverse=True)

    data = {'ids':[x[0] for x in sorted_matches], 'n_matches': [x[1] for x in sorted_matches],  'common_interests': [x[2] for x in 
            sorted_matches]}
    print(data)
    return json.dumps(data);

def get_interest_matches(l1, l2, threshold):
    #return the number of matching interests between l1, l2 where a match is where distance(x, y) < threshold
    #and the matches themselves
    combinations = list(product(l1, l2))
    distances = [(distance(x[0], x[1]), x) for x in combinations]
    sorted_matches_with_distances = sorted(distances, key=lambda x:x[0])
    print(sorted_matches_with_distances)
    n_matches = 0
    matches = []
    for x in sorted_matches_with_distances:
        if x[0] < threshold:
            n_matches += 1
            matches.append(x[1][0]) # the first person's interest
        else:
            break

    return n_matches, matches

@api_bp.route('/user/changeprofile', methods=['POST'])
def change_profile():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return json.dumps("Error: No id field provided. Please specify an id.")
    if id == 'CURRENT':
        user = current_user
    try:
        for attribute in request.args:
            if attribute != 'id':
                print(attribute, request.args[attribute])
                user.update(attribute, request.args[attribute])
    except NameError:
        return json.dumps("Error: No id")
    return json.dumps(True)