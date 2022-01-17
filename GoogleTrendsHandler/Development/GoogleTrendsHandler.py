from pytrends.request import TrendReq
import pandas as pd


class GoogleTrendsHandler: 
	def __init__(self):
		self.pytrends = TrendReq(hl='en-US', tz=0)

		# Define data
		self.data = None

	def get_google_trends_data(self, keywords: list, start_time='1970-01-01', end_time='2100-01-01'):
		timeframe = start_time + ' ' + end_time

		for key in keywords:
			self.pytrends.build_payload([key], cat=0, timeframe=timeframe)

			# Get the data for the keyword
			data = self.pytrends.interest_over_time()

			if self.data is None:
				self.data = pd.DataFrame(data[key])
			else:
				self.data = self.data.join(pd.DataFrame(data[key]))
