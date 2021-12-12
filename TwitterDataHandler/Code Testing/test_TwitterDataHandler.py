from TwitterDataHandler.Development.TwitterDataHandler import TwitterDataHandler
import matplotlib.pyplot as plt


def main():
	twd = TwitterDataHandler()

	twd.add_keyword('Ronaldo')
	twd.add_keyword('Rashford')
	twd.add_keyword('Fernandes')
	twd.add_keyword('Solskjaer')
	twd.add_keyword('Zidane')
	twd.add_keyword('Carrick')
	twd.add_keyword('Rangnick')

	twd.plot_data(['Solskjaer', 'Zidane', 'Carrick', 'Rangnick'])
	twd.plot_data()

	plt.show()


if __name__ == '__main__':
	main()
