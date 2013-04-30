import cgi
import os
import random

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
    numWorn = db.IntegerProperty()
    clean = db.BooleanProperty()

class Preferences(db.Model):
    user = db.UserProperty()
    veryheavy_max = db.IntegerProperty()
    veryheavy_min = db.IntegerProperty()
    heavy_max = db.IntegerProperty()
    heavy_min = db.IntegerProperty()
    medium_max = db.IntegerProperty()
    medium_min = db.IntegerProperty()
    light_max = db.IntegerProperty()
    light_min = db.IntegerProperty()
    verylight_max = db.IntegerProperty()
    verylight_min = db.IntegerProperty()
    location = db.StringProperty()

def makePreferences(user):
    prefs = Preferences()
    prefs.user = user
    prefs.veryheavy_max = 20
    prefs.veryheavy_min = -100
    prefs.heavy_max = 40
    prefs.heavy_min = 25
    prefs.medium_max = 60
    prefs.medium_min = 40
    prefs.light_max = 80
    prefs.light_min = 55
    prefs.verylight_max = 120
    prefs.verylight_min = 70
    prefs.location = "Austin"
    return prefs

class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
        w = weatherDataForecast()
        w.getXML()    
        currentTemp = int(round(w.getCurrentTemp()))
        wind = int(round(w.getWindSpeed()))
        prefs = getPrefs(user)
        size = 'light'
        if(currentTemp <= prefs.veryheavy_max):
            size = 'veryheavy'
        elif(currentTemp <= prefs.heavy_max and currentTemp >= prefs.heavy_min):
            size = 'heavy'
        elif(currentTemp <= prefs.medium_max and currentTemp >= prefs.medium_min):
            size = 'medium'
        elif(currentTemp <= prefs.light_max and currentTemp >= prefs.light_min):
            size = 'light'
        elif(currentTemp >= prefs.verylight_min):
            size = 'verylight'
        clothes = getTempClothes(user, size)
        top = getOutfitTop(user, size)
        bottom = getOutfitBottom(user, size)
        clothes = {top, bottom}
        template_values = {
            'url': url,
            'currentTemp': currentTemp,
            'wind': wind,
            'clothes': clothes,
            'top': top,
            'bottom': bottom,
        }
        path = os.path.join(os.path.dirname(__file__), 'Templates/index.html')
        self.response.out.write(template.render(path, template_values))


class ClosetPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
        clothes = getAllClothes(user)
        template_values = {
            'clothes': clothes,
            'url': url,
        }
        path = os.path.join(os.path.dirname(__file__), 'Templates/closet.html')
        self.response.out.write(template.render(path, template_values))

class AddItemPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
        clothes = getAllClothes(user)
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
        num = int(self.request.get('num'))
        for i in range(num):
            clothing = Clothing()
            clothing.user = users.get_current_user()
            clothing.cat = self.request.get('cat')
            clothing.name = self.request.get('name')
            clothing.weight = self.request.get('weight')
            clothing.options = self.request.get_all('options')
            clothing.layers = self.request.get_all('layers')
            clothing.period = int(self.request.get('period'))
            clothing.numWorn = 0;
            clothing.clean = True;
            clothing.put()
        self.redirect('/')

class Empty(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        clothes = getAllClothes(user)
        db.delete(clothes)
        self.redirect('/')

class MarkOutfitWorn(webapp.RequestHandler):
    def post(self):
        keys = self.request.get_all('key')
        for key in keys:
            clothing = db.get(key)
            clothing.numWorn += 1
            if clothing.numWorn == clothing.period:
                clothing.clean = False
            clothing.put()
        self.redirect('/')

class MarkWorn(webapp.RequestHandler):
    def post(self):
        key = self.request.get('key')
        clothing = db.get(key)
        clothing.numWorn += 1
        if clothing.numWorn == clothing.period:
            clothing.clean = False
        clothing.put()
        self.redirect('/')

class Laundry(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        clothes = getAllClothes(user)
        for cloth in clothes:
            cloth.clean = True
            cloth.numWorn = 0
            cloth.put()
        self.redirect('/')

class MarkClean(webapp.RequestHandler):
    def post(self):
        key = self.request.get('key')
        clothing = db.get(key)
        clothing.clean = True
        clothing.numWorn = 0
        clothing.put()
        self.redirect('/')

class MarkDirty(webapp.RequestHandler):
    def post(self):
        key = self.request.get('key')
        clothing = db.get(key)
        clothing.clean = False
        clothing.put()
        self.redirect('/')

class Remove(webapp.RequestHandler):
    def post(self):
        key = self.request.get('key')
        clothing = db.get(key)
        db.delete(clothing)
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

class PrefPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
        clothes = getAllClothes(user)
        prefs = getPrefs(user)
        template_values = {
            'prefs': prefs,
            'clothes': clothes,
            'url': url,
        }
        path = os.path.join(os.path.dirname(__file__), 'Templates/prefs.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        user = users.get_current_user()
        prefs = getPrefs(user)
        prefs.veryheavy_max = long(self.request.get('veryheavy_max'))
        prefs.veryheavy_min = long(self.request.get('veryheavy_min'))
        prefs.heavy_max = long(self.request.get('heavy_max'))
        prefs.heavy_min = long(self.request.get('heavy_max'))
        prefs.medium_max = long(self.request.get('medium_max'))
        prefs.medium_min = long(self.request.get('medium_max'))
        prefs.light_max = long(self.request.get('light_max'))
        prefs.light_min = long(self.request.get('light_max'))
        prefs.verylight_max = long(self.request.get('verylight_max'))
        prefs.verylight_min = long(self.request.get('verylight_max'))
        prefs.location = self.request.get('location')
        prefs.put()
        self.redirect('/')

application = webapp.WSGIApplication(
    [('/', MainPage),
     ('/cloth', Clothes),
     ('/closet', ClosetPage),
     ('/addItem', AddItemPage),
     ('/empty', Empty),
     ('/weather', WeatherPage),
     ('/edit', EditPage),
     ('/laundry', Laundry),
     ('/clean', MarkClean),
     ('/dirty', MarkDirty),
     ('/remove', Remove),
     ('/worn', MarkWorn),
     ('/wornOutfitWorn', MarkOutfitWorn),
     ('/prefs', PrefPage)],
    debug=True)

def getPrefs(user):
    pquery = db.GqlQuery("SELECT * FROM Preferences where user= :1",user)
    prefs = pquery.get()  # gets the first one that matched
    if not prefs:   # no account exists yet for this user
        prefs = makePreferences(user)
    return prefs

def getAllClothes(user):
    clothes = Clothing.all().order('-user')
    clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1",user)
    clothes = clothes_query.fetch(None)
    return clothes

def getCleanClothes(user):
    clothes = Clothing.all().order('-user')
    clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1 AND clean= :2", user, True)
    clothes = clothes_query.fetch(None)
    return clothes

def getDirtyClothes(user):
    clothes = Clothing.all().order('-user')
    clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1 AND clean= :2", user, False)
    clothes = clothes_query.fetch(None)
    return clothes

def getTempClothes(user, size):
    clothes = Clothing.all().order('-user')
    clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1 AND clean= :2 AND weight= :3", user, True, size)
    clothes = clothes_query.fetch(None)
    return clothes

def getOutfitTop(user, size):
    clothes = Clothing.all().order('-user')
    clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1 AND clean= :2 AND weight= :3 AND cat= :4", user, True, size, 'top')
    clothes = clothes_query.fetch(None)
    numItems = len(clothes)
    if(numItems == 1):
        return clothes.pop()
    elif(numItems == 0):
        return None
    index = random.randint(0,numItems-1)
    cloth = clothes.pop(index)
    return cloth

def getOutfitBottom(user, size):
    clothes = Clothing.all().order('-user')
    clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1 AND clean= :2 AND weight= :3 AND cat= :4", user, True, size, 'pants')
    clothes = clothes_query.fetch(None)
    numItems = len(clothes)
    if(numItems == 1):
        return clothes.pop()
    elif(numItems == 0):
        return None
    index = random.randint(0,numItems-1)
    cloth = clothes.pop(index)
    return cloth

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
