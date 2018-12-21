
import random
import getpass
from pathlib import Path
import pickle

def main_game():
    game_settings = GameSettings()
    game_users = GameUsers()

    introduction() ## print introduction

    while True:
        ## If there are not yet enough users, then there is a need to first add user(s):
        ## Note that changing the settings [num_players] may require more than 2 users!
        while game_users.number_of_users() < game_settings.num_players :
            game_users.add_user()
        
        ## prompt the main menue:
        prompt = ("Enter 1 to add a user\n"
                "Enter 2 to play the game\n"
                "Enter 3 to view user records\n"
                "or    0 to to exit (terminate) the game\n"
                ">>> ")
                
        res = select_number(prompt, 0, 9, None) ## user selection
        if res == 1: # add user
            game_users.add_user()
        elif res == 2: # run game
            players = game_users.select_players(game_settings.num_players)
            if players is None:
                continue
            
            play_again = True
            while play_again: ## play many games with the same players and settings
                
                game = Game(players, game_settings) ## set a new game
                winner_loser = game.run()  ## run the game
                
                if winner_loser != None:  ## if there is a winner and a loser, we store them in game users:
                    game_users.user_win(winner_loser[0]) ## store the winner
                    game_users.user_loss(winner_loser[1]) ## store the loser
                play_again = query_yes_no("Would you like to play again?") ## play again?
            
        elif res == 3: # print the user recors
            game_users.user_records()
        
        elif res == 9: # advance change settings
            game_settings.change_settings()
        elif res == 0: #terminate, exit!
            break

def introduction():
    print ("""
===================================================
= Introduction") =
= Introduction: blah blah blah... Ron, please complete the introduction with good English")
= "blah blah blah...
===================================================
""")
            
### Game settings ### 
"""The advance game settings 
It store most of the constant of the games. 
changing the settings helped me to test different feature and code
"""

class GameSettings:
    def __init__(self):
        self.initialize_defaults()
        
    def initialize_defaults(self):
        self.cube_size = 6
        self.num_turns = 5
        self.bonus = [10, -5] # 10 points bonus for even rolls, -5 penalty for odd rolls
        self.num_players = 2
        self.num_of_dice = 2 # the number of dice to roll at each turn
        self.double_num_of_dice = 1 # the number of dice to roll when double
        self.draw_num_of_dice = 1 # the number of dice to roll after the main game ended at draw

    def change_settings(self):
        while True:
            prompt = ("Enter 1 to change cube size \n"
                "Enter 2 to change number of turns \n"
                "Enter 3 to change even number bonus (or penalty) \n"
                "Enter 4 to change odd number bonus (or penalty)  \n"
                "Enter 5 to change the number of players in a game  \n"
                "Enter 6 to change the number of dice in each regular roll \n"
                "Enter 7 to change the number of dice to roll when a double occur  \n"
                "Enter 8 to change the number of dice to roll after the main game ended at draw \n"
                "Enter 9 to set all settings back to defaults \n"
                "or    0 to exit to the main menu \n"
                ">>> ")

            selection = select_number(prompt, 0, 9, None)
            if selection == 1:
                prompt = ("Please enter the cube size \n"
                    "The default (recommended) value is 6 and the current value is " + str(self.cube_size) + "\n"
                    ">>> ")
                self.cube_size = select_number(prompt, 2, None, 6)
            elif selection == 2:
                prompt = ("Please enter the number of turns \n"
                    "The default (recommended) value is 5 and the current value is " + str(self.num_turns) + "\n"
                    ">>> ")
                self.num_turns = select_number(prompt, 0, None, 5)
            elif selection == 3:
                prompt = ("Please enter even number bonus (negative for penalty) \n"
                    "The default (recommended) value is 10 and the current value is " + str(self.bonus[0]) + "\n"
                    ">>> ")
                self.bonus[0] = select_number(prompt, None, None, 10)
            elif selection == 4:
                prompt = ("Please enter odd number bonus (negative for penalty) \n"
                    "The default (recommended) value is -5 and the current value is " + str(self.bonus[1]) + "\n"
                    ">>> ")
                self.bonus[1] = select_number(prompt, None, None, -5)
            elif selection == 5:
                print("IMPORTANT NOTE: when the number of players is different than 2:")
                print("=============== there is no draw (even if all players ended with the same score)")
                print("=============== and the winner and loser are not recorded")
                prompt = ("Please enter the number of players in a game \n"
                    "The default (recommended) value is 2 and the current value is " + str(self.num_players) + "\n"
                    ">>> ")
                self.num_players = select_number(prompt, 2, None, 2)
            elif selection == 6:
                prompt = ("Please enter the number of dice in each regular roll \n"
                    "The default (recommended) value is 2 and the current value is " + str(self.num_of_dice) + "\n"
                    ">>> ")
                self.num_of_dice = select_number(prompt, 0, None, 2)
            elif selection == 7:
                prompt = ("Please enter the number of dice to roll when a double occur \n"
                    "The default (recommended) value is 1 and the current value is " + str(self.double_num_of_dice) + "\n"
                    ">>> ")
                self.double_num_of_dice = select_number(prompt, 0, None, 1)
            elif selection == 8:
                prompt = ("Please enter the number of dice to roll after the main game ended at draw \n"
                    "The default (recommended) value is 1 and the current value is " + str(self.draw_num_of_dice) + "\n"
                    ">>> ")
                self.draw_num_of_dice = select_number("Please enter the number of dice to roll after the main game ended at draw  >>> ", 1, None, 1)
            elif selection == 9:
                self.initialize_defaults()
            else :
                break
                

class Game:
    def __init__(self, players, settings):
        self.players = players
        self.s = settings
        self.scores = []
        for i in range(settings.num_players):
            self.scores += [0]

    def run(self):
        for i in range(self.s.num_turns) :
            print("===== Turn #", i+1, "=====")
            for j in range(self.s.num_players):
                print("*** Player: ", self.players[j], "***")
                points = self.play(j, self.s.num_of_dice, True)
                
            print ("The score at the end of turn #", i+1)
            for j in range(self.s.num_players):
                print(self.players[j], "has", self.scores[j], "points")

        if self.s.num_players == 2:
            i = 0
            while self.scores[0] == self.scores[1]:
                i += 1
                print("Draw!", self.scores[0],  " extra turn #", i, " roll single dice")
                for j in range(self.s.num_players):
                    print("*** Player:", self.players[j], "***")
                    self.play(j, self.s.draw_num_of_dice, False)

            print ("The scores:")
            winner = 0
            if self.scores[0] < self.scores[1]:
                winner = 1
            ## player[winner] has the higher score 
            ## The loser is player[1-winner]
            print("The winner is", self.players[winner], "with", self.scores[winner], "points")
            print(self.players[1-winner], "receive", self.scores[1-winner], "points")
            return [ self.players[winner], self.players[1-winner] ]


    def bonus(self, roll, player_number):
        if len(roll) == 2 and roll[0] == roll[1] : ### Double!! roll again:
            print("~ ", self.players[player_number], "You rolled double", roll[0], "and you have a bonus roll ~")
            return self.play(player_number, self.s.double_num_of_dice, False) ## roll the dice again! (note this is a recusive call!!!)

        else: # Bonus
            odd = (roll[0] + roll[1]) % 2 ## 0 for even, 1 for odd
            bonus = self.s.bonus[ odd ]
            if bonus > 0:
                print("Lucky roll! you received", bonus, " bonus points")
            elif bonus < 0:
                print("Unlucky, you lose", -bonus, " points")
            ## else: ## no bonus, i.e. bunus must 0
                
            self.scores[player_number] += bonus ## add the bonus to the score
            return bonus

    def play(self, player_number, num_of_dice, add_bonus): # i is the number of turn, j is the number of user that plays
        input(self.players[player_number] + " please press Enter to roll the dice...")
        roll = []
        roll_score = 0
        for i in range (num_of_dice):
            r = random.randint(1, self.s.cube_size)
            roll_score += r
            roll +=  [ r ]
        
        print("You rolled:", roll, "and you scored", roll_score, "points")
        self.scores[player_number] += roll_score
        
        if add_bonus:
            roll_score += self.bonus(roll, player_number)
            print(self.players[player_number], "your score for this turn is", roll_score, "points")
            
        if self.scores[player_number] < 0:
            self.scores[player_number] = 0
        return roll_score


def test_game():
    s = GameSettings()
    g = Game(['Tom', 'Ron'], s)
    #g.bonus([3,3], 0)
    #g.bonus([0,1], 0)
    #g.bonus([0,2], 0)
    
    #g.bonus([3,3], 1)
    #g.bonus([0,1], 1)
    #g.bonus([0,2], 1)

    #g.play(0, 1, False)
    #g.play(0, 2, False)
    #g.play(0, 2, True)

    #g.play(1, 1, False)
    #g.play(1, 2, False)
    #g.play(1, 2, True)

    g.run()

# test_game()


### Game Users ### 
"""The following is Gameusers class
It handles all the usage of the users in the game
It stores a map of users and their <passwords, number of wins, number of losses
It persists its data in pickle file with name: game_storage.pkl
requires:

from pathlib import Path
import pickle
import getpass
"""

class GameUsers:
    def __init__(self):
        self.s = {}
        self.file_name = 'game_storage.pkl'
        
        if Path(self.file_name).exists() :
            self.s = pickle.load( open(self.file_name, 'rb') )
    
    def store(self):
        pickle.dump(self.s, open(self.file_name, 'wb'))
    
    def add_user(self):
        print ("Adding a user:")
        
        username = None
        password = None
        ## get the user name: 
        while True :
            username = input("Please type user name...")
            if len(username) < 3 :
                print("User name must contain at least 3 characters" )
            elif len(username) > 30 :
                print("User name contain maximum 30 characters" )
            elif ' ' in username :
                print("User name must not contain spaces" )
            elif username in self.s :
                print("Sorry, user name " + username + " already exists" )
            else:
                break
        
        ## Now password
        while True :
            password = getpass.getpass("Please type the password for " + username)
            if len(password) < 3 :
                print("Password must contain at least 3 characters" )
            elif len(password) > 30 :
                print("Password contain maximum 30 characters" )
            elif ' ' in password :
                print("Password must not contain spaces" )
            else:
                break
        
            
        self.s[username] = {'password':encrypt(password), 'win':0,'loss':0}
        self.store()
        return username
    
    def select_players(self, number_of_players):
        players = []
        while len(players) < number_of_players:
            print ("Selecting a player:")
            username = None
            while True :
                username = input("Please type user name... (or press Enter to exist to the main menue)...")
                if len(username) < 1 :
                    return None
                elif username not in self.s :
                    print("Sorry, user name " + username + " does not exists" )
                elif username in players:
                    print("Player " + username + " already selected, please select a different user" )
                else:
                    break

            password = None
            for i in range(3) : ## 3 attempts to enter matching password
                password = getpass.getpass("Please type the password for " + username)  ## get the password from the user
                if password == decrypt( self.s[username]['password'] ) : ## compare the password to the saved password
                    players += [ username ] ### Add a user, password matches!
                    break ## Next user...
                print("Sorry, wrong password for user name: " + username  )
                password = None
                
            if password is None:
                return None
        return players
    
    def user_win(self, username):
        self.s[username]['win'] += 1  ## increment the number of wins
        self.store() ## Store in pickle file
    def user_loss(self, username):
        self.s[username]['loss'] += 1 ## increment the number of losss
        self.store() ## Store in pickle file
    def user_records(self): ## Print the records (except the passwords!)
        for username in sorted(self.s.keys()): # iterate sorted, nice.
            print (username, "won", self.s[username]['win'], "games and lost", self.s[username]['loss'], "games")
        
    def number_of_users(self):
        return len(self.s)



### Utilities and methods from other sources ###

## Method was taken from: https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
def query_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        print(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            print("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")
            
def encrypt (s): ## I don't know how to encrypt or decrypt
    return s
def decrypt (s): ## I don't know how to encrypt or decrypt
    return s

def select_number(prompt, minimum, maximum, default):
    if default is not None :
        prompt += " [default: " + str(default) + "]"
    while True:
        i = input(prompt)
        if i == "" and default is not None:
            return default
        try:
            res = int(i)
        except ValueError:
            continue
        if minimum is not None and res < minimum :
            print ("The number must be >=", minimum)
        elif maximum is not None and res > maximum :
            print ("The number must be <=", maximum)
        else:
            return res
    
        
main_game()