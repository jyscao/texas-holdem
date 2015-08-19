# -*- coding: utf-8 
from itertools import product
from random import shuffle

class PlayingCards(object):
    
    def __init__(self):
        self._ranks = "2 3 4 5 6 7 8 9 10 J Q K A".split()
        self._suits = "♠ ♥ ♣ ♦".split()
        self._cards = [(rk, st) for rk, st in product(self._ranks, self._suits)]

    def len(self):
        return len(self._cards)

    def showcards(self, aloc=None): # show cards in a list of cards via printing
        if aloc is None:
            aloc = self._cards
        for card in aloc:
            print ''.join(card),
        print

    def shufflecards(self): # shuffling the deck
        shuffle(self._cards)
    
    def deal(self, N, show=False): # dealing N cards, not shown by default
        dealt = [self._cards.pop() for i in range(N)]
        if show == True:
            self.showcards(dealt)
        return dealt

    def reformdeck(self, dealt):
        self._cards += dealt
        return self._cards


a_deck = PlayingCards()
#a_deck.showcards()
