"""
from test_hands import *
testhands = [royal_flush, str8_flush, wheel_str8_flush, quads, full_house, flush, str8, trip, two_pairs, pair, high_card]
for combo in testhands:
    hand = HandEvaluator(combo)
    hand.judgehand()
"""



from holdem import *

a_deck = PlayingCards()
poker_with_fish = HoldemRound(a_deck)
for rounds in range(1):
    print "\n\nROUND %d" % (rounds + 1), "\n"
    P = 6 # number of players 
    poker_with_fish.playround(P)
    print
    
    all_hands = [pktcards + poker_with_fish._community for pktcards in poker_with_fish.playerhands]
    p = 1 # player ID
    for hand in all_hands:
        combo = HandEvaluator(hand)
        print "Player %d has" % p,
        combo.judgehand()
        p += 1



