import cgi
import os

from weatherDataForecast import weatherDataForecast
import suggestion as sugg

from google.appengine.ext.webapp import template
from google.appengine.api import users
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db


class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)
        w = weatherDataForecast()
        w.getXML()
        currentTemp = int(round(w.getCurrentTemp()))
        wind = int(round(w.getWindSpeed()))
        suggEng = sugg.SuggestionEngine(user)
        suggestion = suggEng.newSuggestion(w)
        template_values = {
            'url': url,
            'currentTemp': currentTemp,
            'wind': wind,
            'suggestion': suggestion
        }
        path = os.path.abspath('templates/index.html')
        self.response.out.write(template.render(path, template_values))


application = webapp2.WSGIApplication(
    [('/', MainPage),
     ('/cloth', 'closet.Clothes'),
     ('/closet', 'closet.ClosetPage'),
     ('/addItem', 'closet.AddItemPage'),
     ('/empty', 'closet.Empty'),
     ('/edit', 'closet.EditPage'),
     ('/laundry', 'closet.Laundry'),
     ('/clean', 'closet.MarkClean'),
     ('/dirty', 'closet.MarkDirty'),
     ('/remove', 'closet.Remove'),
     ('/worn', 'closet.MarkWorn'),
     ('/wornOutfitWorn', 'closet.MarkOutfitWorn'),
     ('/weather', 'weather.WeatherPage'),
     ('/prefs', 'preferences.PrefPage')],
     debug = True)




def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
