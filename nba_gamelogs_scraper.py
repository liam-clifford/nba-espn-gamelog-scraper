import requests
from bs4 import BeautifulSoup
import string 
import csv
import urllib
import decimal
import re
import numpy as np
import datetime

date_today = datetime.date.today()
day = date_today.day
month = date_today.month
year = date_today.year

# you can plug in any of the key dates here:
Last_Game_Date = datetime.date(year, month, day+1)
Opening_Night_Date = datetime.date(year, month, day)

# key dates
# (2020, 10, 13) --> around when the nba finals concluded this year
# (2020, 7, 29) --> around when they resumed play during covid
# (2020, 3, 12) --> around when the nba was first suspended due to covid
# (2019, 10, 21) --> around when the season began

days = [Opening_Night_Date + datetime.timedelta(days=x) for x in range((Last_Game_Date-Opening_Night_Date).days + 1)]

UNIQUE_URLs = [] # unique URL list
DUPLICATE_URLs = [] # Duplicate URL list
URL_CODE_LIST = [] # URL code list

for i in days:
	try:
		month = i.month
		day = i.day
		year = i.year

		if month < 10:
			month = "0" + str(month)
		else:
			month = month

		if day < 10:
			day = "0" + str(day)
		else:
			day = day	

		date = "{}".format(year) + "/" + "{}".format(month) + "/" + "{}".format(day)

		p = requests.get("http://espn.com/nba/scoreboard/_/date/" + "{}".format(year) + "{}".format(month) + "{}".format(day))
		soup = str(BeautifulSoup(p.content, "html.parser"))

		for i in range(0,1000):
			try:
				boxscore_URL = soup.split("http://www.espn.com/nba/boxscore?gameId=")[i].split("text")[0]

				boxscore_URL = re.sub(',"',"",boxscore_URL)
				boxscore_URL = re.sub('"',"",boxscore_URL)
				if "40" in boxscore_URL: # unique ID = 40 (from url ID #)
					boxscore_URL = "http://www.espn.com/nba/boxscore?gameId=" + boxscore_URL	

					boxscore_URL_code = boxscore_URL[40:49]

					DUPLICATE_URLs.append(boxscore_URL_code)
					boxscore_URL_code_list = list(set(DUPLICATE_URLs))	#list with boxscore URL CODES
			
					URL_CODE_LIST.append(boxscore_URL)
					boxscore_URL_list = list(set(URL_CODE_LIST)) #list with boxscore URL only

			except:
				continue
	except:
		continue

for item in boxscore_URL_list:
	for i in boxscore_URL_code_list:
		if item.find(i) == 40:
			print(item)
			UNIQUE_URLs.append(item) #create list of unique URLs without Date

csv_file = open('/Users/[INSERT YOUR NAME HERE]/Desktop/[INSERT FILE NAME].csv', 'w') # this is to create a file on your local computer's desktop
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['name','team','opp','date','pos','is_starter','team_total','outcome','venue','minutes', 'fgm', 'fga', 'treysm', 'treysa', 'ftm', 'fta', 'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'to', 'pf', 'plusminus', 'pts', 'double_double', 'triple_double', 'dk_score', 'fd_score'])

print()

for i in UNIQUE_URLs:
	p = requests.get(i)

	soup = BeautifulSoup(p.content, "html.parser")
	data = soup.find_all("tr")
		
	date = soup.title.string
	date = date[date.find('e - ')+4:date.find(' - E')]

	raw_away = soup.findAll("div", {"class": "col column-one gamepackage-away-wrap"})
	raw_home = soup.findAll("div", {"class": "col column-two gamepackage-home-wrap"})

	cleaned_away = str(raw_away).encode('ascii','ignore').decode('ascii')
	cleaned_home = str(raw_home).encode('ascii','ignore').decode('ascii')

	away_score = int(re.sub(' ','',cleaned_away.split('class="highlight"')[1].split('class="pts">')[1].split('</td')[0]))
	home_score = int(re.sub(' ','',cleaned_home.split('class="highlight"')[1].split('class="pts">')[1].split('</td')[0]))

	starter_indication_away = cleaned_away.find('<th class="name">Bench</th>') # using as reference to determine starters v. bench players. Starters come before the bench players 
	starter_indication_home = cleaned_home.find('<th class="name">Bench</th>') # using as reference to determine starters v. bench players. Starters come before the bench players 

	away = cleaned_away.split('<span>')
	home = cleaned_home.split('<span>')

	for i in range(0,len(away)):
		team_away = cleaned_away.split('teamlogos')[1].split('/>')[1].split('</')[0]
		team_home = cleaned_home.split('teamlogos')[1].split('/>')[1].split('</')[0]
		try:
			if cleaned_away.split('<span>')[i+1].find('boxscore-team-stats') != -1: 
				continue
			else:
				name     = cleaned_away.split('<span>')[i+1].split('</')[0]
				
				if cleaned_away.find(name) < starter_indication_away:
					is_starter = 1
				else:
					is_starter = 0

				team_total = away_score
				if away_score < home_score:
					outcome = 'LOSS'
				else:
					outcome = 'WIN'
                 
				venue    = 0
				pos      = cleaned_away.split('<span>')[i+1].split('"position">')[1].split('</')[0]
				team     = team_away
				opp      = team_home
				minutes  = int(cleaned_away.split('<span>')[i+1].split('"min">')[1].split('</')[0])

				fgm       = cleaned_away.split('<span>')[i+1].split('"fg">')[1].split('</')[0]
				fgm       = int(fgm[:fgm.find("-")])
				fga       = cleaned_away.split('<span>')[i+1].split('"fg">')[1].split('</')[0]
				fga       = int(fga[fga.find("-")+1:])

				treysm   = cleaned_away.split('<span>')[i+1].split('"3pt">')[1].split('</')[0]
				treysm   = int(treysm[:treysm.find("-")])
				treysa   = cleaned_away.split('<span>')[i+1].split('"3pt">')[1].split('</')[0]
				treysa   = int(treysa[treysa.find("-")+1:])

				ftm      = cleaned_away.split('<span>')[i+1].split('"ft">')[1].split('</')[0]
				ftm      = int(ftm[:ftm.find("-")])
				fta      = cleaned_away.split('<span>')[i+1].split('"ft">')[1].split('</')[0]
				fta      = int(fta[fta.find("-")+1:])

				oreb     = int(cleaned_away.split('<span>')[i+1].split('"oreb">')[1].split('</')[0])
				dreb     = int(cleaned_away.split('<span>')[i+1].split('"dreb">')[1].split('</')[0])
				reb      = int(cleaned_away.split('<span>')[i+1].split('"reb">')[1].split('</')[0])
				ast      = int(cleaned_away.split('<span>')[i+1].split('"ast">')[1].split('</')[0])
				stl      = int(cleaned_away.split('<span>')[i+1].split('"stl">')[1].split('</')[0])
				blk      = int(cleaned_away.split('<span>')[i+1].split('"blk">')[1].split('</')[0])
				to       = int(cleaned_away.split('<span>')[i+1].split('"to">')[1].split('</')[0])
				pf       = int(cleaned_away.split('<span>')[i+1].split('"pf">')[1].split('</')[0])
				plusminus= int(cleaned_away.split('<span>')[i+1].split('"plusminus">')[1].split('</')[0])
				pts      = int(cleaned_away.split('<span>')[i+1].split('"pts">')[1].split('</')[0])

				if ((1 if pts >= 10 else 0) + (1 if blk >= 10 else 0) + (1 if ast >= 10 else 0) + (1 if reb >= 10 else 0)) >= 2:
					double_double = 1
				else:
					double_double = 0

				if ((1 if pts >= 10 else 0) + (1 if blk >= 10 else 0) + (1 if ast >= 10 else 0) + (1 if reb >= 10 else 0)) >= 3:
					triple_double = 1
				else:
					triple_double = 0

				dk_score = round(((pts) + (.5*treysm) + (1.25*reb) + (1.5*ast) + (2*stl) + (2*blk) + (1.5*double_double) + (3*triple_double)) - (.5*to),2)
				fd_score = round(((pts) + (1.2*reb) + (1.5*ast) + (3*stl) + (3*blk)) - to,2)
		except:
			continue
		print(name,team,opp,date,pos,is_starter,team_total,outcome,venue,minutes,fgm,fga,treysm,treysa,ftm,fta,oreb,dreb,reb,ast,stl,blk,to,pf,plusminus,pts,double_double,triple_double,dk_score,fd_score)
		csv_writer.writerow([name,team,opp,date,pos,is_starter,team_total,outcome,venue,minutes,fgm,fga,treysm,treysa,ftm,fta,oreb,dreb,reb,ast,stl,blk,to,pf,plusminus,pts,double_double,triple_double,dk_score,fd_score])

	for i in range(0,len(home)):
		try:
			if cleaned_home.split('<span>')[i+1].find('boxscore-team-stats') != -1: 
				continue
			else:
				name     = cleaned_home.split('<span>')[i+1].split('</')[0]
				
				if cleaned_home.find(name) < starter_indication_away:
					is_starter = 1
				else:
					is_starter = 0

				team_total = home_score
				if away_score < home_score:
					outcome = 'WIN'
				else:
					outcome = 'LOSS'
                 
				venue    = 0
				pos      = cleaned_home.split('<span>')[i+1].split('"position">')[1].split('</')[0]
				team     = team_home
				opp      = team_away
				minutes  = int(cleaned_home.split('<span>')[i+1].split('"min">')[1].split('</')[0])

				fgm       = cleaned_home.split('<span>')[i+1].split('"fg">')[1].split('</')[0]
				fgm       = int(fgm[:fgm.find("-")])
				fga       = cleaned_home.split('<span>')[i+1].split('"fg">')[1].split('</')[0]
				fga       = int(fga[fga.find("-")+1:])

				treysm   = cleaned_home.split('<span>')[i+1].split('"3pt">')[1].split('</')[0]
				treysm   = int(treysm[:treysm.find("-")])
				treysa   = cleaned_home.split('<span>')[i+1].split('"3pt">')[1].split('</')[0]
				treysa   = int(treysa[treysa.find("-")+1:])

				ftm      = cleaned_home.split('<span>')[i+1].split('"ft">')[1].split('</')[0]
				ftm      = int(ftm[:ftm.find("-")])
				fta      = cleaned_home.split('<span>')[i+1].split('"ft">')[1].split('</')[0]
				fta      = int(fta[fta.find("-")+1:])

				oreb     = int(cleaned_home.split('<span>')[i+1].split('"oreb">')[1].split('</')[0])
				dreb     = int(cleaned_home.split('<span>')[i+1].split('"dreb">')[1].split('</')[0])
				reb      = int(cleaned_home.split('<span>')[i+1].split('"reb">')[1].split('</')[0])
				ast      = int(cleaned_home.split('<span>')[i+1].split('"ast">')[1].split('</')[0])
				stl      = int(cleaned_home.split('<span>')[i+1].split('"stl">')[1].split('</')[0])
				blk      = int(cleaned_home.split('<span>')[i+1].split('"blk">')[1].split('</')[0])
				to       = int(cleaned_home.split('<span>')[i+1].split('"to">')[1].split('</')[0])
				pf       = int(cleaned_home.split('<span>')[i+1].split('"pf">')[1].split('</')[0])
				plusminus= int(cleaned_home.split('<span>')[i+1].split('"plusminus">')[1].split('</')[0])
				pts      = int(cleaned_home.split('<span>')[i+1].split('"pts">')[1].split('</')[0])

				if ((1 if pts >= 10 else 0) + (1 if blk >= 10 else 0) + (1 if ast >= 10 else 0) + (1 if reb >= 10 else 0)) >= 2:
					double_double = 1
				else:
					double_double = 0

				if ((1 if pts >= 10 else 0) + (1 if blk >= 10 else 0) + (1 if ast >= 10 else 0) + (1 if reb >= 10 else 0)) >= 3:
					triple_double = 1
				else:
					triple_double = 0

				dk_score = round(((pts) + (.5*treysm) + (1.25*reb) + (1.5*ast) + (2*stl) + (2*blk) + (1.5*double_double) + (3*triple_double)) - (.5*to),2)
				fd_score = round(((pts) + (1.2*reb) + (1.5*ast) + (3*stl) + (3*blk)) - to,2)
		except:
			continue
		print(name,team,opp,date,pos,is_starter,team_total,outcome,venue,minutes,fgm,fga,treysm,treysa,ftm,fta,oreb,dreb,reb,ast,stl,blk,to,pf,plusminus,pts,double_double,triple_double,dk_score,fd_score)
		csv_writer.writerow([name,team,opp,date,pos,is_starter,team_total,outcome,venue,minutes,fgm,fga,treysm,treysa,ftm,fta,oreb,dreb,reb,ast,stl,blk,to,pf,plusminus,pts,double_double,triple_double,dk_score,fd_score])
csv_file.close()