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
        r = requests.post("https://alpha.app.net/oauth/access_token", data=payload)
        result = anyjson.deserialize(r.text)

        if result.get('error', None):
            return result.get('error')

        access_token = result.get('access_token', None)

        if access_token:
            #save token to session
            session['access_token'] = access_token
            redirect(url_for('show'))
    
    return redirect(url_for('hello'))


@app.route('/show')
def show():
    if 'access_token' in session:
        access_token = escape(session['access_token'])
        
        # Get the User details
        auth_headers = {'Authorization': 'Bearer %s' % access_token }
        r = requests.get("https://alpha-api.app.net/stream/0/users/me")
        result = anyjson.deserialize(r.text)

        if result.get('error', None):
            return result.get('error')

        user = result
        return render_template('show.html', user=user)
    else:
        return redirect(url_for('hello'))


@app.route('/follow')
def follow_me():
    if 'access_token' in session:
        access_token = escape(session['access_token'])
        auth_headers = {'Authorization': 'Bearer %s' % access_token }
        user = requests.post("https://alpha-api.app.net/stream/0/users/346/follow")
        return redirect(url_for('show'))
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
