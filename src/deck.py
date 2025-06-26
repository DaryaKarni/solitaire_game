import random
from src.card import Card
class Deck:
    def __init__(self):
        self.suits = ("Hearts", "Diamonds", "Clubs", "Spades")
        self.ranks = [i for i in range(1,14)]
        self.cards = []

    def create_deck(self):
        self.cards = []
        for suit in self.suits:
            for i in self.ranks:
                self.cards.append(Card(i, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num):
        if not isinstance(num, int) or not (1 <= num <= 52):
            raise ValueError("The number of cards to be dealt must be an integer from 1 to 52.")
        card_pile = []
        for i in range(num):
            if self.cards:
                card_pile.append(self.cards.pop())
        return card_pile
    
    def __len__(self):
        return len(self.cards)