import os

import StandardMethods as sm
import Models as m

import webapp2
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import db


class ClosetPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
        clothes = sm.getAllClothes(user)
        template_values = {
            'clothes': clothes,
            'url': url,
        }
        path = os.path.abspath('templates/closet.html')
        self.response.out.write(template.render(path, template_values))

class AddItemPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
        clothes = sm.getAllClothes(user)
        template_values = {
            'clothes': clothes,
            'url': url,
        }
        path = os.path.abspath('templates/addItem.html')
        self.response.out.write(template.render(path, template_values))

class EditPage(webapp2.RequestHandler):
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
        path = os.path.join(os.path.dirname(__file__), 'templates/addItem.html')
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
        self.redirect('/closet')

class Clothes(webapp2.RequestHandler):
    def post(self):
        num = int(self.request.get('num'))
        for i in range(num):
            clothing = m.Clothing()
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
        self.redirect('/closet')

class Empty(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        clothes = sm.getAllClothes(user)
        db.delete(clothes)
        self.redirect('/closet')

class MarkOutfitWorn(webapp2.RequestHandler):
    def post(self):
        keys = self.request.get_all('key')
        for key in keys:
            clothing = db.get(key)
            clothing.numWorn += 1
            if clothing.numWorn == clothing.period:
                clothing.clean = False
            clothing.put()
        self.redirect('/')

class MarkWorn(webapp2.RequestHandler):
    def post(self):
        key = self.request.get('key')
        clothing = db.get(key)
        clothing.numWorn += 1
        if clothing.numWorn == clothing.period:
            clothing.clean = False
        clothing.put()
        self.redirect('/closet')

class Laundry(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        clothes = sm.getAllClothes(user)
        for cloth in clothes:
            cloth.clean = True
            cloth.numWorn = 0
            cloth.put()
        self.redirect('/closet')

class MarkClean(webapp2.RequestHandler):
    def post(self):
        key = self.request.get('key')
        clothing = db.get(key)
        clothing.clean = True
        clothing.numWorn = 0
        clothing.put()
        self.redirect('/closet')

class MarkDirty(webapp2.RequestHandler):
    def post(self):
        key = self.request.get('key')
        clothing = db.get(key)
        clothing.clean = False
        clothing.put()
        self.redirect('/closet')

class Remove(webapp2.RequestHandler):
    def post(self):
        key = self.request.get('key')
        clothing = db.get(key)
        db.delete(clothing)
        self.redirect('/closet')
