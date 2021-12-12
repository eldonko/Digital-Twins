from MatchEventHandler.Development.MatchEventHandler import MatchEventHandler


def main():
	meh = MatchEventHandler()
	print(meh.get_match_events('Atalanta Bergamo', '2021-10-20'))


if __name__ == '__main__':
	main()