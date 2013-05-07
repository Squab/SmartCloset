import models as m

from google.appengine.ext import db

def getAllClothes(user):
    clothes = m.Clothing.all().order('-user')
    clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1", user)
    clothes = clothes_query.fetch(None)
    return clothes

def getCleanClothes(user):
    clothes = m.Clothing.all().order('-user')
    clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1 AND clean= :2", user, True)
    clothes = clothes_query.fetch(None)
    return clothes

def getDirtyClothes(user):
    clothes = m.Clothing.all().order('-user')
    clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1 AND clean= :2", user, False)
    clothes = clothes_query.fetch(None)
    return clothes

def getTempClothes(user, size):
    clothes = m.Clothing.all().order('-user')
    clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1 AND clean= :2 AND weight= :3", user, True, size)
    clothes = clothes_query.fetch(None)
    return clothes

def getTempDirtyClothes(user, size):
    clothes = m.Clothing.all().order('-user')
    clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1 AND clean= :2 AND weight= :3", user, False, size)
    clothes = clothes_query.fetch(None)
    return clothes

def getPrefs(user):
    pquery = db.GqlQuery("SELECT * FROM Preferences where user= :1",user)
    prefs = pquery.get()  # gets the first one that matched
    if not prefs:   # no account exists yet for this user
        prefs = __makePreferences(user)
    return prefs

def __makePreferences(user):
    prefs = m.Preferences()
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
    prefs.vll = 2
    prefs.lm = 2
    prefs.mh = 2
    prefs.hvh = 2
    prefs.favType = ''
    prefs.secondFavType = ''
    prefs.warmth = 2
    return prefs