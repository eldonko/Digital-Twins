import pandas as pd
import glob
import os


class TwitterDataHandler:
	def __init__(self):
		self.data = None
		self.data_keyword = None

		self.data_location = r"C:\Users\danie\Documents\Montanuni\2021_22WS\Digital Twins\4 Data"

		# Define errors
		self.errors = {'PLT_1': '*** PLT_1 *** Data could not be plotted. Please specify only keys which are actually in the data!',
					   'PLT_2': '*** PLT_2 *** Data could not be plotted. Please pass \'all\' or a list for columns',
					   'NO_DATA_1': '*** NO_DATA_1 *** No data has been loaded yet. Please load data before calling functions on it'}

	def add_keyword(self, keyword: str):
		"""
		Reads all files for a certain keyword into self.data
		:param keyword: string, which defines the csv file to load
		:return:
		"""

		# Load all the files containing the keyword into the data directory
		files = [x for x in glob.glob(os.path.join(self.data_location, '*.csv')) if keyword in x]

		# Read all the files into self.data
		for file in files:
			self.read_file(file, keyword)

		# Add the data obtained to self.data
		if self.data is None:
			self.data = self.data_keyword
		else:
			self.data = self.data.join(self.data_keyword)

		# Reset the temporary global DataFrame
		self.data_keyword = None

		# Sort the data by the index
		self.data.sort_index(0)

	def read_file(self, filename, keyword):
		"""
		Reads the data from a file and appends the data to a temporary global DataFrame, from which it is
		later appended to the general global DataFrame.
		:param filename: the filename of the file to open
		:param keyword: the keyword to look for
		:return:
		"""
		# Read the file
		data_file = pd.read_csv(filename)[['end', 'start', 'tweet_count']]

		# Sort the file by the start date
		data_file = data_file.sort_values(by=['start'])

		# Drop rows which contain the CSV header
		data_file = data_file[~(data_file['start'] == 'start')]

		# Drop column 'end' as the information in it is redundant
		data_file = data_file[['start', 'tweet_count']]

		data_file['start'] = pd.to_datetime(data_file['start'])

		# Set the time information as the index
		data_file = data_file.set_index(['start'])

		# Cast the tweet count Series to integer
		data_file['tweet_count'] = data_file['tweet_count'].astype('int32')

		# Rename column tweet_count to the keyword
		data_file = data_file.rename(columns={'tweet_count': keyword})

		# Keep the data from the file
		if self.data_keyword is None:
			self.data_keyword = data_file
		else:
			self.data_keyword = self.data_keyword.append(data_file)

	def extract_data(self, columns=None, time_range=None):
		"""
		Extracts data from specified columns and time range and returns it
		:param columns: columns to be contained in the returned DataFrame
		:param time_range: (optional) a time interval which can be used to only plot data from a specific time range.
				time_range is a tuple like (start_date, end_date)
		:return: DataFrame only containing specified by columns and time_range
		"""

		# Check if data has been loaded
		self.no_data()

		# Copy the DataFrame
		data = self.data

		# Convert time_range to str if it is Timestamp
		if type(time_range[0]) == pd.Timestamp:
			time_range = (str(time_range[0]), str(time_range[1]))

		# Extract the time range if one is specified
		if time_range is not None:
			# Check input
			assert type(time_range) == tuple
			assert len(time_range) == 2

			# Extract the time range
			data = data[data.index >= time_range[0]]
			data = data[data.index <= time_range[1]]

		# Get all columns
		if columns == 'all' or columns is None:
			return data
		# Plot only selected columns
		elif type(columns) == list:
			return data[columns]

	def plot_data(self, columns=None, time_range=None):
		"""
		Plots the data in self.data
		:param columns: A list of the columns (specified by the keyword) to plot. If columns is 'all', all
		columns shall be plotted
		:param time_range: (optional) a time interval which can be used to only plot data from a specific time range.
				time_range is a tuple like (start_date, end_date)
		:return:
		"""

		data = self.extract_data(columns, time_range)

		try:
			data.plot(y=columns, grid=True)
		except:
			print('Possible keys: ', data.columns.values)
			raise ValueError(self.errors['PLT_1'])

	def no_data(self):
		"""
		Checks if data has been loaded and raises an exception if not. Is called at the beginning of any function
		which calls functions on data.
		:return:
		"""
		if self.data is None:
			raise Exception(self.errors['NO_DATA_1'])
