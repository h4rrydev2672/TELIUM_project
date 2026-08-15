#-------------------------------------------------------
#TELIUM - texted baced - light - commented + structured  
#-------------------------------------------------------

##INFORMATION##------------------------------------------------
#not able to use on mac due to winsound library -> 
# remove winsound and sound effects to make it work on mac 
#--------------------------------------------------------------


#import librarys
import random
#import winsound
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
num_modules = 12
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

def spawn_npcs():
    global num_modules, queen, vent_shafts, info_panels, workers                                #make these vars global (acsssable to all)
    modules_set = []                                                                            #table to hold all modules (except module 1, where the player starts)

    for counter in range(2, num_modules + 1):                                                   #iteration to loop through all modules except module 1
        modules_set.append(counter)                                                             #add all modules to a list 
    random.shuffle(modules_set)                                                                 #shuffle the list of modules
    i = 0
    queen = modules_set[i]                                                                      #assign queen to a random module from the shuffled list

    for counter in range(1, 3):                                                                 #iteration to loop through 2 vent shafts
        i = i + 1
        vent_shafts.append(modules_set[i])                                                      #assign vent shafts to random modules from the shuffled list

    for counter in range(3, 5):                                                                 #loop to add 2 random info panles
        i = i + 1
        info_panels.append(modules_set[i])                                                      #assing randomly

    for counter in range(0, 3):                                                                 #loop to add 3 random workers
        i = i + 1                                                                               
        workers.append(modules_set[i])                                                          #added them ranomly


def TitleScreen():
    global user_option

    print(f"{BLUE}-{BLUE}" * 20)                                                                #titlescean design
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

def check_vent_shafts():
    global num_modules, module, vent_shafts, fuel, current_module, last_module
    fuel_table = [20, 30, 40, 50]                                                                    #table of fuel amounts
    if module in vent_shafts :                                                          
        print("There is a bank of fuel cells here.")
        print("You can laad them into your famethrower.")                                            #picks a random amount of fuel from the fuel_table and adds it to the players current fuel
        fuel_gained = random.choice(fuel_table)                                                      #randomly select a fuel amount from the table
        print("Fule was", fuel, "now reading", fuel + fuel_gained)
        fuel = fuel + fuel_gained
        print("The doors suddenly lock shut.")
        print("What is happening to the station?")
        print("our only escape is to climb into the vent and move to another module.")
        print("We have no idea where we are going.")
        print("We follow the passage and find ourselvs sliding down.")

        last_module = module
        module = random.randint(1, num_modules)
        while module == last_module or module in vent_shafts:
            module = random.randint(1, num_modules)

        print("We have arrived in module", module)



#procedure declarations
def load_module():
    global module, possible_moves
    possible_moves = get_modules_from(module)
    output_module()

def get_modules_from(module):
    global module_name
    moves = []
    # text_file = open(f"Charles_Darwin\\module{module}.txt","r")    #FOR WINDOWS USE
    text_file = open(f"Charles_Darwin/module{module}.txt", "r")      #FOR MAC USE
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

    if module == queen:                                                                         #if the player is in the same module as the queen
        queen_responcese = ["The queen is here, it looks very angry.",                          
                            "The queen is here, it looks very hungry.",
                            "The queen is here, it looks very dangerous."]
        print(random.choice(queen_responcese))                                                 #print one of 3 responce from table

    if module in vent_shafts:                                                                   #if the player is in the same module as a vent shaft
        vent_responcese = ["There is a vent shaft here.",
                            "You can use  a vent to move to another module.",
                            "You can feel cold air coming from a vent."]
        print(random.choice(vent_responcese))                                                   #print one of 3 responce from table

    if module in workers:                                                                       #if the player is in the same module as a worker
        worker_responcese = ["There is a worker here.",
                            "You can hear a worker moving around.",
                            "You can see a worker moving around."]
        print(random.choice(worker_responcese))                                                 #print one of 3 responce from table

    print()


def output_moves():
    global possible_moves
    print()
    print("From here you can move to modules:",end = '')                                         # adds couser at end of line , with space
    for moves in possible_moves:
        print(moves, '', end = '')
    print()


def lock(module_to_lock=None):
    global num_modules, power, locked, queen                                                       # make these globals available inside the function

    # Determine which module to lock (prompt if no argument supplied)
    if module_to_lock is None:
        try:
            new_lock = int(input("Enter the module number to lock: "))                             # ask the player for a module number
        except ValueError:
            print("Invalid input: please enter a number.")                                          # handle non-numeric input
            return                                                                                  # abort on invalid input
    else:
        new_lock = int(module_to_lock)                                                              # use provided argument (e.g. lock(5))

    # Validate module range (modules are numbered 1..num_modules)
    if new_lock < 1 or new_lock > num_modules:
        print("Invalid module number, operation not permitted.")                                    # out-of-range modules not allowed
        return

    # Disallow locking the queen module
    if new_lock == queen:
        print("You cannot lock the module with the queen in it.")                                   # cannot lock the queen's module
        return

    # Already locked?
    if new_lock == locked:
        print("Module", new_lock, "is already locked, you cannot lock it again.")                   # inform if module is already locked
        return

    # Lock it
    locked = new_lock                                                                                # set the locked module
    print("Aliens cannot enter module", locked, "anymore.")                                          # feedback to player

    # Use power for the lock operation and report it
    power_used = 25 + 5 * random.randint(0, 5)                                                       # random power cost formula
    power -= power_used                                                                              # subtract used power from total
    print("Power used:", power_used, "Power remaining:", power)                                      # show power consumption and remaining


def get_action():
    global module, last_module, possible_moves, power                                                # make game state vars accessible

    valid_action = False                                                                              # loop until a valid action is taken
    while not valid_action:
        print("What do you want to do next? [MOVE] [SCANNER] [L -> MAP] [LOCK]")                      # prompt options
        action = input(">").lower().strip()                                                           # read player input, normalize

        # MOVE handling (supports "move 2", "m2", "m 2", or entering only the destination after "move")
        if action.startswith("move") or action.startswith("m"):
            move_text = action.replace("move", "", 1).replace("m", "", 1).strip()                     # strip command to get number
            if move_text.isdigit():
                move = int(move_text)                                                                 # parse direct number e.g. "m2"
            else:
                try:
                    move = int(input("Enter module number to move to: "))                             # fallback prompt
                except ValueError:
                    print("Invalid module number.")                                                   # invalid fallback input
                    continue

            if move in possible_moves:
                power -= 1                                                                            # moving costs 1 power
                valid_action = True                                                                   # accept action and break loop
                last_module = module                                                                  # update last module
                module = move                                                                         # update current module
                check_vent_shafts()                                                                   # process vent effects after move
            else:
                print("The module must be connected to the module you are currently in.")             # invalid move (not adjacent)
            continue                                                                                  # go back to top of action loop

        # LOCK handling: supports "lock 5", "lock5", "l5", "l 5". Single "l" is map (see below).
        if action.startswith("lock") or (action.startswith("l") and action != "l"):
            if action.startswith("lock"):
                lock_text = action[len("lock"):].strip()                                              # get trailing digits from "lock5" or "lock 5"
            else:
                lock_text = action[1:].strip()                                                        # get trailing digits from "l5" or "l 5"

            if lock_text.isdigit():
                module_to_lock = int(lock_text)                                                       # convert to int and lock
                lock(module_to_lock)
            else:
                lock()                                                                                 # no number given -> prompt inside lock()
            continue                                                                                   # loop for next action

        # Single-letter 'l' shows the map
        if action == "l":
            show_map()                                                                                 # l alone displays the map
            continue                                                                                   # return to action prompt

        # SCANNER handling
        if action == "scanner" or action == "s":
            command = input("Scanner ready, Enter command (LOCK), (POWER): ").lower().strip()          # scanner options
            if command == "lock":
                lock()                                                                                 # scanner lock -> prompt for module
            elif command == "power":
                print("Power remaining:", power)                                                       # show power via scanner
            else:
                print("Unknown scanner command.")                                                      # invalid scanner command
            continue                                                                                   # go back to action loop

        print("Unknown action. Try MOVE, LOCK, SCANNER, or L (map).")                                   # fallback for bad action input



def typeLine(line):
    for letter in line:
        print(letter, end="", flush=True)
        time.sleep(0.0005)

def show_map():
    #winsound.PlaySound(TYPEsound, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)

    with open("MAP.txt", "r", encoding="utf-8") as mapfile:
        for line in mapfile:
            target = f"{module:02d}"                                                            # ALWAYS two digits: 01, 02, 07, 12

            if target in line:
                line = line.replace(target, f"{RED}👨{RESET}")                                  # marker inside the box, same width

            typeLine(line)

    #winsound.PlaySound(None, 0)



#MAIN PROGRAME
spawn_npcs()                                                                                   #call spawn_npcs() func to spawn the npcs in random modules
print("Queen is located in module", queen)
print("Vent shafts are located in modules", vent_shafts)
print("Info panels are located in modules", info_panels)
print("Workers are located in modules", workers)

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

#updated version 1.0.1