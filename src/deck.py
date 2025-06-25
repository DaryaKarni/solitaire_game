import random
from src.card import Card
class Deck:
    def __init__(self):
        self.suits = ("Hearts", "Diamons", "Clubs", "Spades")
        self.ranks = [i for i in range(1,14)]
        self.cards = []
    def create_deck(self):
        for suit in self.suits:
            for i in self.ranks:
                self.cards.append(Card(i, suit))
    def shuffle(self):
        random.shuffle(self.cards)
    def deal(self, num):
        card_pile = []
        for i in range(num):
            if self.cards:
                card_pile.append(self.cards.pop())
        return card_pile