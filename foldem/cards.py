"""
Manage cards, suits, and decks, their ordering and symbols.



https://en.wikipedia.org/wiki/Playing_cards_in_Unicode
"""

from random import shuffle


def delegate_rank_comparisons(cls):
    """Delegate comparison operations on cards to their respective ranks"""
    for op in ('__eq__', '__ne__', '__le__', '__lt__', '__ge__', '__gt__'):
        setattr(cls, op, lambda self, other: getattr(self.rank, op)(other.rank))
    return cls


@delegate_rank_comparisons
class Card:

    _ranks = {'blank': 0, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    _ranks.update({str(x): x for x in range(2, 11)})

    def __init__(self, name, suit, symbol):
        self.name = name
        self.suit = suit
        self.symbol = symbol
        self.rank = self._ranks[name]
    
    def __str__(self):
        return self.symbol
    
    def __repr__(self):
        return f"<Card name='{self.name}', suit='{self.suit.symbol}', symbol='{self.symbol}'>"
    

class Suit:
    def __init__(self, name, symbol, card_codepoint_base):
        self.name = name
        self.initial = name[0].upper()
        self.symbol =  symbol
        self._card_codepoint_base = card_codepoint_base
        self.cards = self.generate_cards()
    
    def generate_cards(self):
        codepoints = {}
        for n in range(2, 11):
            codepoints[str(n)] = self._card_codepoint_base + n
        for name, increment in (('J', 0xB), ('Q', 0xD), ('K', 0xE), ('A', 0x1)):
            codepoints[name] = self._card_codepoint_base + increment
        cards = tuple([Card(k, self, chr(v)) for k, v in codepoints.items()])
        return cards

    def __str__(self):
        return self.symbol
    
    def __repr__(self):
        return f"<Suit name='{self.name}', symbol='{self.symbol}', cards={tuple(c.symbol for c in self.cards)}>"


blank = Card(suit=None, name='blank', symbol='🂠')


class Deck:
    suits = (
        Suit('Spades', '♠', 0x1F0A0),    # 🂢 🂣 🂤 🂥 🂦 🂧 🂨 🂩 🂪 🂫 🂭 🂮 🂡
        Suit('Hearts', '♥', 0x1F0B0),    # 🂲 🂳 🂴 🂵 🂶 🂷 🂸 🂹 🂺 🂻 🂽 🂾 🂱
        Suit('Diamonds', '♦', 0x1F0C0),  # 🃂 🃃 🃄 🃅 🃆 🃇 🃈 🃉 🃊 🃋 🃍 🃎 🃁
        Suit('Clubs', '♣', 0x1F0D0),     # 🃒 🃓 🃔 🃕 🃖 🃗 🃘 🃙 🃚 🃛 🃝 🃞 🃑
    )

    def __init__(self):
        all_cards = []
        for suit in self.suits:
            all_cards.extend(suit.cards)
        shuffle(all_cards)
        self.undealt = all_cards
        self.dealt = []

    def deal(self):
        card = self.undealt.pop()
        self.dealt.append(card)
        return card
        
    def __repr__(self):
        dealt = ",".join([c.symbol for c in self.dealt])
        undealt = ",".join([c.symbol for c in self.undealt])
        return f'<Deck {dealt=}, {undealt=}>'
