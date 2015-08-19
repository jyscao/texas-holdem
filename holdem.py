from playingcards import *
from collections import Counter
                                                 
class HoldemRound(object):
    
    def __init__(self, deck):
        self._deck = deck
            
    def _burncard(self):
        return self._deck.deal(1)

    def _returncards(self):
        if self._deck.len() == 52: # if deck is full, then do nothing
            pass
        else:
            used = [card for hand in self.playerhands for card in hand] + self._burnt + self._community
            self._deck.reformdeck(used)

    def dealplayers(self, numplayers):
        self._returncards() # return all cards back into the main deck
        self._deck.shufflecards() # then shuffle cards before dealing
        self.playerhands = [self._deck.deal(2) for players in range(numplayers)]
        return self.playerhands

    def flop(self):
        self._burnt = self._burncard()
        print "Flop: ",
        self._community = self._deck.deal(3, show=True)

    def turn(self):
        self._burnt += self._burncard()
        print "Turn: ",
        self._community += self._deck.deal(1, show=True)

    def river(self):
        self._burnt += self._burncard()
        print "River: ",
        self._community += self._deck.deal(1, show=True)

    def showdown(self, playerhands):
        p = 1 # player number
        print "\nTime for Showdown!\n"
        for hand in playerhands:
            print "Player %d: " % p, 
            self._deck.showcards(hand)
            p += 1
        #print

    def playround(self, numplayers):
        playerhands = self.dealplayers(numplayers)
        self.flop()
        self.turn()
        self.river()
        self.showdown(playerhands)



class HandEvaluator(object): ##### Add documentations and tidy&add comments

    def __init__(self, aloc):
        self._aloc = aloc # a list of cards
        self._alor = [card[0] for card in self._aloc] # a list of ranks
        self._rk2val_lowAmap = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13} # Aces low mapping of card rank
        self._rk2val_highAmap = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':11, 'Q':12, 'K':13, 'A':14} # Aces high mapping of card rank
        self._val2rkmap = {1:'A', 2:'2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10:'10', 11:'J', 12:'Q', 13:'K', 14:'A'} # mapping of value to rank
        self._trips = self._multipool(3) # all possible triples
        self._pairs = self._multipool(2) # all possible doubles
        
    def _cards2vals(self, aloc, acehl='auto'): # returns a list of integer values of given list of cards
        if all(rk in self._alor for rk in "A 2 3 4 5".split()) and acehl == 'auto': # use aces are low mapping only if wheel staight present
            return [self._rk2val_lowAmap[card[0]] for card in aloc] # aces are low mapping
        else:
            return [self._rk2val_highAmap[card[0]] for card in aloc] # aces are high mapping
        ### note: when whole deck is used, aces are low
    
    def _getassov(self, aloc, high2low=True, acehl='auto'): # sorted set of values from any given aloc
        return sorted(list(set(self._cards2vals(aloc, acehl))), reverse=high2low)

    def _val2rk(self, value): # maps an integer value to a card rank, note both 1 and 14 maps to 'A'
        return self._val2rkmap[value]

    def _rkgetcards(self, rank, aloc=None): # returns all cards in the given card list that matches the input rank
        if aloc is None:
            aloc = self._aloc 
        return [card for card in aloc if card[0] == rank]

    def _sortcards(self, aloc, high2low=True, acehl='auto'):#=None): # sorts the given cards from high to low
        ### high2low can be removed, and in need of reverse order, just use slicing [::-1]
        _assor = [self._val2rk(val) for val in self._getassov(aloc, high2low, acehl)] # convert above set of values into corresponding set of card ranks
        _asaor = [self._rkgetcards(rk, aloc) for rk in _assor] # a sorted 2D array of card ranks
        return [card for element in _asaor for card in element] # return flattened list of above array

    def _getkickers(self, combo): # given a combo that is less than 5 cards, return possible kickers 
        return [card for card in self._sortcards(self._aloc) if card not in combo][:(5-len(combo))]

    def _multipool(self, N): # get pairs, trips or quads
        _assor = [self._val2rk(val) for val in self._getassov(self._aloc)] # assorted set of ranks for the initial hand given
        _rkcountmap = {rk:self._alor.count(rk) for rk in _assor} # map of count of unique ranks in given aloc
        if N == 4: 
            _quadrk = [rk for rk in _assor if _rkcountmap[rk] == 4]
            return [[card for card in self._aloc if card[0] == rk] for rk in _quadrk]
        elif N == 3:
            _triprk = [rk for rk in _assor if _rkcountmap[rk] == 3]
            return [[card for card in self._aloc if card[0] == rk] for rk in _triprk]
        elif N == 2:
            _pairrk = [rk for rk in _assor if _rkcountmap[rk] == 2]
            return [[card for card in self._aloc if card[0] == rk] for rk in _pairrk]

    def _str8pool(self, aloc=None):
        if aloc is None:
            aloc = self._aloc
        elif not aloc:
            return []
        _assov = self._getassov(aloc) # sorted set of values from initial aloc
        _temp = [_assov[i]+i for i in range(len(_assov))]
        _mode, _count = Counter(_temp).most_common(1)[0]
        if _count >= 5:
            _start = _temp.index(_mode)
            _str8rk = [self._val2rk(_mode - i) for i in range(_start, _start + _count)]
            return [card for card in aloc if card[0] in _str8rk]
        else:
            return []

    def _flushpool(self):
        _alos = [card[1] for card in self._aloc] # a list of suits
        _stcountmap = {st:_alos.count(st) for st in set(_alos)} # map of count of unique suits in given aloc
        return [card for card in self._aloc if _stcountmap[card[1]] >= 5]

    def _str8flush(self):
        _str8flush = self._str8pool(self._sortcards(self._flushpool()))
        return self._sortcards(_str8flush[:5], True) #False)

    def _4kind(self):
        _quads = self._multipool(4)
        if _quads: # True if _quads is not empty
            _kicker = self._getkickers(_quads[0])
            return _quads[0] + _kicker
        else:
            return []

    def _fullhouse(self):
        if self._trips and (self._pairs or len(self._trips) >= 2): # if both _trips & _pairs are non-empty OR if _trips has at least 2  elements
            _pairpool = self._sortcards([card for combo in self._trips[1:] for card in combo] + [card for combo in self._pairs for card in combo])
            # the doublet comes from all pairs and the possible remaining lower triples
            return self._trips[0] + _pairpool[:2]
        else:
            return []

    def _flush(self):
        return self._sortcards(self._flushpool(), acehl='manual')[:5] # acehl='manual' is so that aces are always high at this point of the hand eval, ugly though

    def _straight(self):
        _multiarray = self._trips + self._pairs
        _multilist = [card for combo in _multiarray for card in combo]
        _str8 = self._sortcards([card for card in self._str8pool() if card not in _multilist] + [combo[:1][0] for combo in _multiarray])
        return self._sortcards(_str8[:5], True) #False)

    def _3kind(self):
        if self._trips: # True if self._trips is not empty
            _trips = self._trips[0]
            _kickers = self._getkickers(_trips)
            return _trips + _kickers
        else:
            return []

    def _2pairs(self):
        if len(self._pairs)>=2:
            _2pairs = [card for combo in self._pairs[:2] for card in combo]
            _kicker = self._getkickers(_2pairs)
            return _2pairs + _kicker
        else:
            return []

    def _pair(self):
        if self._pairs: # True if self._pairs is not empty
            _pair = [card for combo in self._pairs[:1] for card in combo]
            _kickers = self._getkickers(_pair)
            return _pair + _kickers
        else:
            return []

    def _highcards(self):
        return self._getkickers([])

    def _besthand(self):
        _combos = [self._str8flush, self._4kind, self._fullhouse, self._flush, self._straight, self._3kind, self._2pairs, self._pair, self._highcards]
        for n in range(len(_combos)):
            _hand = _combos[n]()
            if len(_hand) == 5:
                return n, _hand

    def judgehand(self):
        _handinfo = self._besthand()
        _hID = _handinfo[0]
        _hand = _handinfo[1]
        if _hID == 0:
            if _hand[4][0] == 'A':
                print "a Royal Flush!!!"
            else:
                print "%s-high Straight Flush!" % _hand[0][0]
        elif _hID == 1:
            print "a Four of a Kind of %s's" % _hand[0][0]
        elif _hID == 2:
            print "a Full House of %s's over %s's" % (_hand[0][0], _hand[3][0])
        elif _hID == 3:
            print "a %s-high Flush of %s's" % (_hand[0][0], _hand[0][1])
        elif _hID == 4:
            print "a %s-high Straight" % _hand[0][0]
        elif _hID == 5:
            print "a Three of a Kind of %s's" % _hand[0][0]
        elif _hID == 6:
            print "Two Pairs: %s's & %s's" % (_hand[0][0], _hand[2][0])
        elif _hID == 7:
            print "a Pair of %s's" % (_hand[0][0])
        elif _hID == 8:
            print "%s-high" % (_hand[0][0])
        for card in _hand:
            print ''.join(card),
        print '\n'

