import cookielib,urllib,urllib2,getpass
from bs4 import BeautifulSoup
import json
def ifel(a,b,c):
	if(a==True):
		return(b)
	else:
		return(c)
		
name=raw_input("SID: ")
#change to "'115501xxxxx'" (include')#password=raw_input("password: ")
#change to "'xxxxxxxx'" (include')

password=getpass.getpass()

url_2="https://portal.cuhk.edu.hk/psp/epprd/?cmd=login"
url_1="https://portal.cuhk.edu.hk/psp/epprd/?cmd=login&languageCd=ENG&"
url_05="https://portal.cuhk.edu.hk/psp/epprd/?languageCd=ENG"
url0="https://onepass.cuhk.edu.hk/login/index.jsp?resource_url=https%3A%2F%2Fportal.cuhk.edu.hk%2Fpsp%2Fepprd%2F%3FlanguageCd%3DENG"
url="https://onepass.cuhk.edu.hk/login/submit.jsp"
url1="https://onepass.cuhk.edu.hk/oam/server/auth_cred_submit"
url_cusis="https://cusis.cuhk.edu.hk/psc/csprd/CUHK/PSFT_HR/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ACAD_CAREER=UG&EMPLID="+name+"&ENRL_REQUEST_ID=&INSTITUTION=CUHK1&STRM=1845"
url_submit="https://cusis.cuhk.edu.hk/psc/csprd/CUHK/PSFT_HR/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL"
url_subject="https://cusis.cuhk.edu.hk/psc/csprd/CUHK/PSFT_HR/c/SA_LEARNER_SERVICES.SSS_BROWSE_CATLG_P.GBL"

cj=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
header=[('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36')]
opener.addheaders=header

sem1='1835'
sem2='1845'
course_table='CLASS$scroll$'

def submit(url,soup,typ):
	input=soup.select('input')
	data=[]
	for i in input:
		if i['name']=="ICAction":
			data.append((i['name'],typ))
		else:
			data.append((i['name'],i['value']))
		##print(i['name']+": "+i['value'])
	return BeautifulSoup(opener.open(url,urllib.urlencode(data)).read())

def icount(content):
	size=-1
	while 1:
		try:
			content.next()
			size+=1
		except:
			break
	return size

def submit_(url,soup,typ,data):
	input=soup.select('input')
	for i in input:
		if i['name']=="ICAction":
			data.append((i['name'],typ))
		else:
			data.append((i['name'],i['value']))
		##print(i['name']+": "+i['value'])
	return BeautifulSoup(opener.open(url,urllib.urlencode(data)).read())

def login(name,password):
	opener.open(url_2)
	opener.open(url_1)
	opener.open(url_05)
	opener.open(url0)
	data=(('username',name),('password',password))
	resp=opener.open(url,urllib.urlencode(data))
	temp=resp.read()
	soup=BeautifulSoup(temp)
	name=soup.select('input[name="username"]')[0]['value']
	#print soup.select('input[name="username"]')[0].parent
	password=soup.select('input[name="password"]')[0]['value']
	key=soup.select('input[name="OAM_REQ"]')[0]['value']
	data=(('username',name),('password',password),('OAM_REQ',''))
	resp1=opener.open(url1,urllib.urlencode(data))


def cusis():
	resp2=opener.open(url_cusis)
	soup=BeautifulSoup(resp2.read())
	resp_submit=submit(url_submit,soup,'DERIVED_REGFRM1_LINK_ADD_ENRL')
	#print(resp_submit)
	

Date=['Mo','Tu','We','Th','Fr','Sa']

def change_time(time_):
	time_=time_.encode("utf-8")
	if time_[1]==':':time_="0"+time_
	if time_[(len(time_)-2):]=="PM":
		if int(time_[0:2])!=12:
			time_=str(int(time_[0:2])+12)+time_[2:5]
	return time_[0:5]

class Time:
	def __init__(self,date,start,end,place,name):#input ('Mo','13:30','14:30','bilibili')
		sum=0
		for i in range(0,5):
			if Date[i]==date:
				sum+=1440*i
		start=change_time(start)
		end=change_time(end)
		##print [date,start,end,place]
		if start=='TBA':
			self._start='TBA'
			self._end='TBA'
			self.start='TBA'
			self.date='TBA'
			self.end='TBA'
			self.place=place
			self.name=name
			self.session=""
			return
		else:
			self._start=sum+int(start[0:2])*60+int(start[3:5])
			self._end=sum+int(end[0:2]*60)+int(end[3:5])
			self.start=start
			self.date=date
			self.end=end
			self.place=place
			self.name=name
			self.session=[]
			for i in range(int(start[0:2])-7,int(end[0:2])-7):
				temp=date.encode('UTF-8')+'_'+str(i-1)
				self.session.append(temp)
			self.session='#'.join(self.session)
#	def __call__(self):
		#print(Date[self.date]+' '+self.start+' to '+self.end+' at '+self.place)

class Class:
	def __init__(self):
		self.times=[]
		self.title=""
	def refresh(self,soup,tag,title):
		self.title=title
		if not tag.parent.parent.next_sibling:
			return
		temp=tag.parent.parent.next_sibling.next_sibling.next_sibling.next_sibling
		###print temp.contents
		temp=temp.contents[3].contents[1].contents
		print temp
		for i in range(1,len(temp)):
			if i!=1 and i%2!=0:
				content=temp[i].contents
				date=content[1].contents[1].text
				start=content[3].contents[1].text
				end=content[5].contents[1].text
				place=content[7].contents[1].text
				name=content[9].contents[1].text
				_time=Time(date,start,end,place,name)
				self.times.append(_time)


class Tuto(Class):
	pass
	
class Lec(Class):
	pass
	

class Section:
	def __init__(self,term):
		self.term=term
		self.lec=[]
		self.tuto=[]
		self.ok=True
	def refresh(self,soup,tag):
		title=tag.parent.parent.contents[3].contents[1].contents[3].contents[1].contents[1].contents[1].text
		if title.find('LEC')==-1:
			ok=False
			return 
		lec=Lec()
		lec.refresh(soup,tag,title)
		self.lec.append(lec)
		temp=tag.parent.parent
		#not the last tag
		while icount(temp.next_siblings)>8:
			for i in range(0,10):
				temp=temp.next_sibling
			title=temp.contents[3].contents[1].contents[3].contents[1].contents[1].contents[1].text
			if title.find('LEC')==-1:
				tuto=Tuto()
				print title
				tuto.refresh(soup,temp.contents[3].contents[1],title)
				self.tuto.append(tuto)
			else:
				return
	
	
class Course:
	def __init__(self,name,codes):
		self._unit=0
		self.sections=[]
		self.classes=[]
		self._class=False
		self._req=''
		self._description=''
		self._title=name
		self._code=codes
		print codes
	def refresh(self,soup):
		#collecting course info
		units=soup.select('label[for="DERIVED_CRSECAT_UNITS_RANGE$0"]')[0]
		tr=units.parent.parent.next_sibling.next_sibling
		self._unit=tr.contents[3].contents[1].text
		#print self._unit
		pre=soup.select('label[for="SSR_CRSE_OFF_VW_RQRMNT_GROUP$0"]')
		if len(pre)!=0:
			tr=pre[0].parent.parent.next_sibling.next_sibling
			self._req=tr.contents[3].contents[1].contents[0]
		if len(soup.select('span[class="PSLONGEDITBOX"]'))!=0:
			self._description=soup.select('span[class="PSLONGEDITBOX"]')[0].text
		#collecting time info
		a=soup.select('a[name="DERIVED_SAA_CRS_SSR_PB_GO"]')
		if(len(a)==0):
			return submit(url_subject,soup,'DERIVED_SAA_CRS_RETURN_PB')
		soup=submit(url_subject,soup,'DERIVED_SAA_CRS_SSR_PB_GO')
		a=soup.select('a[title^="View"]')[0]
		#check first sem
		first=soup.select('option[selected="selected"]')[1]
		if first['value']!=sem1:
			#sem1 no course
			pass
		else:
			#if more than 5, expand all
			b=soup.select('a[class="PSLEVEL1GRIDNAVIGATIONBAR"]')
			if len(b)>0:
				soup=submit(url_subject,soup,b[0]['name'])
			classes=soup.select('table[id^="CLASS$"]')
			#print len(classes)
			for i in classes:
				section=Section(sem1)
				section.refresh(soup,i)
				if section.ok==True:
					self.sections.append(section)
		soup=submit(url_subject,soup,'DERIVED_SAA_CRS_RETURN_PB')
		return soup

##def find_course: use a webpage to find the specific course info and return a course


def save(course):
	records=[course._code.encode('UTF-8'),course._title.encode('UTF-8'),course._unit.encode('UTF-8'),course._req.encode('UTF-8'),course._description.encode('UTF-8')]
	record1=[]
	print len(course.sections)
	for section in course.sections:
		lec_=[]
		tuto_=[]
		for lec in section.lec:
			time__=[]
			for time_ in lec.times:
				time__.append(time_.session)
				#print [time_.date.encode('UTF-8'),time_.start,time_.end,time_.place.encode('UTF-8'),time_.name.encode('UTF-8')]
			lec_.append([lec.title,time_.place.encode('UTF-8'),'#'.join(time__),time_.name.encode('UTF-8')])
		for tuto in section.tuto:
			for time_ in tuto.times:
				tuto_.append([tuto.title,time_.place.encode('UTF-8'),time_.session,time_.name.encode('UTF-8')])
		record1.append([lec_,tuto_])
	url="http://127.0.0.1:8888/index.php"
	records.append(record1)
	print opener.open(url,json.dumps(records).replace('\n',' ')).read()
		
		

class Subject:
	def refresh(self,soup):
		input=soup.select('a[title^="View"]')
		for i in range(0,len(input)):
			soup=submit(url_subject,soup,input[i]['name'])
			name=soup.select('span[class="PALEVEL0SECONDARY"]')[0]
			codes=name.text[0:4]+name.text[5:9]
			names=name.text[12:]
			course=Course(names,codes)
			soup=course.refresh(soup)
			##print soup
			save(course)
			self.courses.append(course)
		return soup
	def __init__(self,name):
		self.name=''
		self.courses=[]
		self.name=name




class Alphabet:
	def __init__(self,name):
		self.subjects=[]
		self.courses=[]
		self.name=name
	def refresh(self):
		resp=opener.open(url_subject)
		soup=BeautifulSoup(resp)
		soup=submit(url_subject,soup,'DERIVED_SSS_BCC_SSR_ALPHANUM_'+self.name)
		a=soup.select('a[title^="Show/Hide"]')
		for i in range(13,len(a)):
			if i>0:
				soup=submit(url_subject,soup,a[i-1]['name'])
				soup=submit(url_subject,soup,a[i-1]['name'])
			soup=submit(url_subject,soup,a[i]['name'])
			##print soup
			#print a[i].text
			subject=Subject(a[i].text)
			subject.refresh(soup)
			self.subjects.append(subject)
		return self
			##soup=subjects.push(subject,soup)
		
	


login(name,password)
record=[]
#for i in range(66,86):
Alphabet('S').refresh()



