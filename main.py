import cgi
import collections
import os

from weatherDataForecast import weatherForecast
from google.appengine.ext.webapp import template

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Clothing(db.Model):
    name = db.StringProperty(multiline=False)
    cat = db.StringProperty(multiline=False)
    weight = db.StringProperty(multiline=False)
    layers = db.StringProperty(multiline=False)
    options = db.StringProperty(multiline=False)
    user = db.UserProperty()

class Account(db.Model):
    first = db.StringProperty()
    last = db.StringProperty()
    user = db.UserProperty()


def makeAccount(user):
    account = Account()
    account.user = user
    account.first = user.nickname()  # or some other default value like ' '
    account.last = user.nickname()
    account.put()
    return account

class MainPage(webapp.RequestHandler):
    def get(self):
        clothes_query = Clothing.all().order('-user')
        clothes = clothes_query.fetch(10)

        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)


        clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1",user)
        clothes = clothes_query.fetch(10)
            
        pquery = db.GqlQuery("SELECT * FROM Account where user= :1",user)
        account = pquery.get()  # gets the first one that matched
        if not account:   # no account exists yet for this user
            account = makeAccount(user)

        #w = weatherForecast()
        #w.getXML()     this is what I tried to do
        #weather = w.getDayTemp()

        template_values = {
            'clothes': clothes,
            'url': url,
            #'weather': weather,
        }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))


class ClosetPage(webapp.RequestHandler):
    def get(self):
        clothes = Clothing.all().order('-user')

        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)


        clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1",user)
        clothes = clothes_query.fetch(10)
            
        pquery = db.GqlQuery("SELECT * FROM Account where user= :1",user)
        account = pquery.get()  # gets the first one that matched
        if not account:   # no account exists yet for this user
            account = makeAccount(user)

        template_values = {
            'clothes': clothes,
            'url': url,
        }
        path = os.path.join(os.path.dirname(__file__), 'closet.html')
        self.response.out.write(template.render(path, template_values))

class AddItemPage(webapp.RequestHandler):
    def get(self):
        clothes = Clothing.all().order('-user')

        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)


        clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1",user)
        clothes = clothes_query.fetch(10)
            
        pquery = db.GqlQuery("SELECT * FROM Account where user= :1",user)
        account = pquery.get()  # gets the first one that matched
        if not account:   # no account exists yet for this user
            account = makeAccount(user)

        template_values = {
            'clothes': clothes,
            'url': url,
        }
        path = os.path.join(os.path.dirname(__file__), 'addItem.html')
        self.response.out.write(template.render(path, template_values))


class Clothes(webapp.RequestHandler):
    def post(self):
        clothing = Clothing()

        clothing.user = users.get_current_user()

        clothing.cat = self.request.get('cat')
        clothing.name = self.request.get('name')
        clothing.weight = self.request.get('weight')
        clothing.options = self.request.get('options')
        clothing.layers = self.request.get('layers')
        clothing.put()
        self.redirect('/')
   

class Empty(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1",user)
        clothes = clothes_query.fetch(1000)
        db.delete(clothes)
        self.redirect('/')

application = webapp.WSGIApplication(
    [('/', MainPage),
     ('/cloth', Clothes),
     ('/closet', ClosetPage),
     ('/addItem', AddItemPage),
     ('/empty', Empty)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
