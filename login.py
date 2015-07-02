import cookielib,urllib,urllib2,getpass
from bs4 import BeautifulSoup

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
submit="https://cusis.cuhk.edu.hk/psc/csprd/CUHK/PSFT_HR/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL"

cj=cookielib.CookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
header=[('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36')]
opener.addheaders=header

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
	password=soup.select('input[name="password"]')[0]['value']
	key=soup.select('input[name="OAM_REQ"]')[0]['value']
	data=(('username',name),('password',password),('OAM_REQ',''))
	resp1=opener.open(url1,urllib.urlencode(data))
	resp2=opener.open(url_cusis)
	soup=BeautifulSoup(resp2.read())
	input=soup.select('input')
	data=[]
	for i in input:
		if i['name']=="ICAction":
			data.append((i['name'],'DERIVED_REGFRM1_LINK_ADD_ENRL'))
		else:
			data.append((i['name'],i['value']))
		print(i['name']+": "+i['value'])
	resp_submit=opener.open(submit,urllib.urlencode(data))
	print(resp_submit.read())

	
login(name,password)
	
