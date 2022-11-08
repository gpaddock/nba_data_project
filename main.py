#import table_handling
from scrape_nba import *
import pandas as pd

if __name__ == "__main__":
	biometric_table = get_nba_biometrics_table(combined_table)
	print(biometric_table)