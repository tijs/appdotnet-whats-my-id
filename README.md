# What's my ID? for App.net

This is the source code for the What's my ID app, which is live @ 
[http://xyx-pau.herokuapp.com](http://xyx-pau.herokuapp.com).

I made this as an excercise for myself to try out the 
[App.net API](https://github.com/appdotnet/api-spec) but the code is working
so perhaps it will help someone else to find their way around and make something cool.

## Get this app running locally

To test out the app on your dev machine you would need:

 * pip, to install the packages in requirements.txt
 * virtualenv, to make sure you have a neat little package
 * [foreman](https://devcenter.heroku.com/articles/config-vars#local-setup) is
  handy to set the environment variables the app uses
   
The installation steps are:

 1. create a project dir and then a virtual env
 2. clone this repo into your virtualenv
 3. `pip install -r requirements.txt`
 4. create a .env file, see below
 5. start your app with `foreman start`

Your .env file should look something like this:

    CLIENT_ID=[your app.net app client id]
    CLIENT_SECRET=[your app.net app secret]
    REDIRECT_URL=http://127.0.0.1:5000/oauth/complete # default local host:port
    ANALYTICS_ACCOUNT='' # your analytics id if needed; optional
    SECRET_KEY='' # a random secret key for your session cookies
    DEBUG=True # set this to false (or do not set it) for production

## What this is not

This is code slapped together in a few spare hours so please don't interpret 
this as best practice. Actual production code you would take seriously would
need a bit more work.

But.. it works and it's nice and compact so go and have a play with it. Do
let me know when you find nasty bugs or feel i could have done stuff better/cleaner
i'd like to learn as well!

Want keep in touch? [Follow me on App.net](http://alpha.app.net/tijs), i'm _@tijs_ there.

## License

This code is available under the MIT license.