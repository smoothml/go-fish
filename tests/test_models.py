from itertools import product

import pytest

from go_fish.models import Card, Rank, Suit


CARDS = list(product(list(Rank), list(Suit)))
CARD_STRINGS = [
    "A of Clubs",
    "A of Diamonds",
    "A of Hearts",
    "A of Spades",
    "2 of Clubs",
    "2 of Diamonds",
    "2 of Hearts",
    "2 of Spades",
    "3 of Clubs",
    "3 of Diamonds",
    "3 of Hearts",
    "3 of Spades",
    "4 of Clubs",
    "4 of Diamonds",
    "4 of Hearts",
    "4 of Spades",
    "5 of Clubs",
    "5 of Diamonds",
    "5 of Hearts",
    "5 of Spades",
    "6 of Clubs",
    "6 of Diamonds",
    "6 of Hearts",
    "6 of Spades",
    "7 of Clubs",
    "7 of Diamonds",
    "7 of Hearts",
    "7 of Spades",
    "8 of Clubs",
    "8 of Diamonds",
    "8 of Hearts",
    "8 of Spades",
    "9 of Clubs",
    "9 of Diamonds",
    "9 of Hearts",
    "9 of Spades",
    "10 of Clubs",
    "10 of Diamonds",
    "10 of Hearts",
    "10 of Spades",
    "J of Clubs",
    "J of Diamonds",
    "J of Hearts",
    "J of Spades",
    "Q of Clubs",
    "Q of Diamonds",
    "Q of Hearts",
    "Q of Spades",
    "K of Clubs",
    "K of Diamonds",
    "K of Hearts",
    "K of Spades",
]


@pytest.mark.parametrize(
    "rank, suit, expected",
    zip(
        [rank for rank, _ in CARDS],
        [suit for _, suit in CARDS],
        CARD_STRINGS,
    ),
    ids=CARD_STRINGS,
)
def test_card_str(rank: Rank, suit: Suit, expected: str) -> None:
    """Test the string representation of a card.

    Args:
        rank: The rank of the card.
        suit: The suit of the card.
        expected: The expected string representation of the card.
    """
    card = Card(rank=rank, suit=suit)
    assert str(card) == expected


@pytest.mark.parametrize(
    "card1, card2, expected_le, expected_lt",
    [
        (Card(rank=Rank.ACE, suit=Suit.CLUBS), Card(rank=Rank.ACE, suit=Suit.DIAMONDS), True, False),
        (Card(rank=Rank.ACE, suit=Suit.HEARTS), Card(rank=Rank.TWO, suit=Suit.DIAMONDS), True, True),
        (Card(rank=Rank.TWO, suit=Suit.SPADES), Card(rank=Rank.ACE, suit=Suit.DIAMONDS), False, False),
    ],
    ids=[
        "equal",
        "less than",
        "greater than",
    ],
)
def test_card_comparison(card1: Card, card2: Card, expected_le: bool, expected_lt: bool) -> None:
    """Test the card comparison dunder methods.

    Args:
        card1: The first card to compare.
        card2: The second card to compare.
        expected_le: The expected result of the less than or equal comparison.
        expected_lt: The expected result of the less than comparison.
    """
    assert (card1 <= card2) == expected_le
    assert (card1 < card2) == expected_lt
