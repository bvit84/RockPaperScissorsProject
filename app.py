#!/usr/bin/env python3

"""This program plays a game of Rock, Paper, Scissors between two Players,
and reports both Player's scores each round."""

import random
moves = ['rock', 'paper', 'scissors']

"""The Player class is the parent class for all of the Players
in this game"""


class Player:
    def __init__(self):
        # here score is the number of wins for each player, used each round
        self.score = 0
        # list of recorded moves for each player
        self.my_moves = []
        self.their_moves = []

    # methot called to update the reocorded moves
    def learn(self, my_move, their_move):
        print("pXLearn: ")
        self.my_moves.append(my_move)
        self.their_moves.append(their_move)

# AI input subclass
class RandomPlayer(Player):
    def move(self):
        return random.choice(moves)

# user input
class HumanPlayer(Player):
    def move(self):
        print('Rock, Paper, Scissors?: ')
        return input()


# AIv2 input subclass
class ReflectPlayer(Player):
    def move(self):
        # returns last in move list if any
        if len(self.their_moves)==0:
            return random.choice(moves)
        else:
            return self.their_moves[-1]


# AIv3 input subclass
class CyclePlayer(Player):
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
        

def beats(one, two):
    return ((one == 'rock' and two == 'scissors') or
            (one == 'scissors' and two == 'paper') or
            (one == 'paper' and two == 'rock'))


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def play_round(self):
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(f"Player 1: {move1}  Player 2: {move2}")
        if  beats(move1, move2):
            self.p1.score += 1
            print(f"Player 1 Wins!")
        elif (move1 == move2):
            print(f"Tie!")
        else:
            self.p2.score +=1
            print(f"Player 2 Wins!")
        print(f"Score: Player 1: {self.p1.score}  Player 2: {self.p2.score}")
        print("p1Learn")
        self.p1.learn(move1, move2)
        print("p2Learn")
        self.p2.learn(move2, move1)

    def play_game(self):
        print("Game start!")
        for round in range(1, 4):
            print(f"Round {round}:")
            self.play_round()
        print("Game over!")


if __name__ == '__main__':
    game = Game(HumanPlayer(), CyclePlayer())
    game.play_game()