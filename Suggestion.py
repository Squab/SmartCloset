import random

import standard_methods as sm

from google.appengine.ext import db
from google.appengine.api import users


class SuggestionEngine:
    user = False
    weights = False
    prefs = False

    def __init__(self, user):
        self.user = user
        self.prefs = sm.getPrefs(user)
        self.weights = {"verylight": 1}
        self.weights["light"] = self.weights["verylight"]*self.prefs.vll
        self.weights["medium"] = self.weights["light"]*self.prefs.lm
        self.weights["heavy"] = self.weights["medium"]*self.prefs.mh
        self.weights["veryheavy"] = self.weights["heavy"]*self.prefs.hvh

    def newSuggestion(self, weather):
        addTypes = []
        high = weather.getMaxTemp()
        low = weather.getMinTemp()
        chosenTypes = self.pickTypes()
        chosenTypes.extend(addTypes)
        [highClothes, aveWeight] = self.highestSuggestion(high, chosenTypes)
        if not highClothes:
            return [[], []]
        suggestion = self.lowestSuggestion(low, highClothes, aveWeight)
        return suggestion

    def lowestSuggestion(self, low, highClothes, aveWeight):
        additionalClothes = []
        suggestion = [highClothes]
        clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1 AND cat= :2 AND clean= :3", self.user, 'jacket', True)
        clothes = clothes_query.fetch(None)
        if not clothes:
            return [[], 0]
        clothes.sort(key = self.getItemWeight)
        targetSize = self.getSize(low)
        targetWeight = self.getWeight(targetSize)
        currWeight = aveWeight
        deltaWeight = targetWeight - currWeight
        while currWeight < targetWeight:
            item = self.pickItem(clothes, deltaWeight)
            itemWeight = self.getItemWeight(item)
            deltaWeight -= itemWeight
            if self.prefs.warmth > 0 or deltaWeight > 0:
                additionalClothes.append(item)
                currWeight += itemWeight
            else:
                deltaWeight += itemWeight
        suggestion.append(additionalClothes)
        return suggestion

    def highestSuggestion(self, high, chosenTypes):
        suggestion = []
        totalWeight = 0;
        for choice in chosenTypes:
            clothes_query = db.GqlQuery("SELECT * FROM Clothing where user= :1 AND cat IN :2 AND clean= :3", self.user, choice, True)
            clothes = clothes_query.fetch(None)
            if not clothes:
                return [[], 0]
            clothes.sort(key = self.getItemWeight)
            currWeight = 0
            targetSize = self.getSize(high)
            targetWeight = self.getWeight(targetSize)
            deltaWeight = targetWeight - currWeight
            clothes = self.validClothes(clothes, targetWeight)
            while currWeight < targetWeight:
                item = self.pickItem(clothes, deltaWeight)
                if not item:
                    break
                itemWeight = self.getItemWeight(item)
                deltaWeight -= itemWeight
                if self.prefs.warmth > 0 or deltaWeight > 0:
                    suggestion.append(item)
                    currWeight += itemWeight
                    totalWeight += itemWeight
                else:
                    deltaWeight += itemWeight
        return [suggestion, totalWeight/len(chosenTypes)]


    def validClothes(self, clothes, weight):
        validClothes = []
        for cloth in clothes:
            if self.getItemWeight(cloth) <= weight:
                validClothes.append(cloth)
            else:
                break
        return validClothes

    def pickItem(self, clothes, weight):
        for cloth in clothes:
            if self.getItemWeight(cloth) > weight:
                clothes.remove(cloth)
                continue
            val = random.randint(0, int(len(clothes)/2))
            if val < 2:
                return cloth
        for cloth in clothes:
            if self.getItemWeight(cloth) > weight:
                return clothes

    def pickTypes(self):
        types = ['dress', 'top_and_bottom']
        if self.prefs.favType:
            types.append(prefs.favType)
            types.append(prefs.favType)
        if self.prefs.secondFavType:
            types.append(prefs.secondfavType)
        chosenType = random.choice(types)
        if 'top_and_bottom' in chosenType:
            chosenType = [['top', 'jacket'], ['bottom']]
        elif 'dress' in chosenType:
            chosenType = [['dress', 'jacket']]
        #return chosenType
        return [['dress', 'jacket']]

    def getItemWeight(self, item):
        return self.getWeight(item.weight)

    def getWeight(self, size):
        return self.weights[size]

    def getSize(self, temp):
        sizes = self.getSizes(temp)
        helfLen = len(sizes)/2
        if self.prefs.warmth == 2:
            return sizes[-1]
        elif self.prefs.warmth == 1:
            return sizes[math.ceil(halfLen)]
        elif self.pref.warmth == 0:
            return sizes[random.getrandbits(1) * math.trunc(halfLen) + halfLen]
        elif self.prefs.warmth == -1:
            return sizes[math.floor(halfLen)]
        else:
            return sizes[0]

    def getSizes(self, currentTemp):
        sizes = []
        if(currentTemp >= self.prefs.verylight_min):
            sizes.append('verylight')
        elif(currentTemp <= self.prefs.light_max and currentTemp >= self.prefs.light_min):
            sizes.append('light')
        elif(currentTemp <= self.prefs.medium_max and currentTemp >= self.prefs.medium_min):
            sizes.append('medium')
        elif(currentTemp <= self.prefs.heavy_max and currentTemp >= self.prefs.heavy_min):
            sizes.append('heavy')
        elif(currentTemp <= self.prefs.veryheavy_max):
            sizes.append('veryheavy')
        return sizes

    def getOutfitTop(size):
        clothes = Clothing.all().order('-user')
        c
        clothes = clothes_query.fetch(None)
        numItems = len(clothes)
        if(numItems == 1):
            return clothes.pop()
        elif(numItems == 0):
            return None
        index = random.randint(0,numItems-1)
        cloth = clothes.pop(index)
        return cloth

    def getOutfitBottom(size):
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

    def getMainValues(temp):
        prefs = getPrefs(user)
        size = getSize(user, temp, prefs)
        dirty = getTempDirtyClothes(user, size)
        top = getOutfitTop(user, size)
        bottom = getOutfitBottom(user, size)
        return [prefs, size, dirty, top, bottom, bottom, top]