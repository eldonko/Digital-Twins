from PlotHandler.Development.PlotHandler import PlotHandler


def main():
	ph = PlotHandler()
	ph.create_handlers(r"C:\Users\danie\Documents\Montanuni\2021_22WS\Digital Twins\4 Data\Matches\Matches.xls", r"C:\Users\danie\Documents\Montanuni\2021_22WS\Digital Twins\4 Data\Match Events")
	#ax = ph.plot_keywords_in_time_range(['Ronaldo', 'Fernandes'], start_time='2021-11-26', ret=True)
	#ph.plot_keywords_in_time_range(['Rangnick', 'Cavani'], start_time='2021-11-26', show=True, ax_in=ax)

	#ph.plot_match_with_keywords(['Ronaldo', 'Fernandes'], 'Atalanta Bergamo', '2021-10-20', only_keyword_events=False)
	ph.plot_google_trends_data(['Ronaldo', 'Fernandes'], start_time='2021-10-18', end_time='2022-01-17', show_matches=True)


if __name__ == '__main__':
	main()