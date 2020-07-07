
import cmd
import textwrap
import sys
import os
import time
import random
screen_width = 100

################
# Player Setup #
################
class player:
    def __init__(self):
        self.name = ''
        self.feeling = ''
        self.astrological = ''
        self.position = 'start'
        self.won = False
        self.solves = 0
player1 = player()


#############
# Map Setup	#
#############
# a1 a2 a3 #
#----------#
#|  |  |  |# a3
#----------#
#|  |  |  |# b3
#----------#
#|  |  |  |# c3
#----------#


#Sets up constant variables
DESCRIPTION = 'description'
INFO = 'info'
PUZZLE = 'puzzle'
SOLVED = False
UP = 'up', 'up'
DOWN = 'down', 'down'
LEFT = 'left',
RIGHT = 'right',

room_solved = {'lake': False, 'start': False, 'woods': False, 'gate': False, 'town': False, 'prison': False, 'mansion': False, 'cliff': False, 'cave': False,}


zonemap = {
    # a1 # the lake
    'lake': {
        DESCRIPTION: 'You arrive at mist covered lake. A spirit emerges from the center of the water.',
        INFO: '"You have discovered my lake, in order to leave you must solve my riddle."',
        PUZZLE: 'The Lake Spirit asks:\n"Without me and within me is death assured, but within you I am life most pure. What am I?"',
        SOLVED: 'water',
        UP: 'lake',
        DOWN: 'gate',
        LEFT: 'lake',
        RIGHT: 'start'
    },
    # a2 # home
    'start': { 
        DESCRIPTION: 'This is your home.\nYou notice a golden ticket you have never seen with the word "moses" printed on it.',
        INFO: 'You see your home security system manual with the numbers:\n"6921" printed on the front.',
        PUZZLE: 'Your door is locked and will not open without a password.\nThe door requires a four-digit passcode.',
        SOLVED: '6921',
        UP: 'start',
        DOWN: 'gate',
        LEFT: 'lake',
        RIGHT: 'woods',
    },
    # a3 # the woods
    'woods': {
        DESCRIPTION: 'You have entered a large forest.\nIt is snowing heavily making it hard to walk.',
        INFO: 'You see a Yeti blocking your path and preventing you from advancing.',
        PUZZLE: 'The Yeti screams:\n"Fool! Nobody passes through my forest without answering my question."\n"What bites, yet has no teeth?"',
        SOLVED: 'frost',
        UP: 'woods',
        DOWN: 'gate',
        LEFT: 'start',
        RIGHT: 'woods',
    },
    # b1 # hebi town gate
    'gate': {
        DESCRIPTION: 'You arrive at the Hebi Town Gate and are greeted by the town guard.',
        INFO: '"Who are you? No entry allowed!" Screamed the guard.',
        PUZZLE: '"Only those who have been given the password from the golden ticket may enter."',
        SOLVED: 'moses',
        UP: 'lake',
        DOWN: 'mansion',
        LEFT: 'gate',
        RIGHT: 'town',
    },
    # b2 # hebi town square
    'town': {
        DESCRIPTION: 'You find yourself in the center of Hebi town.\nAn old man gazes at a table nearby.',
        INFO: 'You greet the old man.\nHe beckons you to look at the intricate twelve-sided table.',
        PUZZLE: 'Each side of the table has a unique symbol, though all are familar to you.\nWhich symbol do you sit by?',
        SOLVED: False,
        UP: 'start',
        DOWN: 'cliff',
        LEFT: 'gate',
        RIGHT: 'prison',
    },
    # b3 # hebi town prison
    'prison': {
        DESCRIPTION: 'You find yourself in the dark decrepit Hebi Town Prison.\nAll of the cells are open and there are no guards.',
        INFO: 'A prisoner is sitting in his cell alone, chained to wall.\nWith a terrifying smile he asks you:',
        PUZZLE: '"What belongs to you but others use it more than you do?"',
        SOLVED: ['your name','name','my name'],
        UP: 'woods',
        DOWN: 'cave',
        LEFT: 'town',
        RIGHT: 'prison',
    },
    # c1 # hebi mansion
    'mansion': { 
        DESCRIPTION: 'You enter the dark, chilling Hebi Town Mansion.\nImmediately upon entry the door is shut and locked.',
        INFO: 'The door requires a password. Printed on the door is a riddle:',
        PUZZLE: '"The more of this there is, the less you see. What is it?"',
        SOLVED: 'darkness',
        UP: 'gate',
        DOWN: 'mansion',
        LEFT: 'mansion',
        RIGHT: 'cliff',
    },
    # c2 # cliff edge
    'cliff': { 
        DESCRIPTION: 'You arrive at the edge of a cliff.\nIt appears as though the cliff leads to the abyss.',
        INFO: 'On the cliff edge you see a stone slab with the following text printed:',
        PUZZLE: 'I am the beginning of everything, the end of everywhere.\nI’m the beginning of eternity, the end of time and space. What am I?',
        SOLVED: 'e',
        UP: 'town',
        DOWN: 'cliff',
        LEFT: 'mansion',
        RIGHT: 'cave',
    },
    # c3 # world cave
    'cave': { 
        DESCRIPTION: 'You see a pitch black cave that is completly sealed off.\nAlthough you have no memory of this place, it feels... familar.',
        INFO: 'In the ground is a large key with seven notches surrounding the key.',
        PUZZLE: 'You are unable to move the key by force.',
        SOLVED: False,
        UP: 'prison',
        DOWN: 'cave',
        LEFT: 'cliff',
        RIGHT: 'cave',
    },
}


################
# Title Screen #
################
def title_screen_options():
	#Allows the player to select the menu options, case-insensitive.
	option = input("> ")
	if option.lower() == ("play"):
		setup_game()
	elif option.lower() == ("quit"):
		sys.exit()
	elif option.lower() == ("help"):
		help_menu()		
	while option.lower() not in ['play', 'help', 'quit']:
		print("Invalid command, please try again.")
		option = input("> ")
		if option.lower() == ("play"):
			setup_game()
		elif option.lower() == ("quit"):
			sys.exit()
		elif option.lower() == ("help"):
			help_menu()

def title_screen():
	#Clears the terminal of prior code for a properly formatted title screen.
	os.system('cls')
	#Prints the pretty title.
	print('#' * 45)
	print('# Welcome to this text-based puzzle RPG for #')
	print("#  Jimmy McKenney's IS 3020 Final Project!  #")
	print('#' * 45)
	print("                 .: Play :.                  ")
	print("                 .: Help :.                  ")
	print("                 .: Quit :.                  ")
	title_screen_options()


#############
# Help Menu #
#############
def help_menu():
	print("")
	print('#' * 45)
	print("Written by Jimmy McKenney from a Bryan Tong tutorial")
	print("IS 3020 - Application Development Final Project")
	print("~" * 45)
	print("Type a command such as 'move' then 'left'")
	print("to nagivate the map of a 3x3 grid.\n")
	print("Inputs such as 'look' or 'info' will")
	print("let you interact with puzzles in rooms.\n")
	print("If you move to the same location you already were")
	print("you may not move further in that direction.\n")
	print("Please ensure to type in lowercase for ease.\n")
	print('#' * 45)
	print("\n")
	print('#' * 45)
	print("    Please select an option to continue.     ")
	print('#' * 45)
	print("                 .: Play :.                  ")
	print("                 .: Help :.                  ")
	print("                 .: Quit :.                  ")
	title_screen_options()


#################
# Game Handling #
#################
quitgame = 'quit'

def print_location():
	print('\n' + ('#' * (4 +len(player1.position))))
	print('# ' + player1.position.upper() + ' #')
	print('#' * (4 +len(player1.position)))
	print('\n' + (zonemap[player1.position][DESCRIPTION]))

def prompt():
	if player1.solves == 7:
		print("Something in the world seems to have changed. Hmm...")
	print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print("What would you like to do?")
	action = input("> ")
	acceptable_actions = ['move', 'go', 'travel', 'walk', 'quit', 'inspect', 'info', 'look', 'search']
	#Forces the player to write an acceptable sign, as this is essential to solving a puzzle later.
	while action.lower() not in acceptable_actions:
		print("Unknown action command, please try again.\n")
		action = input("> ")
	if action.lower() == quitgame:
		sys.exit()
	elif action.lower() in ['move', 'go', 'travel', 'walk']:
		move(action.lower())
	elif action.lower() in ['inspect', 'info', 'look', 'search', 'examine']:
		info()

def move(myAction):
	askString = "Where would you like to "+myAction+" to?\n> "
	destination = input(askString)
	if destination == 'up':
		move_dest = zonemap[player1.position][UP]
		move_player(move_dest)
	elif destination == 'left':
		move_dest = zonemap[player1.position][LEFT]
		move_player(move_dest)
	elif destination == 'right':
		move_dest = zonemap[player1.position][RIGHT]
		move_player(move_dest)
	elif destination == 'down':
		move_dest = zonemap[player1.position][DOWN]
		move_player(move_dest)
	else:
		print("Invalid direction command, try using up, down, left, or right.\n")
		move(myAction)

def move_player(move_dest):
	print("\nYou have moved to the " + move_dest + ".")
	player1.position = move_dest
	print_location()

def info():
	if room_solved[player1.position] == False:
		print('\n' + (zonemap[player1.position][INFO]))
		print((zonemap[player1.position][PUZZLE]))
		puzzle_answer = input("> ")
		checkpuzzle(puzzle_answer)
	else:
		print("There is nothing new for you to see here.")

def checkpuzzle(puzzle_answer):
    if player1.position == 'cave':
        if player1.solves >= 7:
            endspeech = ("Without you having done anything, the cave entrance is wide open.\nIt begins to rain.\nInside the cave you see a bright light that embraces you.\nThe blinding light immobilizes you and you wake up in your bed.\nYou have saved your soul and survived!")
            for character in endspeech:
                sys.stdout.write(character)
                sys.stdout.flush()
                time.sleep(0.05)
            print("\nCONGRATULATIONS!")
            sys.exit()
        else:
            print("Nothing seems to happen still...")
    elif player1.position == 'town':
        if puzzle_answer.lower() == (player1.astrological):
            room_solved[player1.position] = True
            player1.solves += 1
            print("You have solved the puzzle. Onwards!")
            print("\nPuzzles solved: " + str(player1.solves))
    elif player1.position == 'prison':
        if puzzle_answer.lower() in (zonemap[player1.position][SOLVED]):
            room_solved[player1.position] = True
            player1.solves += 1
            print("You have solved the puzzle. Onwards!")
            print("\nPuzzles solved: " + str(player1.solves))
        else:
            print("Wrong answer! Try again.\n~~~~~~")
            info()
    else:
        if puzzle_answer.lower() == (zonemap[player1.position][SOLVED]):
            room_solved[player1.position] = True
            player1.solves += 1
            print("You have solved the puzzle. Onwards!")
            print("\nPuzzles solved: " + str(player1.solves))
        else:
            print("Wrong answer! Try again.\n~~~~~~")
            info()

def main_game_loop():
	total_puzzles = 8
	while player1.won is False:
		#print_location()
		prompt()


################
# Execute Game #
################
def setup_game():
	#Clears the terminal for the game to start.
	os.system('cls')

	#QUESTION NAME: Obtains the player's name.
	question1 = "Hello there, what is your name?\n"
	for character in question1:
		#This will occur throughout the intro code.  It allows the string to be typed gradually - like a typerwriter effect.
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.03)
	player_name = input("> ")
	player1.name = player_name

	#QUESTION FEELING: Obtains the player's feeling.
	question2 = "My dear friend " + player1.name + ", how are you feeling?\n"
	for character in question2:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.03)
	feeling = input("> ")
	player1.feeling = feeling.lower()

	#Creates the adjective vocabulary for the player's feeling.
	good_adj = ['good', 'great', 'rohit', 'happy', 'aight', 'understanding', 'great', 'alright', 'calm', 'confident', 'not bad', 'courageous', 'peaceful', 'reliable', 'joyous', 'energetic', 'at', 'ease', 'easy', 'lucky', 'k', 'comfortable', 'amazed', 'fortunate', 'optimistic', 'pleased', 'free', 'delighted', 'swag', 'encouraged', 'ok', 'overjoyed', 'impulsive', 'clever', 'interested', 'gleeful', 'free', 'surprised', 'satisfied', 'thankful', 'frisky', 'content', 'receptive', 'important', 'animated', 'quiet', 'okay', 'festive', 'spirited', 'certain', 'kind', 'ecstatic', 'thrilled', 'relaxed', 'satisfied', 'wonderful', 'serene', 'glad', 'free', 'and', 'easy', 'cheerful', 'bright', 'sunny', 'blessed', 'merry', 'reassured', 'elated', '1738', 'love', 'interested', 'positive', 'strong', 'loving']
	hmm_adj = ['idk', 'concerned', 'lakshya', 'eager', 'impulsive', 'considerate', 'affected', 'keen', 'free', 'affectionate', 'fascinated', 'earnest', 'sure', 'sensitive', 'intrigued', 'intent', 'certain', 'tender', 'absorbed', 'anxious', 'rebellious', 'devoted', 'inquisitive', 'inspired', 'unique', 'attracted', 'nosy', 'determined', 'dynamic', 'passionate', 'snoopy', 'excited', 'tenacious', 'admiration', 'engrossed', 'enthusiastic', 'hardy', 'warm', 'curious', 'bold', 'secure', 'touched', 'brave', 'sympathy', 'daring', 'close', 'challenged', 'loved', 'optimistic', 'comforted', 're', 'enforced', 'drawn', 'toward', 'confident', 'hopeful', 'difficult']
	bad_adj = ['bad', 'meh', 'sad', 'hungry', 'unpleasant', 'feelings', 'angry', 'depressed', 'confused', 'helpless', 'irritated', 'lousy', 'upset', 'incapable', 'enraged', 'disappointed', 'doubtful', 'alone', 'hostile', 'discouraged', 'uncertain', 'paralyzed', 'insulting', 'ashamed', 'indecisive', 'fatigued', 'sore', 'powerless', 'perplexed', 'useless', 'annoyed', 'diminished', 'embarrassed', 'inferior', 'upset', 'guilty', 'hesitant', 'vulnerable', 'hateful', 'dissatisfied', 'shy', 'empty', 'unpleasant', 'miserable', 'stupefied', 'forced', 'offensive', 'detestable', 'disillusioned', 'hesitant', 'bitter', 'repugnant', 'unbelieving', 'despair', 'aggressive', 'despicable', 'skeptical', 'frustrated', 'resentful', 'disgusting', 'distrustful', 'distressed', 'inflamed', 'abominable', 'misgiving', 'woeful', 'provoked', 'terrible', 'lost', 'pathetic', 'incensed', 'in', 'despair', 'unsure', 'tragic', 'infuriated', 'sulky', 'uneasy', 'cross', 'bad', 'pessimistic', 'dominated', 'worked', 'up', 'a', 'sense', 'of', 'loss', 'tense', 'boiling', 'fuming', 'indignant', 'indifferent', 'afraid', 'hurt', 'sad', 'insensitive', 'fearful', 'crushed', 'tearful', 'dull', 'terrified', 'tormented', 'sorrowful', 'nonchalant', 'suspicious', 'deprived', 'pained', 'neutral', 'anxious', 'pained', 'grief', 'reserved', 'alarmed', 'tortured', 'anguish', 'weary', 'panic', 'dejected', 'desolate', 'bored', 'nervous', 'rejected', 'desperate', 'preoccupied', 'scared', 'injured', 'pessimistic', 'cold', 'worried', 'offended', 'unhappy', 'disinterested', 'frightened', 'afflicted', 'lonely', 'lifeless', 'timid', 'aching', 'grieved', 'shaky', 'victimized', 'mournful', 'restless', 'heartbroken', 'dismayed', 'doubtful', 'agonized', 'threatened', 'appalled', 'cowardly', 'humiliated', 'quaking', 'wronged', 'menaced', 'alienated', 'wary']

	#Identifies what type of feeling the player is having and gives a related-sounding string.
	if player1.feeling in good_adj:
		feeling_string = "I am glad you feel"
	elif player1.feeling in hmm_adj:
		feeling_string = "that is interesting you feel"
	elif player1.feeling in bad_adj:
		feeling_string = "I am sorry to hear you feel"
	else:
		feeling_string = "I do not know what it is like to feel"

	#Combines all the above parts.
	question3 = "Well then, " + player1.name + ", " + feeling_string + " " + player1.feeling + ".\n"
	for character in question3:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.03)

	#QUESTION SIGN: Obtains the player's astrological sign for a later puzzle.
	question4 = "Now tell me, what is your astrological sign?\n"
	for character in question4:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.03)

	#Prints the astrological sign guide for the player.  Also converts text to be case-insensitive, as with most inputs.
	print("#####################################################")
	print("# Please print the proper name to indicate your sign.")
	print("# ♈ Aries (The Ram)")
	print("# ♉ Taurus (The Bull)")
	print("# ♊ Gemini (The Twins)")
	print("# ♋ Cancer (The Crab)")
	print("# ♌ Leo (The Lion)")
	print("# ♍ Virgo (The Virgin)")
	print("# ♎ Libra (The Scales)")
	print("# ♏ Scorpio (The Scorpion)")
	print("# ♐ Sagittarius (Centaur)")
	print("# ♑ Capricorn (The Goat)")
	print("# ♒ Aquarius (The Water Bearer)")
	print("# ♓ Pisces (The Fish)")
	print("#####################################################")
	astrological = input("> ")
	acceptable_signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
	#Forces the player to write an acceptable sign, as this is essential to solving a puzzle later.  Also stores it in class.
	
	while astrological.lower() not in acceptable_signs:
		print("That is not an acceptable sign, please try again.")
		astrological = input("> ")
	player1.astrological = astrological.lower()

	#Leads the player into the puzzle now!
	speech1 = "Ah, " + player1.astrological + ", this will be interesting.  Well then.\n"
	speech2 = "You have had your soul trapped in the world cave, " + player1.name + ".\n"
	speech3 = "How unfortunate.\n"  
	speech4 = "Oh, you've never heard of that?  Well...\n"
	speech5 = "Luckily, I believe you can find it.\nHowever, the world cave only opens to the most knowledgeable of us all.\n"
	speech6 = "Good luck, heh.. heh.. heh...\n"
	for character in speech1:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.03)
	for character in speech2:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.03)
	for character in speech3:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.04)
	for character in speech4:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	for character in speech5:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.03)
	for character in speech6:
		sys.stdout.write(character)
		sys.stdout.flush()
		time.sleep(0.05)
	time.sleep(1)

	os.system('cls')
	print("################################")
	print("# Here begins the adventure... #")
	print("################################\n")
	print("You awaken in a daze, with little recent memory.\nSeems like you are in your home.\n")
	print("You can type 'info' to get some information on your whereabouts.\nYou may also move to a new location using 'move'.\n")
	print("Is your soul really trapped?\nWhat is the 'World Cave'? I guess I should start searching...")
	main_game_loop()


title_screen()