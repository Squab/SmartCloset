import cgi
import os

from weatherDataForecast import weatherDataForecast

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Clothing(db.Model):
    name = db.StringProperty(multiline=False)
    cat = db.StringProperty(multiline=False)
    weight = db.StringProperty(multiline=False)
    layers = db.StringListProperty()
    options = db.StringListProperty()
    period = db.IntegerProperty()
    user = db.UserProperty()
    numWorn = 0

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
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)

        pquery = db.GqlQuery("SELECT * FROM Account where user= :1",user)
        account = pquery.get()  # gets the first one that matched
        if not account:   # no account exists yet for this user
            account = makeAccount(user)

        w = weatherDataForecast()
        w.getXML()    
        currentTemp = int(round(w.getCurrentTemp()))
        wind = int(round(w.getWindSpeed()))

        template_values = {
            'url': url,
            'currentTemp': currentTemp,
            'wind': wind,
        }

        path = os.path.join(os.path.dirname(__file__), 'Templates/index.html')
        self.response.out.write(template.render(path, template_values))


class ClosetPage(webapp.RequestHandler):
    def get(self):
        clothes = Clothing.all().order('-user')

        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)


        clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1",user)
        clothes = clothes_query.fetch(None)
            
        pquery = db.GqlQuery("SELECT * FROM Account where user= :1",user)
        account = pquery.get()  # gets the first one that matched
        if not account:   # no account exists yet for this user
            account = makeAccount(user)
        closet = ""
        template_values = {
            'clothes': clothes,
            'url': url,
            'closet': closet,
        }
        path = os.path.join(os.path.dirname(__file__), 'Templates/closet.html')
        self.response.out.write(template.render(path, template_values))

class AddItemPage(webapp.RequestHandler):
    def get(self):
        clothes = Clothing.all().order('-user')

        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)


        clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1",user)
        clothes = clothes_query.fetch(None)
            
        pquery = db.GqlQuery("SELECT * FROM Account where user= :1",user)
        account = pquery.get()  # gets the first one that matched
        if not account:   # no account exists yet for this user
            account = makeAccount(user)

        template_values = {
            'clothes': clothes,
            'url': url,
        }
        path = os.path.join(os.path.dirname(__file__), 'Templates/addItem.html')
        self.response.out.write(template.render(path, template_values))


class WeatherPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)    
        pquery = db.GqlQuery("SELECT * FROM Account where user= :1",user)
        account = pquery.get()  # gets the first one that matched
        if not account:   # no account exists yet for this user
            account = makeAccount(user)

        w = weatherDataForecast()
        w.getXML()    
        temp = int(round(w.getCurrentTemp()))
        maxtemp = int(round(w.getMaxTemp()))
        mintemp = int(round(w.getMinTemp()))
        wind = int(round(w.getWindSpeed()))
        humid = int(round(w.getHumidity()))
        rain = w.getHumidity()

        template_values = {
            'temp': temp,
            'maxTemp' : maxtemp,
            'minTemp' : mintemp,
            'wind' : wind,
            'humid' : humid,
            'rain' : rain, 
            'url': url,
        }
        path = os.path.join(os.path.dirname(__file__), 'Templates/weather.html')
        self.response.out.write(template.render(path, template_values))


class Clothes(webapp.RequestHandler):
    def post(self):
        clothing = Clothing()
        clothing.user = users.get_current_user()
        clothing.cat = self.request.get('cat')
        clothing.name = self.request.get('name')
        clothing.weight = self.request.get('weight')
        clothing.options = self.request.get_all('options')
        clothing.layers = self.request.get_all('layers')
        clothing.period = int(self.request.get('period'))
        clothing.put()
        self.redirect('/')


class Empty(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1",user)
        clothes = clothes_query.fetch(None)
        db.delete(clothes)
        self.redirect('/')

class EditPage(webapp.RequestHandler):
    def get(self):
        key = self.request.get('k')
        article = db.Model.get(key)
        cat = article.cat
        name = article.name
        weight = article.weight
        periods = {'1':'one', '2':'two', '3':'three', '4':'four', '10':'ten', '20':'twenty', '30':'thirty', '100':'onehundred', '200':'twohundred', '-1':'negativeone'}
        period = periods[str(article.period)]
        template_values = {
            'name': name,
            cat: True,
            weight: True,
            period: True,
            'edit': 'Edit',
            'value': '/edit',
            'key': key,
        }
        for layer in article.layers:
            template_values[layer] = True
        for option in article.options:
            template_values[option] = True
        path = os.path.join(os.path.dirname(__file__), 'Templates/addItem.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        key = self.request.get('key')
        clothing = db.get(key)
        clothing.user = users.get_current_user()
        clothing.cat = self.request.get('cat')
        clothing.name = self.request.get('name')
        clothing.weight = self.request.get('weight')
        clothing.options = self.request.get_all('options')
        clothing.layers = self.request.get_all('layers')
        clothing.period = int(self.request.get('period'))
        clothing.put()
        self.redirect('/')


application = webapp.WSGIApplication(
    [('/', MainPage),
     ('/cloth', Clothes),
     ('/closet', ClosetPage),
     ('/addItem', AddItemPage),
     ('/empty', Empty),
     ('/weather', WeatherPage),
     ('/edit', EditPage)],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
