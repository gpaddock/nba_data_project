import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
print("imports complete")

# working
def get_nba_bio_table():
	# table that all teams will be added to, turned into CSV
	master_table = pd.DataFrame
	# Create a dataframe
	master_table = pd.DataFrame()

	# base string components, loop through to build links for each team
	team_abbrev = [
		"TOR", "BOS", "NYK", "BRK", "PHI",
		"CLE", "IND", "DET", "CHI", "MIL",
		"MIA", "ATL", "CHO", "WAS", "ORL",
		"OKC", "POR", "UTA", "DEN", "MIN",
		"GSW", "LAC", "SAC", "PHO", "LAL",
		"SAS", "DAL", "MEM", "HOU", "NOP"
		]
	# choose a year
	year = "/2022.html"
	base_url = 'https://www.basketball-reference.com/teams/'

	for team in team_abbrev:
		# temporary team-specific table
		team_table = pd.DataFrame()
		# build url
		url = base_url+team+year
		print("--------------------------")
		print(f"Accessing {team}")
		#request access
		page = requests.get(url)
		if page.status_code != 200:
			#failed access
			print(f"Status code {page.status_code} denied access to webpage: {url}")
			exit()
		else:
			#access successful!
			print("access success")
			#page in better format for python
			soup = BeautifulSoup(page.text, 'lxml')
			
			# |||| TABLE PROCESSING ||||
			# --------------------------
			# find table based off of id
			roster = soup.find("table", id="roster")
			# get table headers, all delinated with "th", limit 6 because
			# rows are also delineated with "th"
			# ["Player", "Pos", "Ht", "Wt", "Birth Date", "Country", "Exp", "College"]
			# Ht = feet-inches, Wt = pounds, Country = country code
			headers = []
			for i in roster.find_all("th", limit=9):
				title = i.text
				if len(title) == 1:
					headers.append("Country")
				elif title == "No.":
					pass
				else:
					headers.append(title)
			# Create a temporary dataframe from headers
			team_table = pd.DataFrame(columns = headers)
			# fill the table
			# data delineated by "td", row delineated by "tr"
			for row in roster.find_all("tr")[1:]:
				row_data = row.find_all("td")
				row = [data.text for data in row_data]
				length = len(team_table)
				team_table.loc[length] = row
			master_table = pd.concat([master_table, team_table], ignore_index=True)
	return master_table

def get_nba_biometrics_table(combined_table):
	url = "https://craftednba.com/player-traits/length"
	#request access
	page = requests.get(url)
	if page.status_code != 200:
		#failed access
		print(f"Status code {page.status_code} denied access to webpage: {url}")
		exit()
	else:
		print("Access Success")
		for player in combined_table["Player"]:
			soup = BeautifulSoup(page.text, 'lxml')
			# |||| TABLE PROCESSING ||||
			# --------------------------
			# find table based off of id
			roster = soup.find("table", id="roster")
			# get table headers, all delinated with "th", limit 6 because
			# rows are also delineated with "th"
			# ["Player", "Pos", "Ht", "Wt", "Birth Date", "Country", "Exp", "College"]
			# Ht = feet-inches, Wt = pounds, Country = country code
			headers = []
			for i in roster.find_all("th", limit=9):
				title = i.text

				if len(title) == 1:
					headers.append("Country")
				elif title == "No.":
					pass
				else:
					headers.append(title)
			# Create a temporary dataframe from headers
			team_table = pd.DataFrame(columns = headers)
			print("Building team_table...")
			# fill the table
			# data delineated by "td", row delineated by "tr"
			for row in roster.find_all("tr")[1:]:
				row_data = row.find_all("td")
				row = [data.text for data in row_data]
				length = len(team_table)
				team_table.loc[length] = row

