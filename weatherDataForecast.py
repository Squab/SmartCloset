import urllib2
from xml.dom.minidom import parseString
import time
class weatherDataForecast:
	wdf=''
	def __init__(self):
		wdf=''
		self.getXML()
	#Call getXML() to get the latest weather forecast before making any new decisions.
	#Returns boolean value False if weather data is not retrieved, run again
	# in this case.  Returns True otherwise.
	def getXML(self):
		city = "Austin" #city needs to be entered upon setup or determined some other way
		url = "http://api.openweathermap.org/data/2.5/forecast/daily?q="
		url += city
		url += "&mode=xml&units=imperial&cnt=1"
		source = urllib2.urlopen(url)
		#print ('source: ')
		#print (source)
		temp=source.read()
		if self.isValidXML(temp):
			self.wdf=temp
			return True
		else:
			print ('Unable to retrieve weather data, results may be outdated')
			return False
		#print ('wdf: ' + self.wdf)

	def parseTest(self,tag):
		dom = parseString(self.wdf)
		xmlTag1 = dom.getElementsByTagName(tag)[0].toxml()
		xmlData = xmlTag1.replace('<'+tag+'>','').replace('</'+tag+'>','')
		#print xmlTag1
		#print xmlData
		return xmlData

	#tests whether string dat is XML weather data, will not work for other data types
	#It is possible that weatherDataForecast will be instantiated with bad XML 
	#data, using this function in conjunction with getXML() is recommended to 
	#avoid failure of weather related functions.
	def isValidXML(self,dat):
		index=dat.find('<weatherdata>',0,len(dat))
		end=dat.find('</weatherdata>',0,len(dat))
		if index>-1 and end>index:
			return True
		else:
			return False


	#print parseTest('temperature')
	#should return a double (long? float? dunno what Python does here), degrees
	# are in farenheit
	def getCurrentTemp(self):
		hour=time.localtime()[3]
		#print hour
		if 0<hour and hour<=6:
			return self.getNightTemp()
		if 6<hour and hour<=12:
			return self.getMornTemp()
		if 12<hour and hour<=18:
			return self.getDayTemp()
		else:
			return self.getEveTemp()

	def getDayTemp(self):
		tempData=self.parseTest('temperature')
		index=tempData.find('day',0,len(tempData))+5
		end=tempData.find('eve',0,len(tempData))-2
		#print index
		#print end
		ret=float(tempData[index:end])
		return ret
	#print getDayTemp()
	def getEveTemp(self):
		tempData=self.parseTest('temperature')
		index=tempData.find('eve',0,len(tempData))+5
		end=tempData.find('max',0,len(tempData))-2
		ret=float(tempData[index:end])
		return ret
	#print getEveTemp()
	def getMaxTemp(self):
		tempData=self.parseTest('temperature')
		index=tempData.find('max',0,len(tempData))+5
		end=tempData.find('min',0,len(tempData))-2
		ret=float(tempData[index:end])
		return ret
	#print getMaxTemp()
	def getMinTemp(self):
		tempData=self.parseTest('temperature')
		index=tempData.find('min',0,len(tempData))+5
		end=tempData.find('morn',0,len(tempData))-2
		ret=float(tempData[index:end])
		return ret
	#print getMinTemp()
	def getMornTemp(self):
		tempData=self.parseTest('temperature')
		index=tempData.find('morn',0,len(tempData))+6
		end=tempData.find('night',0,len(tempData))-2
		ret=float(tempData[index:end])
		return ret
	#print getMornTemp()
	def getNightTemp(self):
		tempData=self.parseTest('temperature')
		index=tempData.find('night',0,len(tempData))+7
		end=len(tempData)-3
		ret=float(tempData[index:end])
		return ret
	#print getNightTemp()
	#returns forecasted humididty as a percentage
	#print parseTest('humidity')
	def getHumidity(self):
		humData=self.parseTest('humidity')
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
		windData=self.parseTest('windSpeed')
		index=windData.find('mps',0,len(windData))+5
		end=windData.find('name',0,len(windData))-2
		#print index
		#print end
		ret=float(windData[index:end])
		return ret
	#print getWindSpeed()
	#print parseTest('precipitation')
	def getRainSeverity(self):
		rainData=self.parseTest('precipitation')
		index=rainData.find('value',0,len(rainData))+7
		end=len(rainData)-3
		ret=float(rainData[index:end])
		#print ret
		if ret<20:
			ret=0
		if ret<50 and ret>=20:
			ret=1
		if ret>=50:
			ret=2
		return ret
	#print getRainSeverity()
