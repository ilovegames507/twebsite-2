from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, url_for, session, jsonify
import os

app = Flask(__name__)


app.secret_key = os.urandom(24)


oauth = OAuth(app)

oauth.register(
    name='google',
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/login')
def login():
   
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    
    token = oauth.google.authorize_access_token()
    user = oauth.google.get('userinfo')

    
    session['user'] = user

    return jsonify(user)

@app.route('/profile')
def profile():
    
    user = session.get('user')
    if user:
        return jsonify(user)
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
