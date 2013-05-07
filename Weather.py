import os

import standard_methods as sm
from weatherDataForecast import weatherDataForecast

import webapp2
from google.appengine.api import users
from google.appengine.ext.webapp import template


class WeatherPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        url = users.create_logout_url(self.request.uri)  
        prefs = sm.getPrefs(user)  
        w = weatherDataForecast(prefs.location)
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
        path = os.path.join(os.path.dirname(__file__), 'templates/weather.html')
        self.response.out.write(template.render(path, template_values))
