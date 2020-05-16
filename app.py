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
        self.input_text = ""
        while self.input_text not in moves:
            self.input_text = (input('Rock, Paper, Scissors?: ')).lower()
        else:
            return self.input_text
            

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


# Announce the winner at the end of game
def score_is(a,b):
    if a >> b:
        return "Player 1 WON!"
    elif a == b:
        return "It is a TIE !"
    else:
        return "Player 2 WON!"


# last option in game
def play_again():
    if check_validity(choice_show([
            "Would you like to play again? (y/n)"]), ["y", "n"]) == "y":
        play_game()
    else:
        print_slow("Goodbye!")

# slowly prints the choises, and returns the user input
def choice_show(choise_list):
    for choice in choise_list:
        print_slow(choice)
    return input().lower()


# prints string and waits
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

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(f"YOU: {move1}  self.p2.name: {move2}")
        # who wins or tie
        if  beats(move1, move2):
            self.p1.score += 1
            print(f"{self.p1.name} Won!")
        elif (move1 == move2):
            print(f"Tie!")
        else:
            self.p2.score +=1
            print(f"{self.p2.name} Wins!")
        print(f"Score: {self.p1.name}: {self.p1.score}  {self.p2.name}: {self.p2.score}")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    # start of game and round loop
    def play_game(self,rounds):
        print("Game start!")
        for round in range(1, rounds+1):
            print(f"Round {round}:")
            self.play_round()
        # winner announcement
        print(f"Game ended!\n{score_is(self.p1.score,self.p2.score)}")

# 1st def that starts the game
def play_game():
    intro()
    choise = check_validity(choice_show([
            "Peress [ENTER] to play quick 3 rounds",
            "Enter 3 to play until one player is ahead by three points",
            "Enter 'q' to play untill 'quit' or 'q' is entered"
            ]), ["", "3","q"])
    if  choise == "":
        rounds = 3
    elif choise == "2":
        rounds = "3wins"
    else:
        rounds = "qstop"
    choise = check_validity(choice_show([
            "Peress [ENTER] to play 'random'",
            "Enter r to play 'reflected'",
            "Enter 3 to play 'cycled'"
            ]), ["", "r","c"])
    if  choise == "":
        AI = RandomPlayer()
    elif choise == "r":
        AI = ReflectPlayer()
    else:
        AI = CyclePlayer()
    game = Game(HumanPlayer(), AI)
    game.play_game(rounds)
    play_again()

# game will not start if imported
if __name__ == '__main__':
    # the only game call
    play_game()
