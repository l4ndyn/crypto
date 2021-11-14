class Solitaire:
    def __init__(self, deck):
        self.deck = deck

    def move_down(self, card):
        if card != 53:
            self.deck[card], self.deck[card + 1] = self.deck[card + 1], self.deck[card]
            return card + 1

        self.deck.insert(1, self.deck.pop())

        return 1

    def next(self):
        joker_a = self.deck.index(53)
        self.move_down(joker_a)

        joker_b = self.deck.index(54)
        joker_b = self.move_down(joker_b)
        joker_b = self.move_down(joker_b)

        joker_a = self.deck.index(53)
    
        top_joker, bottom_joker = (joker_a, joker_b) if joker_a < joker_b else (joker_b, joker_a)
        self.deck = self.deck[bottom_joker+1:] + self.deck[top_joker:bottom_joker+1] + self.deck[:top_joker]

        count = min(self.deck[-1], 53)
        self.deck = self.deck[count:-1] + self.deck[:count] + [self.deck[-1]]

        top = min(self.deck[0], 53)
        value = self.deck[top]
        if value > 52:
            return self.next()

        return value
