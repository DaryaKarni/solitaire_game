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
    def _is_card_compatible_tableau(card, to_card):
        if card.is_red() == to_card.is_red() or card.rank - to_card.rank != -1:
            return False
        else:
            return True
        
    def _can_move_to_tableau(self, card, to_tableau_index):
        target_stack = self.tableau[to_tableau_index]
        can_move = False
        if not target_stack:
            can_move = (card.rank == 13)
        else:
            can_move = self._is_card_compatible_tableau(card, target_stack[-1])
        return can_move
    
    def _can_move_to_foundations(self, card, to_foundation_index):
        to_stack = self.foundations[to_foundation_index]
        can_move = False
        if Card.VALID_SUITS[to_foundation_index] == card.suit:
            if not to_stack and card.rank == 1:
                can_move = True
            elif to_stack and to_stack[-1].rank - card.rank == -1:
                can_move = True
        return can_move
    
    def move_from_waste_to_tableau(self, to_tableau_index):
        if not self.waste:
            return False
        card = self.waste[-1]
        can_move = self._can_move_to_tableau(card, to_tableau_index)
        if can_move:
            self.tableau[to_tableau_index].append(card)
            self.waste.pop()
            return True
        else:
            return False
        
    def move_from_tableau_to_tableau(self, from_tableau_index, card, to_tableau_index):
        start_stack = self.tableau[from_tableau_index]
        if not start_stack:
            return False
        for card in start_stack[card_index_in_source:]:
            if not card.is_face_up:
                return False
        can_move = self._can_move_to_tableau(card, to_tableau_index)
        if can_move:
            card_index_in_source = start_stack.index(card)
            cards_to_move = start_stack[card_index_in_source:]
            self.tableau[to_tableau_index].extend(cards_to_move)
            del start_stack[card_index_in_source:]
            if start_stack:
                start_stack[-1].is_face_up = True
            return True
        else:
            return False
        
    def move_from_tableau_to_foundations(self, from_tableau_index, to_foundation_index):
        from_stack = self.tableau[from_tableau_index]
        if not from_stack:
            return False
        to_stack = self.foundations[to_foundation_index]
        card = from_stack[-1]

        can_move = self._can_move_to_foundations(card, to_foundation_index)
        if can_move:
            to_stack.append(card)
            from_stack.pop()
            if from_stack:
                from_stack[-1].is_face_up = True
            return True
        else:
            return False

    def move_from_foundations_to_tableau(self, from_foundations_index, to_tableau_index):
        to_stack = self.tableau[to_tableau_index]
        from_stack =  self.foundations[from_foundations_index]
        if not from_stack:
            return False
        card = from_stack[-1]
        can_move = self._can_move_to_tableau(card, to_tableau_index)
        if can_move:
            to_stack.append(card)
            from_stack.pop()
            return True
        else:
            return False
    def move_from_waste_to_foundations(self, to_foundations_index):
        if not self.waste:
            return False
        card = self.waste[-1]
        can_move = self._can_move_to_foundations(card, to_foundations_index)
        if can_move:
            self.foundations[to_foundations_index].append(card)
            self.waste.pop()
            return True
        else:
            return False


