#-------------------------------------------------------
#TELIUM - texted baced - light - commented + structured     \
#-------------------------------------------------------

#import librarys
import random
import winsound
import time

#colors
BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
#normal
RESET   = "\033[0m"




#global vars
num_modules = 17
module = 1
last_module = 0
possible_moves = []
alive = True
won = False
power = 100             #amt of power staion has
fuel = 500
locked = 0              #module locked by plr
queen = 0               #possition(module)
vent_shafts = []        #location of vent entrances
info_panels = []        #location of info panels
workers = []            #location of woker aliens
module_name = ""

#file locations
TYPEsound = r"typing.wav"



def TitleScreen():
    global user_option

    print(f"{BLUE}-{BLUE}" * 20)
    print("Welcome to Telium")
    print(f"{BLUE}-{BLUE}" * 20)
    print(f"{WHITE}-{WHITE}" * 20)

    print(f"{GREEN}PLAY -> (p){GREEN}")
    print(f"{CYAN}INSTRUCTIONS -> (z){CYAN}")
    print(f"{BLACK}QUIT -> (q){BLACK}")
    print(f"{WHITE}-{WHITE}" * 20)
    print(f"{RESET} {RESET}")

    user_option = input(" Enter your choise _>").lower()
    if user_option == "p":
        print("Starting game...")
        return
    elif user_option == "z":
        print(f"{WHITE}sorry!, there are curently no instructions our solo dev team \n is working on it {WHITE}")
    elif user_option == "q":
        print("Bye..")
        quit()

TitleScreen()


#procedure declarations
def load_module():
    global module, possible_moves
    possible_moves = get_modules_from(module)
    output_module()

def get_modules_from(module):
    global module_name
    moves = []
    text_file = open(f"Charles_Darwin\\module{module}.txt","r")
    lines = text_file.readlines()


    #iteration to read the modules possible moves to ajacent rooms
    for counter in range(4):
        move_read = int(lines[counter].strip())                                                  #strip() -> removes spaces ect
        if move_read != 0:
            moves.append(move_read)
            module_name = lines[4].strip()
    text_file.close()
    return moves

def output_module():
    global module
    print()
    print("-" * 60)
    print()
    print("You are in module", module, "This is the", module_name, "room")
    print()

def output_moves():
    global possible_moves
    print()
    print("From here you can move to modules:",end = '')                                         # adds couser at end of line , with space
    for moves in possible_moves:
        print(moves, '', end = '')
    print()
   
def get_action():                                                                                
    global module, last_module, possible_moves, power                                            #make these vars global (acsssable to all)
    valid_action = False
    while valid_action == False:                                                                 #iteration to give user move options
        print("What do you want to do next? [MOVE] [SCANNER] [L -> MAP]")
        action = input(">").lower()                                                              #can enter MOVE and move

        if action.startswith("move") or action.startswith("m"):                                  # and abriviation
            move_text = action.replace("move", "").replace("m", "").strip()

            if move_text.isdigit():                                                              #if user typed MOVE 2
                move = int(move_text)
            else:
                move = int(input("Enter module number to move to: "))                            #fallback

            if move in possible_moves:                                                           #check if input is a valid move (if in the file's table, possible_moves)
                power -= 1                                                                       #subs 1 from power var every move
                valid_action = True
                last_module = module                                                             #update last module to the current
                module = move                                                                    #update module to the users imputed valid modle
            else:
                print("The module must be connected to the module you are currently in.")        #error checking if module inputed is not valid

        elif action == "l":
            show_map()



def typeLine(line):
    for letter in line:
        print(letter, end="", flush=True)
        time.sleep(0.0005)

def show_map():
    winsound.PlaySound(TYPEsound, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

    with open("MAP.txt", "r", encoding="utf-8") as mapfile:
        for line in mapfile:
            target = f"{module:02d}"      # ALWAYS two digits: 01, 02, 07, 12

            if target in line:
                line = line.replace(target, f"{RED}👨{RESET}")   # marker inside the box, same width

            typeLine(line)

    winsound.PlaySound(None, 0)



#MAIN PROGRAME
while alive and not won:                                                                         #iteration to loop while playuer is not dead or won
    load_module()                                                                                #call load_module() func
    if won == False and alive == True:                                                           #if player is alive feed the game loop
        output_moves()
        get_action()

if won == True:                                                                                  #checks if player wins or dies displaying win/death text
    print("The queen is traped and you burn it to death with your flamethrower. ")
    print("Game over, YOU WIN")

if alive == False:
    print("The station lost power unable to sustain life suport, you die. ")
    print("Game over, YOU LOST")