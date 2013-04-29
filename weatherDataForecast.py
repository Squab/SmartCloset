import urllib2
from xml.dom.minidom import parseString
class weatherForecast():	
	#call getXML() to get the latest weather forecast before making any new decisions
	def getXML(self):
		city = "Austin" #city needs to be entered upon setup or determined some other way
		url = "http://api.openweathermap.org/data/2.5/forecast/daily?q="
		url += city
		url += "&mode=xml&units=imperial&cnt=1"
		source = urllib2.urlopen(url)
		s = source.read()
		file =  open("weatherForecast.xml", 'w')
		file.write(s)
		file.close()

	def parseTest(tag):
		file =  open("weatherForecast.xml", 'r')
		data = file.read()
		file.close()
		dom = parseString(data)
		xmlTag1 = dom.getElementsByTagName(tag)[0].toxml()
		xmlData = xmlTag1.replace('<'+tag+'>','').replace('</'+tag+'>','')
		#print xmlTag1
		#print xmlData
		return xmlData

	#getXML()		don't uncomment unless you just want to get the latest forecast everytime you load this

	#print parseTest('temperature')
	#should return a double (long? float? dunno what Python does here), degrees are in farenheit
	def getDayTemp(self):
		tempData=parseTest('temperature')
		index=tempData.find('day',0,len(tempData))+5
		end=tempData.find('eve',0,len(tempData))-2
		#print index
		#print end
		ret=float(tempData[index:end])
		return ret
	#print getDayTemp()
	def getEveTemp(self):
		tempData=parseTest('temperature')
		index=tempData.find('eve',0,len(tempData))+5
		end=tempData.find('max',0,len(tempData))-2
		ret=float(tempData[index:end])
		return ret
	#print getEveTemp()
	def getMaxTemp(self):
		tempData=parseTest('temperature')
		index=tempData.find('max',0,len(tempData))+5
		end=tempData.find('min',0,len(tempData))-2
		ret=float(tempData[index:end])
		return ret
	#print getMaxTemp()
	def getMinTemp(self):
		tempData=parseTest('temperature')
		index=tempData.find('min',0,len(tempData))+5
		end=tempData.find('morn',0,len(tempData))-2
		ret=float(tempData[index:end])
		return ret
	#print getMinTemp()
	def getMornTemp(self):
		tempData=parseTest('temperature')
		index=tempData.find('morn',0,len(tempData))+6
		end=tempData.find('night',0,len(tempData))-2
		ret=float(tempData[index:end])
		return ret
	#print getMornTemp()
	def getNightTemp(self):
		tempData=parseTest('temperature')
		index=tempData.find('night',0,len(tempData))+7
		end=len(tempData)-3
		ret=float(tempData[index:end])
		return ret
	#print getNightTemp()
	#returns forecasted humididty as a percentage
	#print parseTest('humidity')
	def getHumidity(self):
		humData=parseTest('humidity')
		index=humData.find('value',0,len(humData))
		#print index
		end=len(humData)-3
		#print end
		ret=float(humData[index+7:end])
		return ret
	#print getHumidity()
	#returns predicted wind speed in (most likely) miles per hour
	#print parseTest('windSpeed')
	def getWindSpeed(self):
		windData=parseTest('windSpeed')
		index=windData.find('mps',0,len(windData))+5
		end=windData.find('name',0,len(windData))-2
		#print index
		#print end
		ret=float(windData[index:end])
		return ret
	#print getWindSpeed()
	#should return either 0,1,or 2 as a measure of predicted rain severity for next 3 hours
	#print parseTest('precipitation')
	def getRainSeverity(self):
		rainData=parseTest('precipitation')
		index=rainData.find('value',0,len(rainData))+7
		end=len(rainData)-3
		ret=float(rainData[index:end])
		print ret
		if ret<20:
			ret=0
		if ret<50 and ret>=20:
			ret=1
		if ret>=50:
			ret=2
		return ret
	#print getRainSeverity()
