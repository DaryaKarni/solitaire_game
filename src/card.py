class Card:
    VALID_RANKS = range(1,14)
    VALID_SUITS = ("Hearts", "Diamonds", "Clubs", "Spades")
    def __init__(self, rank, suit):
        if rank not in self.VALID_RANKS:
            raise ValueError("Rank of card must be in range of 1 to 13")
        if suit not in self.VALID_SUITS:
            raise ValueError("Suit of card must be in range of valid suits")
        self.rank = rank
        self.suit = suit
        self.is_face_up = False
    def flip(self):
        self.is_face_up = not self.is_face_up
    def __str__(self):
        return f"{self.rank} {self.suit}"    
