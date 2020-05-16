# needed to pause after printing something
import time
# needed for random option
import random
# global variable with available moves
moves = ['rock', 'paper', 'scissors']


# 1st and one time message about program
def intro():
    print_slow("This program plays a game of Rock, Paper, Scissors between 2 Players, ")
    print_slow("and reports both Player's scores each round.")


# The Player class is the parent class for all of the Players in this game
class Player:
    # instance variables for each player object
    def __init__(self):
        # each player score
        self.score = 0
        # each player/oponent move list
        self.my_moves = []
        self.their_moves = []

    # update move list for each player object
    def learn(self, my_move, their_move):
        self.my_moves.append(my_move)
        self.their_moves.append(their_move)

# Player v0 subclass, returns validated USER input
class HumanPlayer(Player):
    name = "YOU"
    def move(self):
        return check_validity('Rock, Paper, Scissors?: ', moves)


# Player v1 subclass, returns random move
class RandomPlayer(Player):
    name = "Random AI"

    def move(self):
        return random.choice(moves)
            

# Player v2 subclass, returns last move in oponent list if any
class ReflectPlayer(Player):
    name = "Reflected AI"
    def move(self):
        if len(self.their_moves)==0:
            return random.choice(moves)
        else:
            return self.their_moves[-1]


# Player v3 subclass, returns cycled own move ()
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
        
# provided, used to checks if 1st player's move beats 2nd player's move
def beats(a, b):
    return ((a == 'rock' and b == 'scissors') or
            (a == 'scissors' and b == 'paper') or
            (a == 'paper' and b == 'rock'))


# prints string and pauses
def print_slow(s):
    time.sleep(0.5)
    print(s)


# checks validity of list, retries if failed
def check_validity(choice_list, valid_options):
    if type(choice_list) == list:
        for choice in choice_list:
            print_slow(choice)
    else:
        print_slow(choice_list)
    input_string = input().lower()
    while True:
        if input_string in valid_options:
            return input_string
        else:
            print_slow("Please try again.")
            input_string = input().lower()


# last option in game
def play_again():
    if check_validity("Would you like to play again? (y/n)", ["y", "n"]) == "y":
        start_game()
    else:
        print_slow("Goodbye!")


#  main code for the game
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
        elif rounds == "3 wins ahead":
            while ((self.p1.score != (self.p2.score+3)) and ((self.p1.score+3) != self.p2.score)):
                round+=1
                self.play_round(round)
        else:
            while check_validity("Play round? (y/n)", ["y", "n"]) == "y":
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

# game 
def start_game():
    print_slow("How many rounds to play?:")
    choice = check_validity([
            "Peress [ENTER] to play quick three rounds",
            "Enter 3 to play until any player is ahead by 3 wins",
            "Peress [SPACEBAR] to play until tired!"
            ], ["", "3"," "])
    if  choice == "":
        rounds_selection = 3
    elif choice == "3":
        rounds_selection = "3 wins ahead"
    else:
        rounds_selection = "tired"
    print_slow("Now choose Player 2 type:")
    choice = check_validity([
            "Peress [ENTER] to play 'random', the player chooses its move at random",
            "Enter r to play 'reflected'",
            "Enter c to play 'cycled'"
            ], ["", "r","c"])
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


def start_program():
    intro()
    start_game()


# nothing starts if imported
if __name__ == '__main__':
    # the only call
    start_program()
