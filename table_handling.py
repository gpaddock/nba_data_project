import pandas as pd
import requests
from bs4 import BeautifulSoup
import sys

#import tables
nba_bios = pd.read_csv("22_player_bio.csv")
nba_stats = pd.read_csv("22_player_stats.csv")
if(len(nba_bios)==0) or (len(nba_stats)==0):
	print("Error reading tables")
	exit()

#reindex on "Player" for ease of joining tables
player_bios = nba_bios.set_index("Player")
player_stats = nba_stats.set_index("Player")

#merge on player name
combined_table = nba_bios.merge(nba_stats, on="Player")
#drop duplicates (only players who were traded during season have multiple entries)
#keeps their total statistics row, but their team is labeled as TOT
print(combined_table.reset_index().head(10))
print("-----------------------------------")
#write changes
combined_table = combined_table.reset_index().drop_duplicates(subset="Player")
print(combined_table)

# get wingspans for every player in this table
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


#write file
combined_table.to_csv("22_player_complete.csv", index=False)