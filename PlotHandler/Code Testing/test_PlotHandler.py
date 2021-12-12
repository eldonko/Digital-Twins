from PlotHandler.Development.PlotHandler import PlotHandler


def main():
	ph = PlotHandler()
	#ax = ph.plot_keywords_in_time_range(['Ronaldo', 'Fernandes'], start_time='2021-11-26', ret=True)
	#ph.plot_keywords_in_time_range(['Rangnick', 'Cavani'], start_time='2021-11-26', show=True, ax_in=ax)

	ph.plot_match_with_keywords(['Ronaldo', 'Fernandes'], 'Atalanta Bergamo', '2021-10-20', only_keyword_events=False)


if __name__ == '__main__':
	main()