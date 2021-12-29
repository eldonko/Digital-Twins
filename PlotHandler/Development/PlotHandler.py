import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from mysite.data_handling.Digital_Twins.TwitterDataHandler.Development.TwitterDataHandler import TwitterDataHandler
from mysite.data_handling.Digital_Twins.MatchEventHandler.Development.MatchEventHandler import MatchEventHandler


class PlotHandler:
	def __init__(self):
	    #, matches_file_path=None, match_events_file_path=None):
		#self.match_event_handler = MatchEventHandler(matches_file_path, match_events_file_path)
		#self.twitter_data_handler = TwitterDataHandler()
		self.match_event_handler = None
		self.twitter_data_handler = None

	def create_twitter_handlers(self, matches_file_path, match_events_file_path):
	    self.match_event_handler = MatchEventHandler(matches_file_path, match_events_file_path)
	    self.twitter_data_handler = TwitterDataHandler()

	def plot_keywords_in_time_range(self, keywords: list, start_time='1970-01-01', end_time='2100-01-01', show=False,
									ret=False, ax_in=None):
		"""
		Plots the number of tweets containing keyword in the specified time range
		:param keywords: list of keywords
		:param start_time: date string of the beginning of the search interval
		:param end_time: date string of the end of the search interval
		:param show: Determines if the plot should be shown
		:param ret: If True, the plot axis is returned
		:param ax_in: Can be used to add the plot to another plot
		:return: (optional) plot axis ax
		"""

		for keyword in keywords:
		    keyword_exists = True

		    if self.twitter_data_handler.data is None:
		        keyword_exists = self.twitter_data_handler.add_keyword(keyword)
		    elif keyword not in self.twitter_data_handler.data.columns.values:
			    keyword_exists = self.twitter_data_handler.add_keyword(keyword)

		    if not keyword_exists:
			    keywords.remove(keyword)

		time_range_data = self.twitter_data_handler.extract_data('all', (start_time, end_time))
		time_range_data['Time'] = time_range_data.index
		time_range_data['Time'] = pd.to_datetime(time_range_data['Time']).dt.strftime('%d.%m %H:%M')

		ax = time_range_data.plot(y=keywords, ax=ax_in)

		if show:
			plt.show()

		if ret:
			return ax

	def plot_match_with_keywords(self, keywords: list, opponent: str, date: str, only_keyword_events=False, hours_before=1,
								 hours_after=2):
		"""
		Plots the number of tweets containing keywords during a match and the match events as vertical lines
		:param keywords: list of keywords
		:param opponent: the opponent for the match to be plotted
		:param date: the date of the match to be plotted
		:param only_keyword_events: if False, all events are plotted, else only the events with players in keywords are included
		:param hours_before: number of hours before the match for which data shall be plotted
		:param hours_after: number of hours after the match for which data shall be plotted
		:return:
		"""

		# Load the match events for the match in question
		match_events = self.match_event_handler.get_match_events(opponent, date)
		print(match_events)

		# Select only the events where players in keywords are involved (if specified)
		if only_keyword_events:
			match_events = match_events[(match_events['Player 1'].isin(keywords)) | (match_events['Player 2'].isin(keywords))]

			print(match_events)

		# Get the start time of the match# Convert the date string to pandas datetime format
		date_dt = pd.to_datetime(date)
		match_events['Time stamp'] = pd.DatetimeIndex(match_events['Time stamp'], tz='Europe/Vienna').tz_convert(None)
		kick_off_time = match_events['Time stamp'].iloc[0]

		# Set the interval for which the data should be plotted
		start_time = date_dt.replace(hour=kick_off_time.hour - hours_before, minute=kick_off_time.minute)
		end_time = date_dt.replace(hour=kick_off_time.hour + 2, minute=kick_off_time.minute)

		# Get the keywords plot
		ax = self.plot_keywords_in_time_range(keywords, start_time=start_time, end_time=end_time, ret=True)

		# Draw a vertical line for the kick off time
		ax.axvline(date_dt.replace(hour=kick_off_time.hour, minute=kick_off_time.minute), color='r', linestyle=':')

		for time in match_events['Time stamp']:
			ax.axvline(time, color='k', linestyle='--')

		#plt.show()
		return ax
