import pytest
from src.card import Card
from src.deck import Deck

def test_deck_initialization():
    deck = Deck()
    assert len(deck.cards) == 52, "Deck contain 52 cards upon initialization."
    temp_deck = Deck()
    temp_deck.create_deck()
    assert deck.cards != temp_deck.cards, "Shuffled stack must differ from unshuffled"
    
def test_create_deck():
    deck = Deck()
    deck.create_deck()
    assert len(deck.cards) == 52, "Deck should contain 52 cards after creation."

    card_strings = set(str(card) for card in deck.cards)
    assert len(card_strings) == 52, "All cards in the deck must be unique."

    expected_cards = set()
    for suit in deck.suits:
        for rank in deck.ranks:
            expected_cards.add(f"{rank} {suit}")
    
    for card in deck.cards:
        assert f"{card.rank} {card.suit}" in expected_cards, f"Unexpected card in the deck: {card.rank} {card.suit}"

def test_shuffle():
    deck = Deck()
    deck.create_deck()
    original_order = list(deck.cards)

    deck.shuffle()
    shuffled_order = deck.cards

    assert shuffled_order != original_order, "The deck should be shuffled."
    
    assert len(shuffled_order) == 52, "The number of cards should not change after shuffling."
    assert all(card in original_order for card in shuffled_order) and \
           all(card in shuffled_order for card in original_order), \
           "The shuffled deck should contain the same cards as the original."


def test_deal_single_card():
 
    deck = Deck()
    deck.create_deck()
    initial_len = len(deck)
    
    dealt_cards = deck.deal(1)
    assert len(dealt_cards) == 1, "Exactly one card should be dealt."
    assert isinstance(dealt_cards[0], Card), "The dealt item must be an instance of Card."
    assert len(deck) == initial_len - 1, "The number of cards in the deck should decrease by 1."

def test_deal_multiple_cards():
    deck = Deck()
    deck.create_deck()
    initial_len = len(deck)
    
    num_to_deal = 5
    dealt_cards = deck.deal(num_to_deal)
    assert len(dealt_cards) == num_to_deal, f"Exactly {num_to_deal} cards should be dealt."
    assert len(deck) == initial_len - num_to_deal, f"The number of cards in the deck should decrease by {num_to_deal}."
    for card in dealt_cards:
        assert isinstance(card, Card), "All dealt items must be instances of Card."

def test_deal_more_cards_than_available():
    deck = Deck()
    deck.create_deck()
    
    dealt_cards = deck.deal(52)
    assert len(dealt_cards) == 52, "All 52 cards should be dealt."
    assert len(deck) == 0, "The deck should be empty after dealing all cards."

    # Attempt to deal cards from an empty deck
    dealt_cards_from_empty = deck.deal(1)
    assert len(dealt_cards_from_empty) == 0, "No cards should be dealt from an empty deck."
    assert len(deck) == 0, "The deck should remain empty."

def test_deal_invalid_number_raises_valueerror():
    deck = Deck()
    deck.create_deck()

    with pytest.raises(ValueError, match="The number of cards to be dealt must be an integer from 1 to 52."):
        deck.deal(0) 

    with pytest.raises(ValueError, match="The number of cards to be dealt must be an integer from 1 to 52."):
        deck.deal(53) 

    with pytest.raises(ValueError, match="The number of cards to be dealt must be an integer from 1 to 52."):
        deck.deal("three")

    with pytest.raises(ValueError, match="The number of cards to be dealt must be an integer from 1 to 52."):
        deck.deal(3.5)

def test_deck_len_method():
    deck = Deck()
    assert len(deck) == 52, "The length of an empty deck should be 0."

    deck.create_deck()
    assert len(deck) == 52, "The length of a full deck should be 52."

    deck.deal(10)
    assert len(deck) == 42, "The deck length should be 42 after dealing 10 cards."

    deck.deal(42)
    assert len(deck) == 0, "The deck length should be 0 after dealing all cards."