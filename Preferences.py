import os

import standard_methods as sm

import webapp2
from google.appengine.api import users
from google.appengine.ext.webapp import template

class PrefPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
        clothes = sm.getAllClothes(user)
        prefs = sm.getPrefs(user)
        template_values = {
            'prefs': prefs,
            'clothes': clothes,
            'url': url,
        }
        path = os.path.join(os.path.dirname(__file__), 'templates/prefs.html')
        self.response.out.write(template.render(path, template_values))

    def post(self):
        user = users.get_current_user()
        prefs = sm.getPrefs(user)
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
