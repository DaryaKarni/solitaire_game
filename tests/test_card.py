import pytest
from src.card import Card

def test_card_initialization_valid_data():
    card = Card(6, "Diamonds")
    assert card.rank == 6, "Rank of card must be 6"
    assert card.suit == "Diamonds", "Suit of card must be 'Diamonds'"
    assert not card.is_face_up, "Card must be face down at initialisation"

def test_card_initialization_with_invalid_rank_raises_valueerror():
    with pytest.raises(ValueError, match="Rank of card must be in range of 1 to 13"):
        Card(rank=0, suit="Hearts")
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

def test_is_red():
    card_heart = Card(7, "Hearts")
    assert card_heart.is_red() is True, "A Heart card should be red"

    card_diamond = Card(10, "Diamonds")
    assert card_diamond.is_red() is True, "A Diamond card should be red"

    card_club = Card(2, "Clubs")
    assert card_club.is_red() is False, "A Club card should not be red"

    card_spade = Card(13, "Spades") 
    assert card_spade.is_red() is False, "A Spade card should not be red"
