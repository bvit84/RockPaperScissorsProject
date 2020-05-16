"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

import time
import random
moves = ['rock', 'paper', 'scissors']

"""The Player class is the parent class for all of the Players
in this game"""

class Player:
    # instance variables for each player object
    def __init__(self):
        # each player score
        self.score = 0
        # each player/oponent move list
        self.my_moves = []
        self.their_moves = []

    # methot called to update move list
    def learn(self, my_move, their_move):
        self.my_moves.append(my_move)
        self.their_moves.append(their_move)

# AI input subclass, returns random move
class RandomPlayer(Player):
    name = "Random AI"

    def move(self):
        return random.choice(moves)

# user input subclass, returns validated input
class HumanPlayer(Player):
    name = "YOU"

    def move(self):
        return check_validity(input('Rock, Paper, Scissors?: ').lower(), moves)
            

# AIv2 input subclass, returns last move in oponent list if any
class ReflectPlayer(Player):
    name = "Reflected AI"

    def move(self):
        if len(self.their_moves)==0:
            return random.choice(moves)
        else:
            return self.their_moves[-1]


# AIv3 input subclass, returns cycled own move ommiting last 2 used if any
class CyclePlayer(Player):
    name = "Cycled AI"

    def move(self):
        cycle_moves = ['rock', 'paper', 'scissors']
        if len(self.my_moves)==0:
            return random.choice(cycle_moves)
        else:
            cycle_moves.remove(self.my_moves[-1])
            if len(self.my_moves)==1:
                return random.choice(cycle_moves)
            else:
                cycle_moves.remove(self.my_moves[-2])
                return cycle_moves[0]
        
# provided, checks if move1 beats move2
def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


# last option in game
def play_again():
    if check_validity(choice_show([
            "Would you like to play again? (y/n)"]), ["y", "n"]) == "y":
        start_game()
    else:
        print_slow("Goodbye!")

# slowly prints the choices, and returns the user input
def choice_show(choice_list):
    for choice in choice_list:
        print_slow(choice)
    return input().lower()


# prints string and pauses
def print_slow(s):
    time.sleep(0.5)
    print(s)


# intro information before game starts
def intro():
    print_slow(
        """This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""
    )


# checks validity of string, retries if failed
def check_validity(input_string, valid_options):
    while True:
        if input_string in valid_options:
            return input_string
        else:
            print_slow("Please try again.")
            input_string = input().lower()

#  
class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def play_round(self,round):
        print_slow (f"Round {round}:")
        move1 = self.p1.move()
        move2 = self.p2.move()
        print_slow(f"YOU: {move1}  {self.p2.name}: {move2}")
        # who wins or tie
        if  beats(move1, move2):
            self.p1.score += 1
            print_slow(f"{self.p1.name} Won!")
        elif (move1 == move2):
            print_slow(f"Tie!")
        else:
            self.p2.score +=1
            print_slow(f"{self.p2.name} Wins!")
        print_slow(f"Round {round} score: {self.p1.name}: {self.p1.score}  {self.p2.name}: {self.p2.score}")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)


    # start of game and rounds loop
    def play_game(self, rounds):
        print_slow("Game start!")
        round = 0
        if rounds == 3:
            for round in range(3):
                round+=1
                self.play_round(round)
        elif rounds == "3wins":
            while ((self.p1.score != (self.p2.score+3)) and ((self.p1.score+3) != self.p2.score)):
                round+=1
                self.play_round(round)
        else:
            while check_validity(choice_show(["Play round? (y/n)"]), ["y", "n"]) == "y":
                round+=1
                self.play_round(round)

    # winner announcement
    def show_winner(self):
        print_slow("Game ended!")
        if self.p1.score >> self.p2.score:
            print_slow (f"{self.p1.name} WON! :)")
        elif self.p1.score == self.p2.score:
            print_slow ("It is a TIE ! :|")
        else:
            print_slow (f"{self.p2.name} WON! :(")

# 1st def that starts the game
def start_game():
    intro()
    print_slow("How many rounds to play?:")
    choice = check_validity(choice_show([
            "Peress [ENTER] to play quick 3 rounds",
            "Enter 3 to play until one player is ahead by three points",
            "Enter 'q' to play non-stop!"
            ]), ["", "3","q"])
    if  choice == "":
        rounds_selection = 3
    elif choice == "3":
        rounds_selection = "3wins"
    else:
        rounds_selection = "qstop"
    print_slow("Now choose AI player type:")
    choice = check_validity(choice_show([
            "Peress [ENTER] to play 'random'",
            "Enter r to play 'reflected'",
            "Enter c to play 'cycled'"
            ]), ["", "r","c"])
    if  choice == "":
        AI = RandomPlayer()
        AItype = "Random"
    elif choice == "r":
        AI = ReflectPlayer()
        AItype = "Reflected"
    else:
        AI = CyclePlayer()
        AItype = "Cycled"
    print_slow(f"Selected Game: {rounds_selection} rounds with {AItype} type of AI")
    game = Game(HumanPlayer(), AI)
    game.play_game(rounds_selection)
    game.show_winner()
    play_again()

# game will not start if imported
if __name__ == '__main__':
    # the only game call
    start_game()
