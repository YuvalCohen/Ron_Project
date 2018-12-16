
import random
import getpass
from pathlib import Path
import pickle


game_settings = GameSettings()
game_users = GameUsers()

introduction() ## print introduction
while game_users.number_of_users() < game_settings.num_players :
    game_users.add_user()

while True:
	res = select({
		1: "Add a user",
		2: "Play a game",
		3: "Print player records"
		})
    res = main_selection()
    if res = 1: # add user
        game_users.add_user()
    elif res = 2: # run game
        for i in range(game_settings.num_players):
            players[i] = game_users.select_user()
            if players[i] == None :
                break
		
		game = Game(players, game_settings) ## these players are going to play now
		play_again = True
		while play_again: ## play many games with the same players and settings
			winner_loser = game.run()  ## run the game
			if winner_loser != None:  ## if there is a winner and a loser, we store them in game users:
				game_users.win(winner_loser[0]) ## store the winner
				game_users.lost(winner_loser[1]) ## store the loser
			play_again = query_yes_no("Would you like to play again?") ## play again?
		
	elif res = 3: # run game
		game_users.user_records()
	
	elif res = 9: # advance change settings
	
	elif res = 0: # advance change settings
		break

### Game settings ### 
"""The advance game settings 
It store most of the constant of the games. 
changing the settings helped me to test different feature and code
"""

class GameSettings:
    def __init__(self):
		self.initialize_defaults()
		
	def initialize_defaults(self)
        self.cube_size = 6
        self.num_turns = 5
        self.bonus = [10, -5] # 10 points bonus for even rolls, -5 penalty for odd rolls
        self.num_players = 2
        self.num_of_dice = 2 # the number of dice to roll at each turn
        self.double_num_of_dice = 1 # the number of dice to roll when double
        self.draw_num_of_dice = 1 # the number of dice to roll after the main game ended at draw

	def change_settings(self):
		while True:
			print ("Enter 1 to change cube size, default: 6")
			print ("Enter 2 to change number of turns, default: 5")
			print ("Enter 3 to change even number bonus (or penalty), default: 10")
			print ("Enter 4 to change odd number bonus (or penalty), default: -5")
			print ("Enter 5 to change the number of players in a game, default: 2")
			print ("Enter 6 to change the number of dice in each regular roll, default: 2"
			print ("Enter 7 to change the number of dice to roll when a double occur, default: 1")
			print ("Enter 8 to change the number of dice to roll after the main game ended at draw, default: 1")
			print ("Enter 9 to set all settings back to defaults")

			selection = select_number("Enter 0 to exit to the main menu", 0, 9, None)
			if selection == 1:
				self.cube_size = select_number("Please enter the cube size", 2, None, 6)
			elif selection == 2:
				self.num_turns = select_number("Please enter the number of turns", 0, None, 5)
			elif selection == 3:
				self.bonus[0] = select_number("Please enter even number bonus (negative for penalty)", None, None, 10)
			elif selection == 4:
				self.bonus[1] = select_number("Please enter odd number bonus (negative for penalty)", None, None, -5)
			elif selection == 5:
				print("When the number of players is different than 2, there is no draw (even if all players ended with the same score)"
				print("and the winner and loser are not recorded")
				self.num_players = select_number("Please enter the number of players in a game", 2, None, 2)
			elif selection == 6:
				self.num_of_dice = select_number("Please enter the number of dice in each regular roll", 0, None, 2)
			elif selection == 7:
				self.double_num_of_dice = select_number("Please enter the number of dice to roll when a double occur", 0, None, 1)
			elif selection == 8:
				self.draw_num_of_dice = select_number("Please enter the number of dice to roll after the main game ended at draw", 1, None, 1)
			elif selection == :
				self.initialize_defaults()
			else :
				break
				

class Game:
    def __init__(self, users, settings):
        self.users = users
        self.s = settings
        self.scores = []
        for i in range(settings.num_players):
            self.scores += [0]

    def run(self):
        for i in range(self.s.num_turns) :
            print("=== Turn #", i+1, "===")
            for j in range(self.s.num_players):
                print("Player: ", self.users[j])
                points = self.play(j, self.s.num_of_dice, True)
				
            print ("The score at the end of turn #", i+1)
            for j in range(self.s.num_players):
                print(self.users[j], "has", self.scores[j], "points")

        if self.s.num_players == 2:
            i = 0
            while self.scores[0] == self.scores[1]:
                print("Draw!", self.scores[0],  " extra turn #", i+1, " roll single dice")
                for j in range(self.s.num_players):
                    print("Player:", self.users[j])
                    self.play(j, self.s.draw_num_of_dice, False)

            print ("The scores:")
            winner = 0
            if self.scores[0] < self.scores[1]:
                winner = 1
            print("The winner is", self.users[winner], "with", self.scores[winner], "points")
            print(self.users[1-winner], "receive", self.scores[1-winner], "points")


    def bonus(self, roll, player_number):
        if roll.len() == 2 and roll[0] == roll[1] : ### Double!! roll again:
            print("*** You rolled double and you have a bonus roll ***: ", roll[0])
			play(player_number, self.s.double_num_of_dice, False)
            return 0
        else: # Bonus
            odd = (roll[0] + roll[1]) % 2 ## 0 for even, 1 for odd
            bonus = self.s.bonus[ odd ]
            if bonus > 0:
                print("Lucky roll! you rolled", roll, "and received", bonus, " bonus points")
            elif bonus < 0:
                print("You rolled", roll, " unlucky, you lose", -bonus, " points")
            else: ## no bonus, i.e. bunus must 0
                
			self.scores[player_number] += bonus
            return bonus

    def play(self, player_number, num_of_dice, add_bonus): # i is the number of turn, j is the number of user that plays
        input(self.users[player_number] + " please press Enter to roll the dice...")
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
            print(self.users[player_number], "your score for this turn is", roll_score, "points")
            
        if self.scores[player_number] < 0:
            self.scores[player_number] = 0
		return roll_score


def test_game():
    s = GameSettings()
    g = Game(['Tom', 'Ron'], s)
    g.run()

# test_game()


### Game Users ### 
"""The following is Gameusers class
It handles all the usage of the users in the game
It stores a map of users and their <passwords, number of wins, number of losts
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
        
            
        self.s[username] = {'password':encrypt(password), 'win':0,'lost':0}
        self.store()
        return username
    
    def select_user(self):
        print ("Selecting a user:")
        username = None
        while True :
            username = input("Please type user name... (or press Enter to exist to the main menue)...")
            if len(username) < 1 :
                return None
            elif username not in self.s :
                print("Sorry, user name " + username + " does not exists" )
            else:
                break

        for i in range(3) : ## 3 attempts to enter matching password
            password = getpass.getpass("Please type the password for " + username)  ## get the password from the user
            if password == decrypt( self.s[username]['password'] ) : ## compare the password to the saved password
                return username
            print("Sorry, wrong password for user name: " + username  )
        
        return None
        
    
    def user_win(self, username):
        self.s[username]['win'] += 1
        store()
    def user_lost(self, username):
        self.s[username]['lost'] += 1
        store()
    def user_records(self):
        for username, statistic in sorted(self.s):
            print (username, "win", statistic['win'], "lost", statistic['lost'])
        
    def number_of_users(self):
        return self.s.len()



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
	if default is not None
		prompt += " [default: " + str(default) + "]"
	whilt True:
		i = input(promprt)
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
	
		
		