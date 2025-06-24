import pytest
from src.card import Card

def test_card_initialization_valid_data():
    card = Card(6, "Diamonds")
    assert card.rank == 6, "Rank of card must be 6"
    assert card.suit == "Diamonds", "Suit of card must be 'Diamonds'"
    assert not card.is_face_up, "Card must be face down at initialisation"

def test_card_initialization_with_invalid_rank_raises_valueerror():
    with pytest.raises(ValueError, match="Rank of card must be in range of 1 to 13"):
        Card(rank=0, suit="Hearts") # Rank 0 is inappropriate
    with pytest.raises(ValueError, match="Rank of card must be in range of 1 to 13"):
        Card(rank=14, suit="Hearts")

def test_card_initialization_with_invalid_suit_raises_valueerror():
    with pytest.raises(ValueError, match="Suit of card must be in range of valid suits"):
        Card(rank=4, suit="Crystals")   

def test_card_flip_toggles_face_correctry():
    card = Card(6, "Spades")
    assert not card.is_face_up, "Card must be face down at initialization"
    card.flip()
    assert card.is_face_up, "Card must be face up at first flip"
    card.flip()
    assert not card.is_face_up, "Card must be face down at second flip"

