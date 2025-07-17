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
        game_instance.deck = mock_deck_instance
        yield mock_deck_instance

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


      