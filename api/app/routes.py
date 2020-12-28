from . import app, db
from.models import User

@app.route('/')
def home():
    User(name='Johnny G', email='john.gunderson@yale.edu').save()
    user = User.objects(name="Johnny G").first()
    print(user.name)
    return 'Hello World!'