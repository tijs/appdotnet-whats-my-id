import os
import requests
import anyjson
from flask import Flask, session, redirect, url_for, escape, request, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    client_id = os.environ['CLIENT_ID']
    return render_template('hello.html', client_id=client_id)

@app.route('/oauth/complete')
def complete():

    code = request.args.get('code', '')

    if code:
        # Get the access token here
        payload = {
            'client_id': os.environ['CLIENT_ID'], 
            'client_secret': os.environ['CLIENT_SECRET'],
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://rocky-sierra-7348.herokuapp.com/oauth/complete',
            'code': code   
        }
        token = requests.post("https://alpha.app.net/oauth/access_token", data=payload)
        result = anyjson.deserialize(token.json)
        access_token = result['access_token']

        #save token to session
        session['access_token'] = access_token

        # Get the username
        auth_headers = {'Authorization': 'Bearer %s' % access_token }
        user = requests.get("https://alpha-api.app.net/stream/0/users/me")

        return render_template('complete.html')
    else:
        return redirect(url_for('hello'))


@app.route('/follow')
def follow_me():
    if 'access_token' in session:
        access_token = escape(session['access_token'])
        auth_headers = {'Authorization': 'Bearer %s' % access_token }
        user = requests.post("https://alpha-api.app.net/stream/0/users/346/follow")
    else:
        return redirect(url_for('hello'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.secret_key = 'V\x16d|;\x8a\xff]&\x80n\xd7\x98\x01\xd1j\x06,\xa32\x97\xcf_\xfd'
    app.debug = True

    # setup a simple handler for static files
    app.jinja_env.globals['static'] = (
        lambda filename: url_for('static', filename=filename))



    app.run(host='0.0.0.0', port=port)
