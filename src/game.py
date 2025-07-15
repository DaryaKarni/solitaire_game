from deck import Deck
from card import Card
class Game:
    def __init__(self):
        self.deck = Deck()
        self.foundations = [[] for i in range(4)]
        self.tableau = [[] for i in range(7)]
        self.reserve = []
        self.waste = []
        self.initialize_game()

    def initialize_game(self):
        self.deck.create_deck()
        self.deck.shuffle()
        for i in range(7):
            self.tableau[i] = self.deck.deal(i + 1)
            self.tableau[i][-1].is_face_up = True

        self.reserve = self.deck.deal(len(self.deck))

    def open_reserve_card(self):
        if self.reserve:
            card = self.reserve.pop()
            card.is_face_up = True
            self.waste.append(card)
        elif self.waste:
            while self.waste:
                card = self.waste.pop()
                card.is_face_up = False
                self.reserve.append(card)

    @staticmethod
    def is_card_compatible_tableau(card, to_card):
        if card.is_red == to_card.is_red or card.rank - to_card.rank != -1:
            return False
        else:
            return True
        
    def king_to_empty_stack(self, card, target_stack):
        if not target_stack:
            return card.rank == 13
        
    def move_from_waste_to_tableau(self, to_tableau_index):
        if not self.waste:
            return False
        card = self.waste[-1]
        target_stack = self.tableau[to_tableau_index]
        can_move = False
        if not target_stack:
            can_move = (card.rank == 13)
        else:
            can_move = self.is_card_compatible_tableau(card, target_stack[-1])    
        if can_move:
            target_stack.append(card)
            self.waste.pop()
            return True
        else:
            return False
        
    def move_from_tableau_to_tableau(self, from_tableau_index, card, to_tableau_index):
        start_stack = self.tableau[from_tableau_index]
        target_stack = self.tableau[to_tableau_index]
        if not target_stack:
            can_move = (card.rank == 13)
        else:
            can_move = self.is_card_compatible_tableau(card, target_stack[-1])
        if can_move:
            card_index_in_source = start_stack.index(card)
            cards_to_move = start_stack[card_index_in_source:]
            target_stack.extend(cards_to_move)
            del start_stack[card_index_in_source:]
            if start_stack:
                start_stack[-1].is_face_up = True
            return True
        else:
            return False
    #def move_from_tableau_to_foundations():
    #def move_from_foundations_to_tableau():


