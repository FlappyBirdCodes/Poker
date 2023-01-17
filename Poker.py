# Oscar(Tsz Kit) Law 300306180

import random
import itertools

class Poker():

	def __init__(self, players=2):
		
		# Creates all cards in a deck and shuffles them
		self.deck = []
		for rank in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]:
			self.deck.append(rank + "D")
			self.deck.append(rank + "C")
			self.deck.append(rank + "S")
			self.deck.append(rank + "H")
		random.shuffle(self.deck)

		# Creates an empty list of cards for each player
		self.player_cards = []
		for i in range(players):
			self.player_cards.append([])

		# Creates an empty list of cards on the table
		self.table = []

	# Adds top card off the deck to the hand of a certain player
	def add_to_hand(self, index):
		self.player_cards[index].append(self.deck[0])
		self.deck.pop(0)

	def add_to_table(self):
		self.table.append(self.deck[0])
		self.deck.pop(0)

	# Changes special characters such as "T, J, Q and K" into numerical values
	def numerizeSpecialCharacters(self, ranks, character, number):
		while character in ranks:
			ranks.remove(character)
			ranks.append(number)
		return ranks

	def ranksInOrder(self, ranks):
		ranks = self.numerizeSpecialCharacters(ranks, "T", "10")
		ranks = self.numerizeSpecialCharacters(ranks, "J", "11")
		ranks = self.numerizeSpecialCharacters(ranks, "Q", "12")
		ranks = self.numerizeSpecialCharacters(ranks, "K", "13")

		if "A" in ranks and "2" in ranks and "3" in ranks and "4" in ranks and "5" in ranks:
			return True

		ranks = self.numerizeSpecialCharacters(ranks, "A", "14")
		ranks = sorted([int(rank) for rank in ranks])
			
		if ranks == list(range(ranks[0], ranks[-1] + 1)):
			return True
		return False

	def IsStraightFlush(self, draw):
		ranks = [card[0] for card in draw]
		suits = [card[1] for card in draw]

		# Checks if all cards are from the same suit
		if suits.count(suits[0]) == len(suits):

			if self.ranksInOrder(ranks):
				return True
			return False
		return False

	def IsFourofaKind(self, draw):
		ranks = [card[0] for card in draw]
		for rank in ranks:
			if ranks.count(rank) == 4:
				return True
		return False

	def IsFullHouse(self, draw):
		ranks = [card[0] for card in draw]
		for rank in ranks:
			if ranks.count(rank) == 3:
				for i in range(3):
					ranks.remove(rank)
				if ranks.count(ranks[0]) == 2:
					return True
				return False
		return False

	def IsFlush(self, draw):
		suits = [card[1] for card in draw]
		if suits.count(suits[0]) == 5:
			return True
		return False

	def IsStraight(self, draw):
		ranks = [card[0] for card in draw]
		if self.ranksInOrder(ranks):
			return True
		return False

	def IsThreeofaKind(self, draw):
		ranks = [card[0] for card in draw]
		for rank in ranks:
			if ranks.count(rank) == 3:
				return True
		return False

	def IsTwoPairs(self, draw):
		ranks = [card[0] for card in draw]
		firstPair = False

		for rank in ranks:
			if ranks.count(rank) == 2:
				firstPair = True
				for i in range(2):
					ranks.remove(rank)
				break

		if firstPair:
			for rank in ranks:
				if ranks.count(rank) == 2:
					return True
			return False

		return False

	def IsOnePair(self, draw):
		ranks = [card[0] for card in draw]
		for rank in ranks:
			if ranks.count(rank) == 2:
				return True
		return False

	def checkRankings(self, card_combinations):
		possible_rankings = []

		for combination in card_combinations:
			if self.IsStraightFlush(combination) and 8 not in possible_rankings:
				possible_rankings.append(8)

			elif self.IsFourofaKind(combination) and 7 not in possible_rankings:
				possible_rankings.append(7)				

			elif self.IsFullHouse(combination) and 6 not in possible_rankings:
				possible_rankings.append(6)

			elif self.IsFlush(combination) and 5 not in possible_rankings:
				possible_rankings.append(5)

			elif self.IsStraight(combination) and 4 not in possible_rankings:
				possible_rankings.append(4)

			elif self.IsThreeofaKind(combination) and 3 not in possible_rankings:
				possible_rankings.append(3)

			elif self.IsTwoPairs(combination) and 2 not in possible_rankings:
				possible_rankings.append(2)

			elif self.IsOnePair(combination) and 1 not in possible_rankings:
				possible_rankings.append(1)
			else:
				possible_rankings.append(0)
		return possible_rankings

class TexasHoldem(Poker):

	def __init__(self, players=2):
		super().__init__(players)

	def deal(self):
		# Deals 2 cards to the hand of each player
		for i in range(len(self.player_cards)):
			for e in range(2):
				self.add_to_hand(i)

		# Deals 5 cards on the table
		for j in range(5):
			self.add_to_table()

	def hands(self):
		return self.player_cards

	def solve(self):
		best_rankings = []

		for player in self.player_cards:
			all_cards = player + self.table
			card_combinations = list(itertools.combinations(all_cards, 5))
			possible_rankings = self.checkRankings(card_combinations)

			rankings = {
				8: "Straight Flush",
				7: "Four of a Kind",
				6: "Full House",
				5: "Flush",
				4: "Straight",
				3: "Three of a Kind",
				2: "Two Pairs",
				1: "One Pair",
				0: "High Card"
			}
			best_ranking = rankings[max(possible_rankings)]
			best_rankings.append(best_ranking)

		return best_rankings


class OmahaHoldem(Poker):

	def __init__(self, players=2):
		super().__init__(players)

	def deal(self):
		# Deals 4 cards to the hand of each player
		for i in range(len(self.player_cards)):
			for e in range(4):
				self.add_to_hand(i)

		# Deals 5 cards on the table
		for j in range(5):
			self.add_to_table()

	def hands(self):
		return self.player_cards

	def solve(self):
		best_rankings = []

		for player in self.player_cards:
			handChoices = list(itertools.combinations(player, 2))
			tableChoices = list(itertools.combinations(self.table, 3))

			all_combinations = []
			for hand in handChoices:
			    for table in tableChoices:
			        all_combinations.append(hand + table)
			possible_rankings = self.checkRankings(all_combinations)

			rankings = {
				8: "Straight Flush",
				7: "Four of a Kind",
				6: "Full House",
				5: "Flush",
				4: "Straight",
				3: "Three of a Kind",
				2: "Two Pairs",
				1: "One Pair",
				0: "High Card"
			}
			best_ranking = rankings[max(possible_rankings)]
			best_rankings.append(best_ranking)
		return best_rankings

def displayResults(game, version):
	print(version)
	game.deal()
	print("Player hands: ", end="")
	print(game.hands())
	print("Table: ", end="")
	print(game.table)
	print("Best rankings: ", end="")
	print(game.solve())

texasHoldem = TexasHoldem()
displayResults(texasHoldem, "Texas Holdem Simulation")
print("")
omahaHoldem = OmahaHoldem()
displayResults(omahaHoldem, "Omaha Holdem Simulation")