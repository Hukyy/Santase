import random
from enum import Enum
CARD_SUIT = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
CARD_TYPE = ['9','10','Jack', 'Queen', 'King', 'Ace']
CARD_VALUE = [0, 10, 2, 3, 4, 11]

class Card:
    def __init__(self, card_type, card_suit):
        if card_type in CARD_TYPE:
            self.type = card_type
        if card_suit in CARD_SUIT:
            self.suit = card_suit

    def __str__(self):
        return "{} of {}".format(self.type, self.suit)

    @property
    def value(self):
        return CARD_VALUE[CARD_TYPE.index(self.type)]

class Deck:
    def __init__(self):
        self.cards = [Card(_type, suit) for _type in CARD_TYPE
                      for suit in CARD_SUIT]
        random.shuffle(self.cards)
        self.trump_card = self.cards[0]

    #def __getitem__(self, key):
     #   return self.cards[key]
    
    def __str__(self):
        return str([str(card) for card in self.cards])

    def get_next_card(self):
        if len(self.cards) == 0:
            raise EmptyDeck()
        return self.cards.pop()
        
    @property
    def get_trump_card(self):
        return self.trump_card

    def swap_trumps(self, new_card):
        if len(self.cards) > 2 and len(self.cards) < 18: 
            self.trump_card = new_card
            self.cards[0] = new_card
        

class PlayerPosition(Enum):
    not_player = 0
    first_player = 1
    second_player = 2

class Announce(Enum):
    none = 0
    twenty = 20
    forty = 40

class Player:
    def __init__(self, name):
        self.cards = []
        self.name = name

    def draw_card(self, card):
        self.cards.append(card)

    def make_turn(self, context): #??
        pass

class Hand:
    def __init__(self):
        self.winner
        self.first_player_card
        self.first_player_announce = Announce.none
        self.second_player_card
        self.second_player_announce = Announce.none
        self.closed_by = PlayerPosition.not_player

    def start(self):
        pass

class Round:
    def __init__(self, first_player, second_player, plays_first):
        self.first_player = first_player
        self.__first_player_points = 0
        self.__first_player_cards = []
        self.__first_player_taken_cards = []

        self.second_player = second_player
        self.__second_player_points = 0
        self.__second_player_cards = []
        self.__second_player_taken_cards = []

        self.closed_by = PlayerPosition.not_player
        self.plays_first = plays_first
        self.last_hand_taken_by = PlayerPosition.not_player
        self.deck = Deck()
        self.current_state = StartRoundState(self)

        
    @property
    def first_player_points(self):
        return self.__first_player_points

    @property
    def second_player_points(self):
        return self.__second_player_points

    @property
    def first_player_has_hand(self):
        return len(self.__first_player_taken_cards) > 0

    @property
    def second_player_has_hand(self):
        return len(self.__second_player_taken_cards) > 0

    def start(self):
        self.draw_first_cards()
        while self.round_has_finished() is False:
            self.play_hand()

    def set_state(self, new_state):
        self.current_state = new_state

    def play_hand(self):
        hand = Hand()
        hand.Start()
        self.update_points(hand)

        if hand.winner == PlayerPosition.second_player:
            self.__second_player_taken_cards.append(hand.first_player_card)
            self.__second_player_taken_cards.append(hand.second_player_card)
        else:
            self.__first_player_taken_cards.append(hand.first_player_card)
            self.__first_player_taken_cards.append(hand.second_player_card)
            
        self.plays_first = hand.winner
        self.last_hand_taken_by = self.plays_first
        self.__first_player_cards.remove(hand.first_player_card)
        self.__second_player_card.remove(hand.second_player_card)
        self.draw_new_cards()
        self.current_state.PlayHand(len(self.deck))

        if (hand.closed_by == PlayerPosition.first_player
            or hand.closed_by == PlayerPosition.second_player):
            self.current_state.close()
            self.closed_by = hand.closed_by
                

    def draw_new_cards(self):
        if self.current_state.should_draw_card:
            if self.plays_first == PlayerPosition.first_player:
                self.first_player_draw_card()
                self.second_player_draw_card()
            else:
                self.second_player_draw_card()
                self.first_player_draw_card()

    def first_player_draw_card(self):
        card = self.deck.get_next_card()
        self.first_player.draw_card(card)
        self.__first_player_cards.append(card)

    def second_player_draw_card(self):
        card = self.deck.get_next_card()
        self.second_player.draw_card(card)
        self.__second_player_cards.append(card)

    def update_points(self, hand):
        if hand.winner == PlayerPosition.first_player:
            self.__first_player_points += hand.first_player_card.value()
            self.__first_player_points += hand.second_player_card.value()
        else:
            self.__second_player_points += hand.first_player_card.value()
            self.__second_player_points += hand.second_player_card.value()
            
        self.__second_player_points += hand.second_player_announce.value
        self.__first_player_points += hand.first_player_announce.value
        
        

    def draw_fisrt_cards(self):
        for i in range(3):
            self.first_player_draw_card()
        for i in range(3):
            self.second_player_draw_card()
        for i in range(3):
            self.first_player_draw_card()
        for i in range(3):
            self.second_player_draw_card()
            
    def round_has_finished(self):
        return (self.first_player_points >=66 or
                self.second_player_points >= 66 or
                len(self.__first_player_cards) == 0 or
                len(self.__second_player_cards) == 0)
     
class Game:
    def __init__(self, first_player, second_player):
        self.first_player = first_player
        self.second_player = second_player
        self.__first_player_total_points = 0
        self.__second_player_total_points = 0
        self.rounds_played = 0
        self.plays_first = PlayerPosition.first_player
        
        

    @property
    def first_player_total_points(self):
        return self.__first_player_total_points

    @property
    def second_player_total_points(self):
        return self.__second_player_total_points

    def game_has_finished(self):
        return (self.__first_player_total_points >= 11 or
               self.__second_player_total_points >= 11)

    

    def start(self):
        while self.game_has_finished() is False:
            self.play_round()

    def play_round(self):
        game_round = Round(self.first_player, self.second_player,
                           self.plays_first)
        self.calculate_points(game_round)
        self.rounds_played += 1

    def calculate_points(self, game_round):
        if game_round.closed_by == PlayerPosition.first_player:
            if game_round.first_player_points < 66:
                self.__second_player_total_points += 3
                self.plays_first = PlayerPosition.first_player
                return

        if game_round.closed_by == PlayerPosition.second_player:
            if game_round.second_player_points < 66:
                self.__first_player_total_points += 3
                self.plays_first = PlayerPosition.second_player
                return
        if (game_round.first_player_points < 66
            and game_round.second_player_points < 66):
            winner = game_round.last_hand_taken_by
            if winner == PlayerPosition.first_player:
                self.plays_first = PlayerPosition.second_player
                self.__first__player_total_points += 1
                return
            else:
                self.plays_first = PlayerPosition.first_player
                self.__second_player_total_points += 1
                return
        if game_round.first_player_points > game_round.second_player_points:
            self.plays_first = PlayerPosition.second_player
            if game_round.second_player_points >= 33:
                self.__first_player_total_points += 1
            elif game_round.second_player_has_hand == True:
                self.__first_player_total_points += 2
            else:
                self.__first_player_total_points += 3
        elif game_round.second_player_points > game_round.first_player_points:
            self.plays_first = PlayerPosition.first_player
            if game_round.first_player_points >= 33:
                self.__second_player_total_points += 1
            elif game_round.first_player_has_hand == True:
                self.__second_player_total_points += 2
            else:
                self.__second_player_total_points += 3


class BaseState:
    def __init__(self,game_round):
        self.round = game_round
    @property
    def can_announce(self):
        return self.can_announce_20_or_40

    @property
    def can_change(self):
        return self.can_change_trump

    @property
    def can_close(self):
        return self.able_to_close

    @property
    def should_observe_rules(self):
        return self.follow_the_rules

    @property
    def should_draw_card(self):
        return self.draw_card

    def play_hand(self, cards_left):
        pass

    def close(self):
        if self.can_close == True:
            self.round.set_state(FinalState(self.round))


        
class StartRoundState(BaseState):
    def __init__(self, game_round):
        self.can_announce_20_or_40 = False
        self.can_change_trump = False
        self.able_to_close = False
        self.follow_the_rules = False
        self.draw_card = True
        self.round = game_round

    def play_hand(self, cards_left):
        self.round.set_state(MiddleGameState(self.round))


class MiddleGameState(BaseState):
    def __init__(self, game_round):
        self.can_announce_20_or_40 = True
        self.can_change_trump = True
        self.able_to_close = True
        self.follow_the_rules = False
        self.draw_card = True
        self.round = game_round

    def play_hand(self, cards_left):
        if cards_left == 2:
            self.round.set_state(TwoCardsLeftState(self.round))

class TwoCardsLeftState(BaseState):
    def __init__(self, game_round):
        self.can_announce_20_or_40 = True
        self.can_change_trump = False
        self.able_to_close = False
        self.follow_the_rules = False
        self.draw_card = True
        self.round = game_round

    def play_hand(self, cards_left):
        self.round.set_state(FinalState(self.round))

class FinalState(BaseState):
    def __init__(self, game_round):
        self.can_announce_20_or_40 = True
        self.can_change_trump = False
        self.able_to_close = False
        self.follow_the_rules = True
        self.draw_card = False
        self.round = game_round

    def play_hand(self, cards_left):
        pass

class EmptyDeck(Exception):
    pass

