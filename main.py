import cgi

import os
from google.appengine.ext.webapp import template

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Greeting(db.Model):
    author = db.UserProperty()
    content = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)

class Clothing(db.Model):
    type = db.StringProperty(multiline=False) #shirt, pants, shoes, socks, hats, etc
    color = db.StringProperty(multiline=False)
    user = db.UserProperty()

class Account(db.Model):
    first = db.StringProperty()
    last = db.StringProperty()
    user = db.UserProperty()


class MainPage(webapp.RequestHandler):
    def get(self):
        greetings_query = Greeting.all().order('-date')
        greetings = greetings_query.fetch(10)

        clothes = Clothing.all().order('-user')

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            loggedin = True

            clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1",user)
            clothes = clothes_query.fetch(10)
            
            pquery = db.GqlQuery("SELECT * FROM Account where user= :1",user)
            account = pquery.get()  # gets the first one that matched
            if not account:   # no account exists yet for this user
                account = Account()
                account.user = user
                account.first = user.nickname()  # or some other default value like ' '
                account.last = user.nickname()
                account.put()

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            loggedin = False

        template_values = {
            'loggedin': loggedin,
            'clothes': clothes,
            'greetings': greetings,
            'url': url,
            'url_linktext': url_linktext,
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))


class Clothes(webapp.RequestHandler):
    def post(self):
        clothing = Clothing()

        clothing.user = users.get_current_user()

        clothing.type = self.request.get('type')
        clothing.color = self.request.get('color')
        clothing.put()
        self.redirect('/')

application = webapp.WSGIApplication(
    [('/', MainPage),
     ('/cloth', Clothes)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
