import time         # needed to pause after printing something
import random
import math         # needed for infinite loop check
moves = ['rock', 'paper', 'scissors']


# one time message about program
def intro():
    print_slow("This program plays a game of Rock, Paper, Scissors "
               "between 2 Players, ")
    print_slow("and reports both Player's scores each round.")
    print_slow("NOTE: Pressing [ENTER] key without selecting any "
               "choice will pick a random choice for you!")


# The Player class is the parent class for all of the Players in this game
class Player:

    # instance variables for each player object
    def __init__(self):
        self.score = 0
        self.my_moves = []
        self.their_moves = []

    # special rock move
    def move(self):
        print_slow("Rock rocks!")
        return "rock"

    # update move list for each player object
    def learn(self, my_move, their_move):
        self.my_moves.append(my_move)
        self.their_moves.append(their_move)


# Player Human subclass, returns validated USER input
class HumanPlayer(Player):
    name = "Human"

    def move(self):
        choice = check_validity([
            "Enter Rock to beat Scissors but lose to Paper",
            "Enter Paper to beat Rock but lose to Scissors",
            "Enter Scissors to beat Paper but lose to Rock",
            ], moves)
        return player_move_output(self.name, choice)


# Player v0 subclass, returns validated rock move
class RockPlayer(Player):
    name = "Mr Rock"


# Player v1 subclass, returns random move
class RandomPlayer(Player):
    name = "Mr Random"

    def move(self):
        choice = random.choice(moves)
        return player_move_output(self.name, choice)


# Player v2 subclass, returns last move in oponent list if any
class ReflectPlayer(Player):
    name = "Mr Reflect"

    def move(self):
        if len(self.their_moves) == 0:
            choice = random.choice(moves)
        else:
            choice = self.their_moves[-1]
        return player_move_output(self.name, choice)


# Player v3 subclass, returns cycled own move ()
class CyclePlayer(Player):
    name = "Mr Cycle"

    def move(self):
        cycle_moves = ['rock', 'paper', 'scissors']
        if len(self.my_moves) == 0:
            choice = random.choice(cycle_moves)
        else:
            cycle_moves.remove(self.my_moves[-1])
            if len(self.my_moves) == 1:
                choice = random.choice(cycle_moves)
            else:
                cycle_moves.remove(self.my_moves[-2])
                choice = cycle_moves[0]
        return player_move_output(self.name, choice)


# shorcut to player's move output
def player_move_output(name, choice):
    print_slow(f"{name}'s move is {choice}")
    return choice


# provided, used to checks if 1st player's move beats 2nd player's move
def beats(a, b):
    return ((a == 'rock' and b == 'scissors') or
            (a == 'scissors' and b == 'paper') or
            (a == 'paper' and b == 'rock'))


# prints a string and pauses
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
        # random choice for [ENTER] only
        elif input_string == "":
            choice = random.choice(valid_options)
            print_slow(f"You opted random selection: {choice}")
            return choice
        else:
            print_slow("Please try again.")
            input_string = input().lower()


#  main code for the game
class Game:

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    # start of game
    def play_game(self, rounds):
        print_slow("\n--- Game start! ---")
        round = 1

        # round loop based on type selected
        if rounds == "quick three rounds":
            while round < 4:
                self.play_round(round)
                round += 1
        elif rounds == "until any player is ahead by 3 wins":
            while ((self.p1.score != (self.p2.score+3)) and
                    ((self.p1.score+3) != self.p2.score)):
                self.play_round(round)
                round += 1
                # check 10 rounds for infinite loop
                if (math.gcd(round, 10) == 10):
                    if check_validity("Play more rounds? (y/n)",
                                      ["y", "n"]) == "n":
                        break
        else:
            self.play_round(round)
            while check_validity("Play another round? (y/n)",
                                 ["y", "n"]) == "y":
                round += 1
                self.play_round(round)
        self.show_winner()

    # round process
    def play_round(self, round):
        print_slow(f"\nRound _{round}_")
        move1 = self.p1.move()
        move2 = self.p2.move()
        # win or tie
        if beats(move1, move2):
            self.p1.score += 1
            print_slow(
                f"{self.p1.name}'s {move1} beats {self.p2.name}'s {move2}"
                )
        elif (move1 == move2):
            print_slow(f"{self.p1.name}'s {move1} is same as "
                       f"{self.p2.name}'s {move2}")
        else:
            self.p2.score += 1
            print_slow(f"{self.p1.name}'s {move1} loses "
                       f"{self.p2.name}'s {move2}")
        # show round score
        print_slow(f"Round {round} score:")
        print_slow(
            f"{self.p1.name} {self.p1.score} : {self.p2.name} {self.p2.score}"
            )
        # call for score update
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    # winner/tie announcement
    def show_winner(self):
        print_slow("--- Game ended! ---")
        print_slow(f"\nFinal score: {self.p1.name}: {self.p1.score} vs "
                   f"{self.p2.name}: {self.p2.score}")
        if self.p1.score > self.p2.score:
            print_slow(f"*** {self.p1.name} WON! ***")
        elif self.p1.score == self.p2.score:
            print_slow("*** It is a TIE ! ***")
        else:
            print_slow(f"*** {self.p2.name} WON! ***")


# player options selection
def player_options():
    choice = check_validity([
            "Enter 'human' to play as a person (keyboard input)",
            "Enter 'rock' to play as Mr Rock (always plays 'rock')",
            "Enter 'random' to play as Mr Random "
            "(chooses it's move at random)",
            "Enter 'reflect' to play as Mr Reflect "
            "(plays opponent's last round move)",
            "Enter 'cycle' to play as Mr Cycle "
            "(cycles through the different moves)"
            ], ["human", "rock", "random", "reflect", "cycle"])
    if choice == "human":
        return HumanPlayer()
    elif choice == "rock":
        return RockPlayer()
    elif choice == "random":
        return RandomPlayer()
    elif choice == "reflect":
        return ReflectPlayer()
    else:
        return CyclePlayer()


# game option selection
def start_game():
    print_slow("---------")
    print_slow("Choose Player 1:")
    player1 = player_options()
    print_slow("Now choose Player 2:")
    player2 = player_options()

    # checks if both players name are same type,
    # if so changes names to differentiate
    if (player1.name == player2.name):
        player1.name = "1st " + player1.name
        player2.name = "2nd " + player2.name

    # rounds type selection
    print_slow("\nHow many rounds would you like the game to last?:")
    choice = check_validity([
            "Enter 1 to play quick three rounds",
            "Enter 2 to play until any player is ahead by 3 wins",
            "Enter 3 to play until USER stops it"
            ], ["1", "2", "3"])
    if choice == "1":
        rounds_selection = "quick three rounds"
    elif choice == "2":
        rounds_selection = "until any player is ahead by 3 wins"
    else:
        rounds_selection = "until USER stops it"

    # print selected game options
    print_slow(f"\nSelected Game: {player1.name} vs {player2.name} play "
               f"{rounds_selection}")
    game = Game(player1, player2)
    game.play_game(rounds_selection)
    end_game()


# option for game to start again or end
def end_game():
    if check_validity("\nWould you like to play again? (y/n)",
                      ["y", "n"]) == "y":
        start_game()
    else:
        print_slow("Goodbye!")


# call for parts of program
def start_program():
    intro()
    start_game()


# nothing starts if imported
if __name__ == '__main__':
    # the only call
    start_program()
