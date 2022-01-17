import matplotlib.pyplot as plt
import pandas as pd
from TwitterDataHandler.Development.TwitterDataHandler import TwitterDataHandler
from MatchEventHandler.Development.MatchEventHandler import MatchEventHandler
from GoogleTrendsHandler.Development.GoogleTrendsHandler import GoogleTrendsHandler


class PlotHandler:
    def __init__(self):
        # , matches_file_path=None, match_events_file_path=None):
        # self.match_event_handler = MatchEventHandler(matches_file_path, match_events_file_path)
        # self.twitter_data_handler = TwitterDataHandler()
        self.match_event_handler = None
        self.twitter_data_handler = None
        self.google_trends_handler = None

    def create_handlers(self, matches_file_path, match_events_file_path):
        self.match_event_handler = MatchEventHandler(matches_file_path, match_events_file_path)
        self.twitter_data_handler = TwitterDataHandler()
        self.google_trends_handler = GoogleTrendsHandler()

    def plot_keywords_in_time_range(self, keywords: list, start_time='1970-01-01', end_time='2100-01-01', show=False,
									ret=False, ax_in=None, plot_matches=False):
		"""
		Plots the number of tweets containing keyword in the specified time range
		:param keywords: list of keywords
		:param start_time: date string of the beginning of the search interval
		:param end_time: date string of the end of the search interval
		:param show: Determines if the plot should be shown
		:param ret: If True, the plot axis is returned
		:param ax_in: Can be used to add the plot to another plot
		:param plot_matches: if vertical lines for matches should be plotted

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

		ax = time_range_data.plot(y=keywords, ax=ax_in, figsize=(13, 7))

		if plot_matches:
		    matches = self.match_event_handler.matches

		    for i in range(len(matches)):
		        datetime = matches.iloc[i]['Datetime']
		        result = matches.iloc[i]['Result']
		        result = result.split(':')

		        c = ''

		        if result[0] > result[1]:
		            c = 'g'
		        elif result[0] < result[1]:
		            c = 'r'
		        else:
		            c = 'y'

		        ax.axvline(datetime, color=c, alpha=0.5)

		plt.xlabel('Time')
		plt.xlabel('# of tweets')
		plt.title('Number of tweets containing keywords during a Manchester United match')
		plt.grid()

		if show:
			plt.show()

		if ret:
			return ax

    def plot_match_with_keywords(self, keywords: list, opponent: str, date: str, only_keyword_events=False,
                                 hours_before=1,
                                 hours_after=1):
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
        self.match_events = self.match_event_handler.get_match_events(opponent, date)

        # Select only the events where players in keywords are involved (if specified)
        if only_keyword_events:
            self.match_events = self.match_events[
                (self.match_events['Player 1'].isin(keywords)) | (self.match_events['Player 2'].isin(keywords))]

        # Get the start time of the match# Convert the date string to pandas datetime format
        date_dt = pd.to_datetime(date)
        self.match_events['Time stamp'] = pd.DatetimeIndex(self.match_events['Time stamp'],
                                                           tz='Europe/Vienna').tz_convert(None)
        kick_off_time = self.match_events['Time stamp'].iloc[0]
        full_time = self.match_events['Time stamp'].iloc[-1]

        # Set the interval for which the data should be plotted
        start_time = date_dt.replace(hour=kick_off_time.hour - hours_before, minute=kick_off_time.minute)
        end_time = date_dt.replace(hour=(full_time + pd.Timedelta(str(hours_after) + ' hours')).hour,
                                   minute=full_time.minute)

        # Get the keywords plot
        ax = self.plot_keywords_in_time_range(keywords, start_time=start_time, end_time=end_time, ret=True)

        for i in range(len(self.match_events)):
            time = self.match_events.iloc[i]['Time stamp']
            event = self.match_events.iloc[i]['Event']
            team = self.match_events.iloc[i]['Team']
            if event == 'Kick-off' or event == 'Half-time' or event == 'Full-time' or event == 'Second-half':
                ax.axvline(time, color='k')
            elif event == 'Goal' and team == 'United':
                ax.axvline(time, color='g', linestyle='--')
            elif event == 'Goal' and team != 'United':
                ax.axvline(time, color='b', linestyle='--')
            elif event == 'Yellow':
                ax.axvline(time, color='y', linestyle=':')
            elif event == 'Second Yellow' or event == 'Red':
                ax.axvline(time, color='r', linestyle=':')
            elif event == 'Sub':
                ax.axvline(time, color='orange', linestyle='-.')

        # plt.show()
        return ax

    def plot_stock_data(self, stock_data):
        matches = self.match_event_handler.matches
        ax = stock_data.plot(y='close', figsize=(13, 7))
        plt.grid()

        for i in range(len(matches)):
            datetime = matches.iloc[i]['Datetime']
            result = matches.iloc[i]['Result']
            result = result.split(':')

            c = ''

            if result[0] > result[1]:
                c = 'g'
            elif result[0] < result[1]:
                c = 'r'
            else:
                c = 'y'

            ax.axvline(datetime, color=c)

        return ax

    def plot_google_trends_data(self, keywords: list, start_time='1970-01-01', end_time='2100-01-01', show_matches=False):
        self.google_trends_handler.get_google_trends_data(keywords, start_time, end_time)

        ax = self.google_trends_handler.data.plot(y=keywords)

        if show_matches:
            matches = self.match_event_handler.matches

            for i in range(len(matches)):
                datetime = matches.iloc[i]['Datetime']
                result = matches.iloc[i]['Result']
                result = result.split(':')

                c = ''

                if result[0] > result[1]:
                    c = 'g'
                elif result[0] < result[1]:
                    c = 'r'
                else:
                    c = 'y'

                ax.axvline(datetime, color=c, alpha=0.5)

        return ax
