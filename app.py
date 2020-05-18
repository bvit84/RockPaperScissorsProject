# needed to pause after printing something
import time
# needed for random option
import random
# global variable with available moves
moves = ['rock', 'paper', 'scissors']


# one time message about program
def intro():
    print_slow("This program plays a game of Rock, Paper, Scissors between 2 Players, ")
    print_slow("and reports both Player's scores each round.")
    print_slow("NOTE: Pressing [ENTER] key without selecting any choice will pick a random choice for you!")
    


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
    name = "Mr Random"

    def move(self):
        return random.choice(moves)
            

# Player v2 subclass, returns last move in oponent list if any
class ReflectPlayer(Player):
    name = "Mr Reflect"
    def move(self):
        if len(self.their_moves)==0:
            return random.choice(moves)
        else:
            return self.their_moves[-1]


# Player v3 subclass, returns cycled own move ()
class CyclePlayer(Player):
    name = "Mr Cycle"
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


# prints a string and pauses
def print_slow(s):
    time.sleep(0.5)
    print(s)


# sorcut for printing user choice
def print_my_choice(choice):
    print_slow(f"Your choice is {choice}!")


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
            print_slow("* Random selection!")
            return random.choice(valid_options)
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
        print_slow (f" Round _{round}_")
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
        # show round score
        print_slow(f"Round {round} score: {self.p1.name}: {self.p1.score}  {self.p2.name}: {self.p2.score}")
        # call for score update
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

    # start of game
    def play_game(self, rounds):
        print_slow("--- Game start! ---")
        round = 0
        # round loop based on type selected
        if rounds == "3 rounds":
            for round in range(3):
                round+=1
                self.play_round(round)
        elif rounds == "3 wins ahead":
            while ((self.p1.score != (self.p2.score+3)) and ((self.p1.score+3) != self.p2.score)):
                round+=1
                self.play_round(round)
        else:
            self.play_round(round)
            while check_validity("Play another round? (y/n)", ["y", "n"]) == "y":
                round+=1
                self.play_round(round)

    # winner/tie announcement
    def show_winner(self):
        print_slow("--- Game ended! ---")
        print_slow(f"Final score: {self.p1.name}: {self.p1.score}  {self.p2.name}: {self.p2.score}")
        if self.p1.score > self.p2.score:
            print_slow (f"*** {self.p1.name} WON! ***")
        elif self.p1.score == self.p2.score:
            print_slow ("*** It is a TIE ! ***")
        else:
            print_slow (f"*** {self.p2.name} WON! ***")


# game option selection 
def start_game():
    print_slow("---------")
    print_slow("How many rounds would you like to play?:")
    choice = check_validity([
            "Enter 1 to play quick three rounds",
            "Enter 2 to play until any player is ahead by 3 wins",
            "Enter 3 to play until YOU stop it!"
            ], ["1", "2", "3"])
    if  choice == "1":
        rounds_selection = "3 rounds"
    elif choice == "2":
        rounds_selection = "3 wins ahead"
    else:
        rounds_selection = "YOU stop it"
    print_my_choice(choice)
    print_slow("Now choose Player 2:")
    choice = check_validity([
            "Enter 'random' to play as Mr Random (chooses it's move at random)",
            "Enter 'reflect' to play as Mr Reflect (plays opponent's last round move)",
            "Enter 'cycle' to play as Mr Cycle (cycles through the different moves)"
            ], ["random", "reflect", "cycle"])
    if  choice == "random":
        player2 = RandomPlayer()
    elif choice == "reflect":
        player2 = ReflectPlayer()
    else:
        player2 = CyclePlayer()
    print_my_choice(choice)
    print_slow(f'Selected Game: "{rounds_selection}" with {player2.name}')
    game = Game(HumanPlayer(), player2)
    game.play_game(rounds_selection)

    game.show_winner()
    play_again()


# call for parts of program
def start_program():
    intro()
    start_game()


# nothing starts if imported
if __name__ == '__main__':
    # the only call
    start_program()
