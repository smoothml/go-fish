from __future__ import annotations

from enum import IntEnum, StrEnum, auto

from pydantic import BaseModel, Field


class Rank(IntEnum):
    """Card rank."""

    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


class Suit(StrEnum):
    """Card suit."""

    CLUBS = auto()
    DIAMONDS = auto()
    HEARTS = auto()
    SPADES = auto()


class Card(BaseModel):
    """Card data model."""

    rank: Rank
    suit: Suit

    def __str__(self) -> str:
        """Return the string representation of the card."""
        rank_value = self.rank.value
        rank_str = str(rank_value) if 1 < rank_value < 11 else self.rank.name.capitalize()[0]
        return f"{rank_str} of {self.suit.name.capitalize()}"

    def __le__(self, other: Card) -> bool:
        """Check if the card is less than or equal to another card."""
        return self.rank <= other.rank

    def __lt__(self, other: Card) -> bool:
        """Check if the card is strictly less than another card."""
        return self.rank < other.rank


class Player(BaseModel):
    """Player data model."""

    name: str
    hand: list[Card] = Field(default_factory=list)
    books: list[Rank] = Field(default_factory=list)


class PlayerMove(BaseModel):
    """Player move data model."""

    target_player: str = ""
    rank: str = ""
    reasoning: str = ""


class GameState(BaseModel):
    """Game state data model."""

    players: list[Player]
    deck: list[Card]
    current_player_index: int = 0
