import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card():
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    def __str__(self):
        return f'{self.rank} of {self.suit}'

class Deck():
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))
    def __str__(self):
        deck_of_cards = ''
        for card in self.deck:
            deck_of_cards += card.__str__() + '\n'
        return deck_of_cards
    def shuffle(self):
        random.shuffle(self.deck)
    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand():
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        # track aces
        if card.rank == 'Ace':
            self.aces += 1
    def adjust_for_ace(self):
        # if total value > 21 and still have an ace
        # change ace to be a 1 instead of 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips():
    def __init__(self,total=100):
        self.total = total
        self.bet = 0
    def win_bet(self):
        self.total += self.bet
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("Bet amount: "))
        except ValueError:
            print("Enter a valid integer for bet amount.")
            continue
        else:
            if chips.bet > chips.total:
                print(f"Bet exceeds available total. You have {chips.bet} available chips.")
                continue
            else:
                break

def hit(deck, hand):
    dealt_card = deck.deal()        
    hand.add_card(dealt_card)        
    hand.adjust_for_ace()

def hit_or_stand(deck, hand):
    global playing 
    while True:
        choice = input("Hit or Stand? (H/S): ")
        if choice[0].lower() == 'h':
            hit(deck, hand)
        elif choice[0].lower() == 's':
            print("Player stands, Dealer's turn.")
            playing = False
        else:
            print("Enter (H/S) only.")
            continue
        break

def show_some(player, dealer):
    # show only one of the dealer's cards
    print("Dealer's Hand. \n")
    print("First card hidden!")
    print(dealer.cards[1])
    # show all (2 cards) of players hand
    print("Player's hand. \n")
    for card in player.cards:
        print(card)

def show_all(player, dealer):
    # show all the dealer's cards
    print("Dealer's's hand. \n")
    for card in dealer.cards:
        print(card)
    # calculate and display value (J+K == 20)
    print(f"Value of Dealer's hand is: {dealer.value}")
    # show all the players cards
    print("Player's hand. \n")
    for card in player.cards:
        print(card)
    print(f"Value of Player's's hand is: {player.value}")

def player_busts(player, dealer, chips):
    print("Player Bust.")
    chips.win_bet()

def player_wins(player, dealer, chips):
    print("Player Wins. Dealer Bust")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("Dealer Bust.")
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print("Dealer Wins. Player Bust")
    chips.win_bet()
    
def push():
    print("Dealer and Player tied. Push.")



while True:
    print("Welcome to BlackJack.")
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal()) 
        
    player_chips = Chips(100)

    take_bet(player_chips)

    show_some(player_hand, dealer_hand)
    
    while playing:
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)
        if player_hand.value > 21:
            player_bust(player_hand, dealer_hand, player_chips)    
        break

    if player_hand.value <= 21:
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
    
        show_all(player_hand, dealer_hand)
        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
    
    # Inform Player of their chips total 
    print(f"\nPlayer total chips are {player_chips.total}")
    # Ask to play again
    new_game = input("Would you like to play another hand? y/n")
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thank you for playing!")
        break
