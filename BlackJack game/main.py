import random
import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 650
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Blackjack")

# Set up fonts
font = pygame.font.SysFont(None, 55, italic=True)
small_font = pygame.font.SysFont(None, 35, italic=True)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Card deck and values
suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}


# Classes
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()


class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


# Functions for game logic
def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def is_bust(hand):
    return hand.value > 21


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# Intro functions
def intro_screen_1():
    win.fill(BLACK)
    draw_text('Black Jack', font, RED, win, width // 2 - 150, height // 2 - 50)
    draw_text('Simple 21 Game', small_font, WHITE, win, width // 2 - 150, height // 2)
    pygame.display.flip()
    time.sleep(3)


def intro_screen_2():
    win.fill(BLACK)
    draw_text('Made by Reha Demircan', font, WHITE, win, width // 2 - 250, height // 2 - 50)
    pygame.display.flip()
    time.sleep(2)


def intro_screen_3():
    win.fill(BLACK)
    draw_text('Game Mechanics:', font, RED, win, width // 2 - 200, height // 2 - 100)
    draw_text('Press H to Hit (draw a card)', small_font, WHITE, win, width // 2 - 200, height // 2 - 50)
    draw_text('Press S to Stand (end your turn)', small_font, WHITE, win, width // 2 - 200, height // 2)
    draw_text('Press R to Restart after game over', small_font, WHITE, win, width // 2 - 200, height // 2 + 50)
    draw_text('Press Q to Quit the game', small_font, WHITE, win, width // 2 - 200, height // 2 + 100)
    pygame.display.flip()
    time.sleep(4)


# Main game function
def game():
    intro_screen_1()
    intro_screen_2()
    intro_screen_3()

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Initialize deck and hands
        deck = Deck()
        deck.shuffle()

        player_hand = Hand()
        dealer_hand = Hand()

        for _ in range(2):
            player_hand.add_card(deck.deal())
            dealer_hand.add_card(deck.deal())

        player_turn = True
        dealer_turn = False
        game_over = False
        message = ""
        message_color = WHITE

        while player_turn or dealer_turn:
            win.fill(BLACK)

            # Draw player's hand
            draw_text('Player\'s Turn', font, WHITE, win, 20, 20)
            draw_text('Your Hand: ' + ', '.join([str(card) for card in player_hand.cards]), small_font, WHITE, win, 20,
                      100)
            draw_text('Total: ' + str(player_hand.value), small_font, WHITE, win, 20, 150)

            # Draw dealer's hand
            draw_text('Dealer\'s Hand: ' + ', '.join([str(card) for card in dealer_hand.cards]), small_font, WHITE, win,
                      20, 200)
            draw_text('Total: ' + str(dealer_hand.value), small_font, WHITE, win, 20, 250)

            if player_turn:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_h:  # Hit
                            hit(deck, player_hand)
                            if is_bust(player_hand):
                                message = "Player busts! Dealer wins."
                                message_color = RED
                                player_turn = False
                                game_over = True
                        elif event.key == pygame.K_s:  # Stand
                            player_turn = False
                            dealer_turn = True

            elif dealer_turn:
                if dealer_hand.value < 17:
                    hit(deck, dealer_hand)
                    if is_bust(dealer_hand):
                        message = "Dealer busts! Player wins."
                        message_color = GREEN
                        dealer_turn = False
                        game_over = True
                else:
                    dealer_turn = False
                    game_over = True
                    if dealer_hand.value > player_hand.value:
                        message = "Dealer wins."
                        message_color = RED
                    elif dealer_hand.value < player_hand.value:
                        message = "Player wins."
                        message_color = GREEN
                    else:
                        message = "It's a tie."
                        message_color = WHITE

            if game_over:
                draw_text(message, font, message_color, win, 20, 300)
                pygame.display.flip()
                time.sleep(1.5)

                draw_text('Press R to restart or Q to quit.', small_font, WHITE, win, 20, 350)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:  # Restart
                            game()
                        elif event.key == pygame.K_q:  # Quit
                            pygame.quit()
                            sys.exit()

            pygame.display.flip()
            clock.tick(30)


# Run the game
if __name__ == "__main__":
    game()
