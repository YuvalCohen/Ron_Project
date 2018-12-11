
import random
import getpass



class GameSettings:
    def __init__(self):
        self.cube_size = 6
        self.num_turns = 5
        self.bonus = [10, -5] # 10 points bunus for even rolls, -5 penalty for odd rolls
        self.num_users = 2
        self.num_of_dice = 2 # the number of dice to roll at each turn
        self.double_num_of_dice = 1 # the number of dice to roll when double
        self.draw_num_of_dice = 1 # the number of dice to roll after the main game ended at draw
         

class Game:
    def __init__(self, users, settings):
        self.users = users 
        self.s = settings
        self.scores = []
        for i in range(settings.num_users):
            self.scores += [0]

    def run(self):
        for i in range(self.s.num_turns) :
            print("=== Turn #", i+1, "===")
            for j in range(self.s.num_users):
                print("Player: ", self.users[j])
                self.play(j, self.s.num_of_dice)
            print ("The score at the end of turn #", i+1)
            for j in range(self.s.num_users):
                print(self.users[j], "has", self.scores[j], "points")

        if self.s.num_users == 2:
            i = 0
            while self.scores[0] == self.scores[1]:
                print("Draw!", self.scores[0],  " extra turn #", i+1, " roll single dice")
                for j in range(self.s.num_users):
                    print("Player:", self.users[j])
                    self.play(j, 1)

            print ("The scores:")
            winner = 0
            if self.scores[0] < self.scores[1]:
                winner = 1
            print("The winner is", self.users[winner], "with", self.scores[winner], "points")
            print(self.users[1-winner], "receive", self.scores[1-winner], "points")


    def bonus(self, roll, player_number):
        if roll[0] == roll[1] : ### Double!! roll again:
            print("*** You rolled double ***: ", roll[0])
            print(self.users[player_number], "please press Enter to roll an extra dice...")
            input()
            r = random.randint(1, self.s.cube_size)
            print("You rolled:", r)
            return r
        else: # Bonus
            odd = (roll[0] + roll[1]) % 2 ## 0 for even, 1 for odd
            bonus = self.s.bonus[ odd ]
            if bonus > 0:
                print("Lucky roll! you rolled", roll, "and received", bonus, " bonus points")
            elif bonus < 0:
                print("You rolled", roll, " unlucky, you lose", -bonus, " points")
            else: ## no bonus, i.e. bunus must 0
                print("You rolled:", roll)
            return bonus

    def play(self, player_number, num_of_dice): # i is the number of turn, j is the number of user that plays
        print(self.users[player_number], "please press Enter to roll the dice...")
        input()
        roll = []
        roll_score = 0
        for i in range (num_of_dice):
            r = random.randint(1, self.s.cube_size)
            roll_score += r
            roll +=  [ r ]
        if num_of_dice == 2:
            roll_score += self.bonus(roll, player_number)
            print(self.users[player_number], "your score for this turn is", roll_score, "points")
        else:
            print("You rolled:", roll)
                
        self.scores[player_number] += roll_score
        if self.scores[player_number] < 0:
            self.scores[player_number] = 0



def main():
    s = GameSettings()
    g = Game(['Tom', 'Ron'], s)
    g.run()

pswd = getpass.getpass('Password:')
print ("printing")
print (pswd)
main()

