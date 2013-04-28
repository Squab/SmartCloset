import urllib2
from xml.dom.minidom import parseString
def getXML():
	city = "Austin" #city needs to be entered upon setup or determined some other way
	url = "http://api.openweathermap.org/data/2.5/weather?q="
	url += city
	url += "&mode=xml&units=imperial"
	source = urllib2.urlopen(url)
	s = source.read()
	file =  open("weather.xml", 'w')
	file.write(s)
	file.close()

def parseTest(tag):
	file =  open("weather.xml", 'r')
	data = file.read()
	file.close()
	dom = parseString(data)
	xmlTag1 = dom.getElementsByTagName(tag)[0].toxml()
	xmlData = xmlTag1.replace('<'+tag+'>','').replace('</'+tag+'>','')
	#print xmlTag1
	#print xmlData
	return xmlData
#def checkCity():
getXML()
print parseTest('temperature')
#should return a double (long? float? dunno what Python does here), degrees are in farenheit
def getCurrentTemp():
	tempData=parseTest('temperature')
	index=tempData.find('value',0,len(tempData))
	end=len(tempData)-3
	#ret=tempData[index+7:index+12]
	#print index
	#print end
	ret=tempData[index+7:end]
	return ret
print getCurrentTemp()
def getMinTemp():
	tempData=parseTest('temperature')
	index=tempData.find('min',0,len(tempData))
	end=tempData.find('unit',0,len(tempData))-2
	ret=tempData[index+5:end]
	return ret
print getMinTemp()
def getMaxTemp():
	tempData=parseTest('temperature')
	index=tempData.find('max',0,len(tempData))
	end=tempData.find('min',0,len(tempData))-2
	ret=tempData[index+5:end]
	return ret
print getMaxTemp()
#returns current humididty as a percentage
print parseTest('humidity')
def getHumidity():
	humData=parseTest('humidity')
	index=humData.find('value',0,len(humData))
	#print index
	end=len(humData)-3
	#print end
	ret=humData[index+7:end]
	return ret
print getHumidity()
print parseTest('wind')
def getWindSpeed():
	windData=parseTest('wind')
	index=windData.find('value',0,len(windData))
	end=windData.find('\"/>',0,len(windData))
	#print index
	#print end
	ret=windData[index+7:end]
	return ret
print getWindSpeed()
#should return either 0,1,or 3 as a measure of predicted rain severity for next 3 hours
#def getRainSeverity
