import pytest 
from src.game import Game
from src.deck import Deck
from src.card import Card
from unittest.mock import MagicMock, patch

@pytest.fixture
def mock_deck():
    with patch('src.game.Deck') as MockDeck:
        mock_deck_instance = MockDeck.return_value
        all_cards = []

    for suit in Card.VALID_SUITS:
        for rank in Card.VALID_RANKS:
            all_cards.append(Card(rank, suit))

    def side_effect_deal(num):
        dealt_cards = all_cards[:num]
        del all_cards[:num]
        return dealt_cards
    
    mock_deck_instance.deal.side_effect = side_effect_deal
    mock_deck_instance.__len__.return_value = len(all_cards)

    yield mock_deck_instance

@pytest.fixture
def game(mock_deck):
    return Game()

@pytest.fixture
def custom_game():
    with patch('src.game.Deck') as MockDeck:
        mock_deck_instance = MockDeck.return_value
        game_instance = Game()
        yield game_instance

class TestGameInitialization:
    def test_initialization_tableau_counts_and_face_up(self, game):
        expected_counts = range(1,8)
        total_tableau_cards = 0
        for i, count in enumerate(expected_counts):
            assert len(game.tableau[i]) == count, "Invalid amount of cards in tableau stacks"
            total_tableau_cards += count
            assert game.tableau[i][-1].is_face_up is True, "Last card of tableau stack must be face up"
            for card in game.tableau[i][:-1]:
                assert card.is_face_up is False, "All cards except the last one must be face down"

        assert total_tableau_cards == 28, "Invalid amount of total tableau cards"  

    def test_initialization_reserve_and_waste(self, game):
        assert len(game.reserve) == 24, "Invalid reserve length"
        for card in game.reserve:
            assert card.is_face_up == False, "Reserve cards must be face down"
        assert len(game.waste) == 0, "Waste length must be 0"

    def test_initialization_foundations(self, game):
        for foundation in game.foundations:
            assert len(foundation) == 0, "Foundation length must be 0"

class TestOpenReserveCard:
    def test_open_reserve_card_moves_to_waste(self, custom_game):
        custom_game.reserve = [Card(10, "Spades", is_face_up=False), Card(5, "Diamonds", is_face_up=False)]
        custom_game.waste = []

        initial_reserve_len = len(custom_game.reserve)
        initial_waste_len = len(custom_game.waste)
        card_to_move = custom_game.reserve[-1]

        custom_game.open_reserve_card()

        assert len(custom_game.reserve) == initial_reserve_len - 1
        assert len(custom_game.waste) == initial_waste_len + 1
        assert custom_game.waste[-1] == card_to_move
        assert custom_game.waste[-1].is_face_up == True

    def test_open_reserve_card_recycles_waste_to_reserve(self, custom_game):
        custom_game.reserve = []
        custom_game.waste = [Card(7, "Clubs", is_face_up=True), Card(4, "Hearts", is_face_up=True)]

        initial_waste_cards = list(custom_game.waste)
        custom_game.open_reserve_card()

        assert custom_game.reserve[0] == initial_waste_cards[1]
        assert custom_game.reserve[1] == initial_waste_cards[0]
        assert len(custom_game.reserve) == len(initial_waste_cards)
        assert len(custom_game.waste) == 0

        for card in custom_game.reserve:
            assert card.is_face_up == False

    def test_open_reserve_card_both_empty(self, custom_game):
        custom_game.reserve = []
        custom_game.waste = []

        custom_game.open_reserve_card()

        assert len(custom_game.reserve) == 0
        assert len(custom_game.waste) == 0