import random

playing = False
chip_pool = 100

bet = 1

restart_phrase = "Press 'd' to shuffle or 'q' to leave.\n"

suits = ('H', 'D', 'C', 'S')
ranking = ('A','2','3','4','5','6','7','8','9','10','J', 'Q', 'K')

card_val = {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':10, 'Q':10, 'K':10}

class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.suit + self.rank
    
    def grab_suit(self):
        return self.suit
    
    def grab_rank(self):
        return self.rank
    
    def draw(self):
        print(self.suit + self.rank)


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.ace = False
    
    def __str__(self):
        hand_comp = ""

        for card in self.cards:
            card_name = card.__str__()
            hand_comp += " " + card_name

        return 'the hand has {} '.format(hand_comp)
    
    def card_add(self, card):
        self.cards.append(card)

        if card.rank == 'A':
            self.ace = True
        self.value += card_val[card.rank]

    def cal_val(self):
        if (self.ace == 'True' and self.value < 12):
            return self.value + 10
        else:
            return self.value
        
    def draw(self, hidden):
        if hidden == True and playing == True:
            starting_card = 1
        else:
            starting_card = 0
        for x in range(starting_card, len(self.cards)):
            self.cards[x].draw()

    
class Deck:

    def __init__(self):
        self.deck = []

        for suit in suits:
            for rank in ranking:
                self.deck.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal(self):
        single_card = self.deck.pop()
        return single_card
    
    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += " " + card.__str__()
        return "the deck has " + deck_comp
    
    
def make_bet():
    global bet
    bet = 0

    print('\nwhat amount of chips you like to bet? (enter whole integer please)')
    print('you have ' + str(chip_pool) + ' chips')

    while bet == 0:
        bet_comp = input()
        bet_comp = int(bet_comp)

        if bet_comp >= 1 and bet_comp <= chip_pool:
            bet = bet_comp
        else:
            print('invalid bet, you have only ' + str(chip_pool) + ' chips remainig')


def deal_cards():
    global result, playing, deck, player_hand, dealer_hand, chip_pool, bet

    deck = Deck()
    deck.shuffle()

    make_bet()

    player_hand = Hand()
    dealer_hand = Hand()

    #2 cards for player
    player_hand.card_add(deck.deal())
    player_hand.card_add(deck.deal())

    #2 cards for dealer
    dealer_hand.card_add(deck.deal())
    dealer_hand.card_add(deck.deal())

    result = "\nhit or stand? Press 'h' or 's': "

    playing = True
    game_step()


def hit():
    global playing, chip_pool, deck, player_hand, dealer_hand, result, bet

    if playing:
        if player_hand.cal_val() <= 21:
            player_hand.card_add(deck.deal())
        print('player hand is %s' %player_hand)

        if player_hand.cal_val() >= 21:
            result = 'busted!\n' + restart_phrase
            chip_pool -= bet
            playing = False
    
    else:
        result = "bad... can't hit!\n" + restart_phrase

    game_step()


def stand():
    global playing, chip_pool, deck, player_hand, dealer_hand, result, bet

    if playing == False:
        if player_hand.cal_val() > 0:
            result = "sorry, you can't stand\n"
    
    else:
        while dealer_hand.cal_val() < 17:
            dealer_hand.card_add(deck.deal())

        if dealer_hand.cal_val() > 21:
            result = "Dealer busts!\n\nYou win\n" + restart_phrase
            chip_pool += bet
            playing = False
        
        elif dealer_hand.cal_val() < player_hand.cal_val():
            result = "You bet the dealer!\nYou win" + restart_phrase
            chip_pool += bet
            playing = False
        
        elif dealer_hand.cal_val() == player_hand.cal_val():
            result = "Tied up!" + restart_phrase
            playing = False

        else:
            result = 'Dealer wins! \n' + restart_phrase
            chip_pool -= bet
            playing = False
    
    game_step()


def game_step():
    print("")
    print("Player hand is: ")
    player_hand.draw(hidden=False)
    print("Player hand total is: " + str(player_hand.cal_val()))

    print("")
    print("Dealer hand is: ")
    dealer_hand.draw(hidden=True)
    print("Dealer hand total is: " + str(dealer_hand.cal_val()))

    if playing == False:
        print('\nchip total is: ' +str(chip_pool))

    print(result)

    player_input()


def game_exit():
    print('\n\nthanks for playing! \n')
    exit()


def player_input():
    plin = input().lower()

    if plin == 'h':
        hit()
    elif plin == 's':
        stand()
    elif plin == 'd':
        deal_cards()
    elif plin == 'q':
        game_exit()
    else:
        print('\ninvalid input... press h, s, d or q: ')


def intro():
   print('\nWelcome to BlackJack! Get as close to 21 as you can without going over! \nDealer hits until she reache 17. \nAces count as 1 or 11. \nCard output goes a letter followed by a number of face notation.')

deck = Deck()
deck.shuffle()

player_hand = Hand()
dealer_hand = Hand()

intro()
deal_cards()
