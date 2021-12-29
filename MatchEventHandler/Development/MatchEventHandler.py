import pandas as pd
import os


<<<<<<< HEAD
class MatchEventHandler:
	def __init__(self, matches_file_path=None, match_events_file_path=None):
		if matches_file_path is None:
			self.matches_file_path = r"C:/Users/danie/Documents/Montanuni/2021_22WS/Digital Twins/4 Data/Matches/Matches.xls"
=======
class MatchEventHandler: 
	def __init__(self, matches_file_path=None, match_events_file_path=None):
		if matches_file_path is None:
			self.matches_file_path = r"C:\Users\danie\Documents\Montanuni\2021_22WS\Digital Twins\4 Data\Matches\Matches.xls"
>>>>>>> 8d295a758751064cb6af81da20c50c44bf384b17
		else:
			self.matches_file_path = matches_file_path

		if match_events_file_path is None:
<<<<<<< HEAD
			self.match_events_file_path = r"C:/Users/danie/Documents/Montanuni/2021_22WS/Digital Twins/4 Data/Match Events"
=======
			self.match_events_file_path = r"C:\Users\danie\Documents\Montanuni\2021_22WS\Digital Twins\4 Data\Match Events"
>>>>>>> 8d295a758751064cb6af81da20c50c44bf384b17
		else:
			self.match_events_file_path = match_events_file_path

		self.matches = None # All possible matches
		self.match = None # The match the match event data has been loaded for
		self.match_events = None # The match events of a certain match

		self.load_matches()

	def load_matches(self):
		"""
		Loads all matches from an excel sheet located in self.matches_file_path
		:return:
		"""
		self.matches = pd.read_excel(self.matches_file_path)

	def load_match_events(self, opponent: str, date: str):
		"""
		Loads the match events of a certain match, which is  specified by the opponent and the date it occurred
		:param opponent: name of the opponent
		:param date: date the match occured
		:return:
		"""

		# Input checking
		if opponent is None or date is None:
			raise ValueError('Opponent and date must be specified')

		# Set match
		match_data = self.matches[(self.matches['Opponent'] == opponent) & (self.matches['Date'] == date)]
		time = match_data['Time']
		result = match_data['Result']
		self.match = {'Opponent': opponent, 'Date': date, 'Time': time, 'Result': result}

		# If opponent has an empty string ' ' in it, replace it with '-'
		opponent = opponent.replace(' ', '-')

		# Create filename
		date = date.split('-')
		filename = opponent + '_' + date[2] + '_' + date[1] + '_' + date[0] + '.xls'

		self.match_events = pd.read_excel(os.path.join(self.match_events_file_path, filename))

	def get_match_events(self, opponent: str, date: str):
		"""
		Loads and returns the match events of the match specified using opponent and date
		:param opponent: name of the opponent
		:param date: date the match occured
		:return: pandas DataFrame containing the match event data
		"""

		self.load_match_events(opponent, date)
		return self.match_events