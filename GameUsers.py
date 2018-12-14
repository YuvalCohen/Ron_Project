
from pathlib import Path
import pickle
import getpass
import game

def encrypt (s): ## I don't know how to encrypt or decrypt
    return s
def decrypt (s): ## I don't know how to encrypt or decrypt
    return s

    
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
    def user_statistics(self):
        for username, statistic in sorted(self.s):
            print (username, "win", statistic['win'], "lost", statistic['lost'])
        
    def user_number(self):
        return self.s.len()

def test_GameUsers() :
    gu = GameUsers()
    u3 = gu.select_user()
    u4 = gu.select_user()
    print ([u3, u4])
    if u3 and u4 and u3 != u4:
        game.Game([u3, u4], game.GameSettings() ).run()
        


test_GameUsers()

