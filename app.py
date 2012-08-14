import os
import requests
from flask import Flask, session, redirect, url_for, escape, request, render_template, json

app = Flask(__name__)

# set the analytics account ID
app.jinja_env.globals['analytics_account'] = os.environ['ANALYTICS_ACCOUNT']

@app.route('/')
def hello():
    if 'access_token' in session:
        return redirect(url_for('show'))

    client_id = os.environ['CLIENT_ID']
    redirect_url = os.environ['REDIRECT_URL']
    return render_template('hello.html', client_id=client_id, redirect_url=redirect_url)

@app.route('/oauth/complete')
def complete():

    code = request.args.get('code', None)

    if code:
        # Get the access token here
        payload = {
            'client_id': os.environ['CLIENT_ID'], 
            'client_secret': os.environ['CLIENT_SECRET'],
            'grant_type': 'authorization_code',
            'redirect_uri': os.environ['REDIRECT_URL'],
            'code': code   
        }
        r = requests.post("https://alpha.app.net/oauth/access_token", data=payload)
        if r.status_code == requests.codes.ok:
            result = json.loads(r.text)
        else:
            return "sorry but that didn't work"

        access_token = result.get('access_token', None)

        #save token to session
        session['access_token'] = access_token
        return redirect(url_for('show'))
    
    return redirect(url_for('hello'))

@app.route('/oauth/logout')
def logout():
    if 'access_token' in session:
        session.pop('access_token', None)
    
    return redirect(url_for('hello'))


@app.route('/show')
def show():
    if 'access_token' in session:
        access_token = escape(session['access_token'])

        # Get the User details
        headers = {'Authorization': 'Bearer %s' % access_token }
        r = requests.get("https://alpha-api.app.net/stream/0/users/me", headers=headers)
        if r.status_code == requests.codes.ok:
            result = json.loads(r.text)
        else:
            # probably the access_token is no longer valid so kill it and go back home
            session.pop('access_token', None)
            return redirect(url_for('hello'))

        user = result
        return render_template('show.html', user=user)
    else:
        return redirect(url_for('hello'))

@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.secret_key = 'V\x16d|;\x8a\xff]&\x80n\xd7\x98\x01\xd1j\x06,\xa32\x97\xcf_\xfd'
 
    # setup a simple handler for static files
    app.jinja_env.globals['static'] = (
        lambda filename: url_for('static', filename=filename))

    app.run(host='0.0.0.0', port=port)
