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
      