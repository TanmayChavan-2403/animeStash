import crochet
crochet.setup()
import os, re, time


import multiprocessing
import flask
from flask import Flask, render_template, url_for, request, session, redirect, jsonify, g, session
from webfunctions import randomWallpaper, animeInfo, animeInfo_s, mal, quote, characters, accurate_search
from webfunctions import wallpapers
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
import requests, json, random, time
from flask_mysqldb import MySQL
from cryptography.fernet import Fernet
from flask.globals import _request_ctx_stack

from spiders.Animeplanet import AnimePlanet
from spiders.AnimeUKNews import AnimeUkNews
from spiders.Episodes import Gogoanime
from spiders.Airing import Recent_Series
from spiders.Staffs import staffs
from spiders.Ninemanga import NineManga
from spiders.MangaLatest import mangaL
from spiders.Mangachapters import mangaC
from spiders.Episode_links import gogoPlay
from spiders.AnimeUkNet import AnimeNews
from spiders.animeNF import AnimeNewsNFacts
from spiders.PopularAnimes import PopularAnimes

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']= 'root'
app.config['MYSQL_DB'] = 'users'

mysql = MySQL(app)

global key
key = b'F-64dVzPNL1ARoayzs_PFSGdKQpNVh3fuecO_xV2NVo='
f = Fernet(key)
app.secret_key = 'sf4a6s5df1sdf8sadf16s5'

global flag
global output_data

output_data = []
crawl_runner = CrawlerRunner()

@app.route('/')
@app.route('/home')
def home():
	session['heading_font'] = 'Poppins'
	session['paragraph_font'] = 'Righteous'
	session['button_font'] = 'Bree Serif'
	session['status'] = 1
	session['user'] = ''
	return render_template('home.html')

@app.route('/Userpage', methods=['GET', 'POST'])
def Userpage():
	if request.method == 'POST':
		if request.args.get('type') =='UserUpdate':
			username = request.form.get('username')
			email = request.form.get('email')
			password = request.form.get('password')
			avatar = request.args.get('u_avatar')
			print('Avatar value', username, email, password,avatar)
			if avatar is None or avatar == '':
				avatar = 'av1'
			if username is None or username == '':
				username = request.args.get('u_name')
			if email is None or email == '' :
				email = request.args.get('u_email')
			if password is None or password == '':
				password = request.args.get('u_password')

			print('CRL [Userpage] and data received is --> ', username, password, email, avatar)
			cursor = mysql.connection.cursor()
			cursor.execute("delete from user where name ='{0}' ".format(session['user']))
			mysql.connection.commit()

			password = bytes(password, 'utf-8')
			password = f.encrypt(password)

			cursor.execute('insert into user(name, password, email, avatar) values(%s, %s, %s, %s)',(username, password, email, avatar))
			mysql.connection.commit()


			# cursor.execute(" update user set name='{0}', password={1}, email='{2}' where name='{3}'".format(username, password, email, session['user']))
			session['user'] = username
		elif request.args.get('type') == 'Avatar':
			u = request.args.get('u_name')
			p = request.args.get('u_password')
			e = request.args.get('u_email')
			a = request.form.get('avatar')
			print('Avatar value', a)
			if a is None:
				a = 'av1'

			cursor = mysql.connection.cursor()
			cursor.execute("update user set avatar='{0}' where name='{1}' ".format(a, session['user']))
			mysql.connection.commit()
			return render_template('Userpage.html', userData = [u, e, p, a])
		elif request.args.get('type') == 'Font':
			heading = request.form.get('font-heading')
			paragraph = request.form.get('font-para')
			button = request.form.get('font-button')
			if heading is None:
				heading = 'Poppins'
			if paragraph is None:
				paragraph = 'Righteous'
			if button is None:
				button = 'Bree Serif'
			session['heading_font'] = heading
			session['paragraph_font'] = paragraph
			session['button_font'] = button
		return render_template('mainpage.html')

	cursor = mysql.connection.cursor()
	if 'user' in session:
		cursor.execute("select * from user WHERE name = '{0}' ".format(session['user']))
		assets = cursor.fetchall()
		u = assets[0][0]
		p = f.decrypt(assets[0][1]).decode('utf-8')
		e = assets[0][2]
		a = assets[0][3]
	else:
		session['user'] = ''
		u = 'Tanmay'
		p = 'TanmayChavan'
		e = 'Email-id'
		a = 'avatar'
	return render_template('Userpage.html', userData = [u, e, p, a])

@app.route('/airing')
def airing():
	crawler = Recent_Series
	btn_type = request.args.get('type')
	if btn_type == 'previous':
		session['currentPage'] -= 1
		fetched_data = scrape(session['currentPage'], crawler, '')
	elif btn_type == 'next':
		session['currentPage'] += 1
		fetched_data = scrape(session['currentPage'], crawler, '')
	else:
		session['currentPage'] = 1
		fetched_data = scrape(session['currentPage'], crawler, '')

	return render_template('Airing.html', content = fetched_data)

@app.route('/mainpage', methods=['POST', 'GET'])	
def mainpage():
	crawler = PopularAnimes
	
	if request.args.get('type') == 'logout':
		session['user'] = ''

	# This function was used when website was having search bar then this function used to check if
	# user is searching for any anime, then used to redirect to search result page
	# if request.method == 'POST':
	# 	anime_name = request.form['animesearch']
	# 	return redirect(url_for('SearchResult', animeName = anime_name, recomendation=''))
	try:
		return render_template('mainpage.html', mainpageData = fetched_data)
	except:
		fetched_data = scrape('', crawler, '')

	return render_template('mainpage.html', mainpageData=fetched_data)
	# return render_template('mainpage.html')


@app.route('/SearchResult', methods=['POST', 'GET'])
def SearchResult():
	if request.method == 'POST':
		animeName = request.form['animesearchacc']
		# print('CRL [ SearchResult ] looking for incoming request -->', animeName)
		data = accurate_search(animeName)
		return render_template('SearchResult.html', content=data)

	suggestion = request.args.get('recomendation')
	if suggestion != '':
		data = animeInfo(suggestion)
		print('CRL -> [SearchResult] after fetching we got ->> ', data)
		return render_template('SearchResult.html', content=data)

	
	animeName = request.args.get('animeName')
	data = animeInfo(animeName)
	print('CRL -> [SearchResult] after fetching we got ->> ', data)

	return render_template('SearchResult.html', content=data)

@app.route('/Wallpaper')
def Wallpaper():
	anime_name = request.args.get('name')
	fetched_data = wallpapers(anime_name)	
	return render_template('Wallpaper.html', wallpapers=fetched_data)

@app.route('/Links')
def Links():
	crawler = gogoPlay

	link = request.args.get('link')	
	fetched_data = scrape(link, crawler, '')
	# print(fetched_data)

	return render_template('Links.html', content = fetched_data)

@app.route('/Download')
def Download():
	global flag
	flag = False
	crawler = Gogoanime

	anime_name = request.args.get('name')
	link = request.args.get('link')
	c_type = request.args.get('type')
	# print('CRL [Download] Checking for crawl type received -->', c_type)
	imgURL = randomWallpaper(anime_name)
	if c_type == 'dlist':
		fetched_data = scrape(anime_name, crawler, c_type)
	else:
		fetched_data = scrape(link, crawler, c_type)
	while flag == False:
		pass
	# print(c_type)
	# print(anime_name)
	print('CRL -> [ Download ] fetched_content is ---> ', fetched_data)
	
	return render_template('Download.html', content=fetched_data, title=anime_name, wallpaper=imgURL, crawl_type=c_type, length= len(fetched_data))


@app.route('/AnimeInfo', methods=['POST', 'GET'])
def AnimeInfo():

	animeTitle = request.args.get('animeTitle')
	animeId = request.args.get('animeId')
	imgURL = randomWallpaper(animeTitle)
	data = animeInfo_s(animeTitle, animeId)

	return render_template('AnimeInfo.html', imageURL = imgURL, content= data)


@app.route('/MangaInfo')
def MangaInfo():
	crawler = NineManga

	type_ = request.args.get('type')
	manga = request.args.get('manga')
	print(' CRL [ MangaInfo ] received info is -->', type_, '          ', manga)
	fetched_data = scrape( manga, crawler, type_ )
	return render_template('MangaInfo.html', content = fetched_data)











@app.route('/MangaL', methods=['POST', 'GET'])
def MangaL():
	crawler1 = mangaL
	crawler2 = NineManga

	# If request method is post that means user is searching for some manga using search bar [ MangaL.html line no 47 ] 
	if request.method == 'POST':
		m_name = request.form['mangasearch']
		fetched_data = scrape(m_name, crawler2, 'dlist')
	
	# If request args type is dlist means that user have clicked on some card and now we have to fecth more 
	# details / related manga [ MangaL.html line no 93 ]
	elif request.args.get('type') == 'dlist':
		type_ = request.args.get('type') # type of req, dlist means we have to extract list from crawler
		manga = request.args.get('manga') # Manga name which we have to search for
		fetched_data = scrape( manga, crawler2, type_ )

	# If user clicks on one of the tabs present in website which are "Hot", "Completed" and "Newest" then 
	# we have to fetch manga accordingly with the help of scrapper. Also when user clicks on previous of next 
	# button then we have to scrape the manga present on next page from the website from which we are scraping.
	elif request.args.get('type') in ['topview', 'newest', 'Completed', 'previous', 'next']:
		btn_type = request.args.get('type')
		category = request.args.get('category')
		if btn_type == 'previous':
			session['currentPage'] -= 1
			fetched_data = scrape(session['currentPage'], crawler1, category)

		elif btn_type == 'next':
			if (session['currentPage']):
				session['currentPage'] += 1
			else:
				session['currentPage'] = 1 
			fetched_data = scrape(session['currentPage'], crawler1, category)

		else:
			session['currentPage'] = 1
			fetched_data = scrape(session['currentPage'], crawler1, category)
		return render_template('MangaL.html', content = fetched_data, type_ = '', postBack = category)
	# If no action is triggered then user have entered this manga page for first time and now we have to display 
	# latest and popular manga from first page of mangakakalot
	else:
		fetched_data = scrape('', crawler1, '')
		return render_template('MangaL.html', content = fetched_data, type_ = 'auto') # type auto means nothing for now just a placeholder 

	return render_template('MangaL.html', content = fetched_data, type_ = 'Search', postBack = '')






@app.route('/MangaChapter')
def MangaChapter():
	crawler = mangaC

	link = request.args.get('link')

	fetched_data = scrape(link, crawler, 'dlink')
	print('CRL [ MangaChapter ] fetched_data is --> ', fetched_data)

	return render_template('MangaChapter.html', content = fetched_data, length = len(fetched_data) + 1)



@app.route('/CharacterPage')
def CharacterPage():
	global flag
	flag = False
	crawler = AnimePlanet

	
	if request.args.get('source') == 'characterPage': #Checking from which page character request was issued
		btn_type = request.args.get('type')

		if btn_type == 'previous':
			page = session['currentPage'] - 1
			characters_fetched = characters(session['target'], page)
			session['currentPage'] = characters_fetched['currentPage']
			session['hasNextPage'] = characters_fetched['hasNextPage']
			fetched_data = scrape(characters_fetched, crawler, 'lists')
			return render_template('CharacterPage.html', content= fetched_data)

		elif btn_type == 'next':
			page = session['currentPage'] + 1
			characters_fetched = characters(session['target'], page)
			session['currentPage'] = characters_fetched['currentPage']
			session['hasNextPage'] = characters_fetched['hasNextPage']
			fetched_data = scrape(characters_fetched, crawler, 'lists')
			return render_template('CharacterPage.html', content= fetched_data)

	# For multiple character search
	anime_name = request.args.get('chs')
	if anime_name != '':
		characters_fetched = characters(anime_name, page=1 )
		# print('CRL [ CharacterPage ] characters fetched are --> ', characters_fetched)
		session['hasNextPage'] = characters_fetched['hasNextPage']
		session['currentPage'] = characters_fetched['currentPage']
		session['target'] = anime_name

		fetched_data = scrape(characters_fetched, crawler, 'lists')
		return render_template('CharacterPage.html', content=fetched_data, page=1, lastPage= 2)


	# For single character search
	baseURL = 'https://www.anime-planet.com/characters/'
	# print(request.args.get('ch_name'))
	char_name = request.args.get('ch_name').lower().replace(' ', '-')
	# char_name = char_name.lower().replace(' ','-')
	readyURL = baseURL + char_name

	fetched_data = scrape(readyURL, crawler, '')
	return render_template('CharacterPage.html', content=fetched_data)

@app.route('/Staff')
def Staff():
	crawler = staffs

	s_name = request.args.get('sname').lower().replace(' ','-')
	print(' CRL [ Staff ] Looking for staff name --> ', s_name)
	fetched_data = scrape( s_name, crawler,'')
	return render_template('Staff.html', content = fetched_data)

@app.route('/NewsRootPage')
def NewsRootPage():
	return render_template('NewsRootPage.html')

@app.route('/AnimeUKNews')
def AnimeUKNews():
	d_type = request.args.get('type')
	heading = request.args.get('heading')
	if d_type is not None:
		baseURL = f'https://animeuknews.net/category/{d_type}/'	
		return redirect(url_for('NewsList', URL=baseURL, title=heading, crawler = 'AnimeUKNews'))

	return render_template('AnimeUKNews.html')

@app.route('/ukNewsdotnet')
def ukNewsdotnet():
	d_type = request.args.get('type')
	heading = request.args.get('heading')
	if d_type is not None:
		baseURL = f"https://www.uk-anime.net/{d_type}"
		return redirect(url_for('NewsList', URL=baseURL, title=heading, crawler='AnimeNews' ))
		

	return render_template('ukNewsdotnet.html')

@app.route('/NewsList')
def NewsList():
	global flag

	flag = False
	URL = request.args.get('URL')
	heading = request.args.get('title')
	spider = request.args.get('crawler')
	
	print(spider, URL)
	if spider == 'AnimeNews':
		crawler = AnimeNews
	elif spider == 'animenewsandfacts':
		crawler = AnimeNewsNFacts
		heading = 'News'
	else:
		crawler = AnimeUkNews


	fetched_data = scrape(URL, crawler, 'list')
	while flag == False:
		pass

	return render_template('NewsList.html', data = fetched_data, title = heading)


@app.route('/NewsDetails')
def NewsDetails():
	global flag
	flag = False

	URL = request.args.get('link')
	title = request.args.get('title')
	
	print(URL)	
	if 'animeuknews.net' in URL:
		crawler = AnimeUkNews
	elif 'uk-anime.net' in URL:
		crawler = AnimeNews
	elif 'animenewsandfacts' in URL:
		crawler = AnimeNewsNFacts


	fetched_data = scrape(URL, crawler, 'details')
	while flag == False:
		pass
	print('CRL [NewsDetails] -->', fetched_data)
	return render_template('NewsDetails.html', content=fetched_data[0]['Data'], heading=title, post_img = fetched_data[0]['Post_image'])


@app.route('/signUp', methods=['POST', 'GET'])
def signUp():

	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email-id']
		password = request.form['password']
		cursor = mysql.connection.cursor()

		# Fetching data from database for validation
		cursor.execute('select * from user')
		assets = cursor.fetchall()
		usernames = [ user[0] for user in assets]
		passwords = [ password[1] for password in assets ]
		emails = [ email[2] for email in assets ]

		#Checking if requested data is in database or not
		if username == '':
			return render_template('signUp.html', status='error', err_type='empty', message='Username')
		elif username in usernames:
			return render_template('signUp.html', status='error', err_type='present', message='Username')
		elif email == '':
			return render_template('signUp.html', status='error', err_type='empty', message = 'Email')
		elif email in emails:
			return render_template('signUp.html', status='error', err_type='present', message = 'Email')
		elif password == '':
			return render_template('signUp.html', status='error', err_type='empty', message = 'Password')
		elif password in passwords:
			return render_template('signUp.html', status='error', err_type='present', message = 'Password')

		session['user'] = username
		password = bytes(password, 'utf-8')
		password = f.encrypt(password)
		cursor.execute('insert into user(name, password, email, avatar) values(%s, %s, %s, %s)',(username, password, email, 'av1'))
		mysql.connection.commit()
		
		return render_template('Success.html', message='Registration Successfull')

	return render_template('signUp.html', status='')


@app.route('/Login', methods=['POST', 'GET'])
def Login():

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		cursor = mysql.connection.cursor()
		cursor.execute('select * from user')
		assets = cursor.fetchall()

		d = {}
		for data in assets:
			d.update({ data[0]: f.decrypt(data[1]).decode('utf-8') })


		e = {}
		for data in assets:
			e.update({ data[0]: data[2] })



		if username == '':
			return render_template('Login.html',status = 'error', err_type='empty', message = 'Username')
		if username in d:
			if password == '':
				return render_template('Login.html',status = 'error', err_type='empty', message = 'Password')
			elif d[username] != password:
				star_email = re.sub('@gmail.com', '', e[username])
				star_email = star_email[:4] + '******' + star_email[-4:]
				return render_template('Login.html',status = 'error', err_type='absent', message = star_email)
		else:
			return render_template('Login.html',status = 'error', err_type='absent', message = '2')

		session['user'] = username
		return render_template('Success.html', message='Login Successfull')

	return render_template('Login.html')


@app.route('/output.html')
def output():
	return render_template('output.html')


@app.route('/Success')
def Success():

	return render_template('Success.html')


























@app.route('/content') # render the content a url differnt from index
def content():
    def inner():
        # # simulate a long process to watch
        # for i in range(500):
        #     j = math.sqrt(i)
        #     time.sleep(1)
        #     # this value should be inserted into an HTML template
        #     yield str(i) + '<br/>\n'
        for i in range(12):
        	session['status'] += i
        	time.sleep(1)
        	yield session['status']
    return flask.Response(inner(), mimetype='text/html')




def _type(val):
	return type(val)

def _len(val):
	return len(val)

def validate(v):
	return str(list(v))

def _str(v):
	return str(v)

def quality(link):
	print('CRL [ quality ] checkking for received paramerter ----> ', link)
	if '360p' in link:
		return '36'
	elif '480p' in link:
		return '48'
	elif '720p' in link:
		return '72'
	elif '1080p' in link:
		return '108'
	# return re.findall('(\d+).(p)', link)[0][0]

def checkDomain(data):
	try:
		data['animeRlink']
		return True
	except:
		return False

@app.context_processor
def cp():
	return dict(
		validate= validate,
		quality=quality,
		_type= _type,
		_len = _len,
		_str = _str,
		checkDomain = checkDomain
	)



@app.route('/scrape')
def scrape(readyURL, crawler, crawl_type):
	global output_data
	global flag

	flag = False
	output_data = []	

	start_crawling(readyURL, crawler, crawl_type)

	while flag == False:
		pass

	if crawl_type.split(' ')[0] == 'dlink':
		d = {}
		for data in output_data:
			d.update(data)
		return d
	print('Reaching here')
	return output_data


@crochet.run_in_reactor
def start_crawling(readyURL, crawler, crawl_type):

	print('CRL [ Crawler Engine ] crawling initaited by Spider' )

	dispatcher.connect(_crawler_result, signal = signals.item_scraped)
	dispatcher.connect(_crawler_status, signal = signals.engine_stopped)
	eventual = crawl_runner.crawl(crawler, category = readyURL, c_type=crawl_type)
	return eventual

def _crawler_result(item, response, spider):
	# with app.test_request_context():
	# 	session['status'] += 1

	output_data.append(dict(item))
	print('ITs reaching here :) :) :) :) :) :) :) :) :) :) :) :) :) :)')
	print(output_data)
	return


def _crawler_status():
	global flag

	flag = True
	print('Spider has crawled and now its resting :( ')



if __name__ == '__main__':
	app.run(debug = True)