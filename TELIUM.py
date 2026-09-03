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
BLACK   = "\033[30m"    #locks 
RED     = "\033[31m"    #warniings 
GREEN   = "\033[32m"    #notifications
YELLOW  = "\033[33m"    #queen
BLUE    = "\033[34m"    #vents 
MAGENTA = "\033[35m"    #move 
CYAN    = "\033[36m"    #info panels
WHITE   = "\033[37m"    #defult/info 
ORANGE  = "\033[38;5;208m" #worker aliens
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
        print(f"{GREEN}-{GREEN}" * len("Starting game..."))                                        #added same approche 
        print("Starting game...")
        print(f"{GREEN}-{RESET}" * len("Starting game..."))
        print(" \n ")

        return

    elif user_option == "z":
        print(f"{WHITE}-{WHITE}" * 100)
        print(f"{WHITE}Here are the simple instructions for Telium:{WHITE}")
        print()
        print(f"{WHITE}Your goal is to trap and defeat the alien Queen. Explore the station, manage your resources, and survive.")
        print(f"{WHITE}Move (M): Travel between connected modules.")
        print(f"{WHITE}Lock (L): Lock a module to trap the Queen or block aliens (costs power).")
        print(f"{WHITE}Scanner (S): Check your power or scan adjacent modules for aliens, vents, or info panels (costs 25 power).")
        print(f"{WHITE}Map: Type L to view the station map and your current location.")
        print()
        print(f"{GREEN}Gameplay Elements{WHITE}")
        print(f"{WHITE}The Queen: The main threat. If you trap her in a module with no escape routes,you will enter a boss fight.\n You need at least 100 fuel to start the fight, and each shot costs 25 fuel.")
        print(f"{WHITE}Worker Aliens: These will attack you. You can use a short blast of your flamethrower to scare them away,\n a long blast to kill them, or attempt to run back to the previous module.")
        print(f"{WHITE}Vent Shafts: These contain fuel cells for your flamethrower \nbut will randomly transport you to another module when you enter them.")
        print(f"{WHITE}Info Panels: Use these to reveal the Queen's location on your map.")
        print()
        print(f"{GREEN}Tips for Survival{WHITE}")
        print(f"{WHITE}Watch your Power: Moving and locking doors drains the station's power.")
        print(f"{WHITE}Conserve Fuel: You need fuel to defend yourself from workers and to defeat the Queen. Don't waste it!")
        print(f"{WHITE}Listen to your Intuition: You will receive warnings about what is in adjacent modules before you enter them. {WHITE}")
        print(f"{WHITE}-{RESET}" * 100)
        print(" \n ")

    elif user_option == "q":
        print(f"{WHITE}-{WHITE}" * len("Bye.."))                                                    #trying smt difrent with len()
        print("Bye..")
        print(f"{WHITE}-{RESET}" * len("Bye.."))
        quit()

TitleScreen()

def check_vent_shafts():
    # Removed undefined current_module from global list
    global num_modules, module, vent_shafts, fuel, last_module
    fuel_table = [20, 30, 40, 50]                                                                    #table of fuel amounts
    if module in vent_shafts :
        print(f"{BLUE}-{RESET}" * 40)                                                        
        print("There is a bank of fuel cells here.")
        print("You can laad them into your famethrower.")                                            #picks a random amount of fuel from the fuel_table and adds it to the players current fuel
        print(f"{BLUE}-{RESET}" * 40)
        fuel_gained = random.choice(fuel_table)                                                      #randomly select a fuel amount from the table)
        print(f"Fule was{GREEN}{fuel}{RESET}, now reading {GREEN}{fuel + fuel_gained}{RESET}")
        fuel = fuel + fuel_gained
        print(f"{BLUE}-{RESET}" * 70)
        print("The doors suddenly lock shut..  What is happening to the station?")
        print(f"our only escape is to climb into the {BLUE}vent{RESET} and move to another module.")
        print("We have no idea where we are going.")
        print("We follow the passage and find ourselvs sliding down.")
        print(f"{BLUE}-{RESET}" * 70)

        last_module = module
        module = random.randint(1, num_modules)
        while module == last_module or module in vent_shafts:
            module = random.randint(1, num_modules)
        print(f"{WHITE}-{WHITE}" * 40)
        print("We have arrived in module", module)
        print(f"{WHITE}-{RESET}" * 40)

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

    # read first 4 lines as move numbers
    for counter in range(4):                                                                     ##iteration to read the modules possible moves to ajacent rooms
        move_read = int(lines[counter].strip())                                                  #strip() -> removes spaces ect
        if move_read != 0:
            moves.append(move_read)

    # set module_name from line 5 (index 4) after reading moves
    if len(lines) > 4:
        module_name = lines[4].strip()
    else:
        module_name = ""
    text_file.close()
    return moves

def move_queen():
    global num_modules, module, last_module, locked, queen, won, vent_shafts, fuel
    
    if module == queen:                                                                         # if the player is in the same module as the queen
        print(f"{YELLOW}-{RESET}" * 40)
        print("The queen is here, it looks very angry.")
        print(f"{YELLOW}-{RESET}" * 40)
        
        moves_to_make = random.randint(1, 3)                                                   # decides how many moves the queen takes
        moves_to_make = 1
        can_move_to_last_module = False                                                        # makes player not able to go to last module
        
        while moves_to_make > 0:                                                               # while there are moves available do..
            escapes = get_modules_from(queen)                                                  # gets possible moves for queen module

            if module in escapes:
                escapes.remove(module)                                                         # if module is escape remove it

            if last_module in escapes and not can_move_to_last_module:
                escapes.remove(last_module)                                                    # lets queen double back behind us from another module

            if locked in escapes:
                escapes.remove(locked)                                                         # remove modules that are locked as escapes

            if len(escapes) == 0:
                print("Starting boss fight, -- you need at least 100 fuel in your flame thrower, ready?")
                
                if fuel < 100:
                    print("You don't have enough fuel, you get killed.")
                    won = False
                    return
                else:
                    print("Enter the appropriate direction, 'up', 'down', 'left', 'right'.")
                    user_input = input("Enter 'YES' to continue: ").strip().lower()
                    
                    if user_input != 'yes':
                        print("You hesitated...")
                        won = False
                        return

                    for i in range(3, -1, -1):                                                  # Fixed: step must be -1, not 0
                        time.sleep(1)                                                           # Fixed: Changed 100 to 1 for a reasonable countdown
                        print(i)
                    print("GO!")

                    queen_outcomes = {
                        "Queen crawls on to the ceiling, where do you shoot?": "up",
                        "Queen scutters to the left wall, where do you shoot?": "left",
                        "The queen hugs the east wall, where do you shoot?": "right",
                        "The queen lays low to the ground, where do you shoot?": "down"}

                    while queen_outcomes:
                        random_key = random.choice(list(queen_outcomes.keys()))
                        correct_answer = queen_outcomes[random_key]

                        print(random_key)
                        player_input = input("Options: up, down, left, right | needed fule to shoot is 25 ").strip().lower()
                        fuel = fuel - 25
                        if player_input == correct_answer:
                            print(f"Good shot! | fuel remaining:{fuel}")
                            del queen_outcomes[random_key]
                        else:
                            print("You missed!")
                            won = False
                            return

                won = True                                                                      # if queen is trapped and defeated, player wins
                moves_to_make = 0
                print("...and the door is locked. The queen is trapped.")

            else:
                if moves_to_make == 1:                                                          # otherwise move queen to another module
                    print("...Queen alien has escaped.")
                
                queen = random.choice(escapes)
                moves_to_make = moves_to_make - 1
                can_move_to_last_module = True

                while queen in vent_shafts:                                                     # handles when queen is in vent shaft module
                    if moves_to_make > 1:
                        print("You hear scuttling above your head. The queen escaped via vent shaft.")
                    
                    valid_move = False
                    while not valid_move:
                        valid_move = True
                        queen = random.randint(1, num_modules)
                        if queen in vent_shafts:
                            valid_move = False
                    
                    moves_to_make = 0                                                           # stops queen from moving through shaft

def output_module():
    global module
    print()
    print(f"{BLACK}-{RESET}" * 160)
    print()
    print("You are in module", module, "This is the", module_name, "room")

    if module == queen:                                                                         #if the player is in the same module as the queen
        queen_responcese = [f"The {YELLOW}queen{RESET} is here, it looks very angry.",                          
                            f"The {YELLOW}queen{RESET} is here, it looks very hungry.",
                            f"The {YELLOW}queen{RESET} is here, it looks very dangerous."]
        print(random.choice(queen_responcese))                                                  #print one of 3 responce from table

    if module in vent_shafts:                                                                   #if the player is in the same module as a vent shaft
        vent_responcese = [f"There is a {BLUE}vent shaft{RESET} here.",
                            f"You can use  a {BLUE}vent{RESET} to move to another module.",
                            f"You can feel {BLUE}cold air{RESET} coming from a vent."]
        print(random.choice(vent_responcese))                                                   #print one of 3 responce from table

    if module in workers:                                                                       #if the player is in the same module as a worker
        worker_responcese = [f"There is a {ORANGE}worker{RESET} here.",
                            f"You can hear a {ORANGE}worker{RESET} moving around.",
                            f"You can see a {ORANGE}worker{RESET} moving around."]
        print(random.choice(worker_responcese))                                                 #print one of 3 responce from table

    print()

def output_moves():
    global possible_moves
    print()
    print("From here you can move to modules:",end = '')                                         # adds couser at end of line , with space
    for moves in possible_moves:
        print(moves, '', end = '')
    print()

def lock(module_to_lock = None):
    global num_modules, power, locked, queen                                                      # make these globals available inside the function

    if module_to_lock is None:                                                                    #check if module_to_lock is provided, if not ask the user for input
        new_lock_str = input("Enter the module number to lock: ")                               
        if not new_lock_str.isdigit():                                                            #chesks if its valid numb                                          
            print(f"{RED}Invalid input: please enter a number.{RESET}")
            return
        new_lock = int(new_lock_str)                                                              #set new_lock to the user input
    else:
        new_lock = int(module_to_lock)                                                            #fallback to the provided module_to_lock if it is not None

    if new_lock < 1 or new_lock > num_modules:                                                    #check if the module number is valid
        print(f"{RED}Invalid module number, operation not permitted.{RESET}")
        return                                                                                    #continue to the next iteration of the loop if the module number is invalid

    if new_lock == queen:                                                                         #dont allow locking the module with the queen in it
        print(f"{RED}You cannot lock the module with the queen in it.{RESET}")
        return                                                                                    #fallback to the next iteration of the loop if the module number is invalid

    if new_lock == locked:                                                                        #if
        print(f"{RED}Module {new_lock} is already locked, you cannot lock it again.{RESET}")
        return                                                                                    #fallback to the next iteration of the loop if the module number is invalid

    locked = new_lock                                                                             #lock the module by setting the locked variable to the new_lock value
    print(f"{RED}Aliens cannot enter module {locked} anymore.{RESET}")

    power_used = 25 + 5 * random.randint(0, 5)                                                    #calculate the power used to lock the module, with a random component
    power -= power_used
    print(f"Power used: {GREEN}{power_used}{RESET}, Power remaining: {GREEN}{power}{RESET}")

def worker_aliens():
    import random

    global module, last_module, workers, fuel, alive
    if module in workers:                                                                        # if the player is in the same module as a worker
        print(f"{ORANGE}-{RESET}" * 60)
        print("A young worker alien is here, it tries to leap at you.")
        print(f"{ORANGE}-{RESET}" * 60)

        successful_attack = False   
        while not successful_attack:                                                            # loop until the player defends or dies
            print(f"{BLACK}-{RESET}" * 80)                                                      #opption menue
            print(f"{WHITE}You can:{BLACK}")
            print(" ")
            print(f"{ORANGE}- Short blast your flamethrower to frighten it away.{RESET}")
            print(" ")
            print(f"{RED}- Long blast your flamethrower to try to kill it.{RESET}")
            print(" ")
            print("- RUN, you return to previous module")
            print(" ")
            print(f"{WHITE}How will you react?{RESET}")
            print(f"{BLACK}-{RESET}" * 80)

            action = ""
            while action not in ("s", "l", "run"):                                             #check approriate input
                action = input("Press the trigger > ").lower().strip()

            if action == "run":
                if last_module in vent_shafts:
                    chance_of_capture = 0.5                                                  # 50% default; change this value to tune risk
                    if random.random() < chance_of_capture:
                        print(f"The {ORANGE}worker alien{RESET} catches you in the vent shaft and kills you.")
                        alive = False
                        return
                    else:
                        print(f"You manage to escape the {ORANGE}worker alien{RESET} through the vents and make it back to the previous module.")
                        module = last_module
                        return
                else:
                    print(f"You run back to the previous module, leaving the {ORANGE}worker alien{RESET} behind.")
                    module = last_module
                    return


            fuel_used = int(input("How much fuel do you want to use?...> "))

            if fuel_used > fuel:
                alive = False
                print("You tried to use more fuel than you have and collapsed.")
                return
            if action == "s":
                fuel_needed = 10 + 10 * random.randint(0, 30)
            else:  
                fuel_needed = 30 + 10 * random.randint(0, 3)
            fuel -= fuel_used
            if fuel_used >= fuel_needed:
                successful_attack = True
            else:
                print(f"The {ORANGE}worker alien{RESET} squeals but is not dead... it's angry.")

        if action == "s":
            print(f"The {ORANGE}worker alien{RESET} scuttles away into the corner of the room.")
        elif action == "l":
            print(f"The {ORANGE}worker alien{RESET} is dead and destroyed.")
            if module in workers:
                workers.remove(module)
            print()

def get_action():
    
    global module, last_module, possible_moves, power                                               # make game state vars accessible

    #MOVE HANDLEING

    valid_action = False                                                                             # loop until a valid action is taken
    while not valid_action:
        print(f"What do you want to do next? {MAGENTA}MOVE{RESET}, {BLACK}LOCK{RESET}, {WHITE}SCANNER{RESET}, or L (map).{RESET}")
        print(f"{BLACK}-{RESET}" * 160)
        action = input(">").lower().strip()                                                         # all input valid 

        if action.startswith("move") or action.startswith("m"):                                      #allowing 'm' as a shorthand for 'move'
            move_text = action.replace("move", "", 1).replace("m", "", 1).strip()                    
            if move_text.isdigit():
                move = int(move_text)
            else:
                move_input = input("Enter module number to move to: ")
                if not move_input.isdigit():                                                        #dont allow non-numeric input for module number
                    print(f"{RED}Invalid module number.{RESET}")
                    continue
                move = int(move_input)

            if move in possible_moves:                                                             #check if the move is valid (i.e., the module is adjacent to the current module)
                power -= 1                                                                         #decrease power by 1 for moving
                valid_action = True                                                                #udtate a bunch or vars 
                last_module = module
                module = move
                check_vent_shafts()
            else:
                print(f"{RED}The module must be connected to the module you are currently in.{RESET}")
            continue

        #LOCK HANDLEING

        if action.startswith("lock") or (action.startswith("l") and action != "l"):               #allowing 'l' as a shorthand for 'lock', but not for the map command              
            if action.startswith("lock"):                                                           
                lock_text = action[len("lock"):].strip()                                          #allow for 'lock' followed by a module number
            else:
                lock_text = action[1:].strip()                                                    #allow for 'l' followed by a module number

            if lock_text.isdigit():                              
                module_to_lock = int(lock_text)                 
                lock(module_to_lock)
            else:
                lock()                                                                            #call function 
            continue

        if action == "l":                                                                         #if preesed call func show_map() to display the map   
            show_map(show_queen = False)                                                            # show standard map: player + locked module only
            continue

        # SCANNER HANDLEING

        if action == "scanner" or action == "s":                                                 #allowing 's' as a shorthand for 'scanner'
            command = input("Scanner ready, Enter command (LOCK), (POWER), (SCAN): ").lower().strip()    #allows abriviated commands for scanner
            if command == "lock":
                lock()
            elif command == "power":
                print(f"Power remaining: {GREEN}{power}{RESET}")
            elif command == "scan":
                print(f"{BLACK}-{RESET}" * 40)
                module_to_scan = input("Enter module number to scan: ").lower().strip()
                print(f"{BLACK}-{RESET}" * 40)
                power = power - 25
                print(f"{GREEN}-{RESET}" * 40)
                print(f"Power used: {GREEN}25{RESET}, Power remaining: {GREEN}{power}{RESET}")
                print(f"{GREEN}-{RESET}" * 40)
                print(" ")
                if module_to_scan.isdigit():
                    module_to_scan = int(module_to_scan)
                    if module_to_scan == queen:
                        print(f"{YELLOW}The queen is in module {module_to_scan}.{RESET}")
                        print(" ")
                    elif module_to_scan in workers:
                        print(f"{ORANGE}A worker alien is in module {module_to_scan}.{RESET}")
                        print(" ")
                    elif module_to_scan in vent_shafts:
                        print(f"{BLUE}A vent shaft is in module {module_to_scan}.{RESET}")
                        print(" ")
                    elif module_to_scan in info_panels:
                        print(f"{CYAN}An info panel is in module {module_to_scan}.{RESET}")
                        print(" ")
                    else:
                        print(f"{RED}-{RESET}" * 40)
                        print(f"{WHITE}Module {module_to_scan} is empty.{RESET}")
                        print(f"{RED}-{RESET}" * 40)
                        print(" ")
            else:
                print(f"{RED}Unknown scanner command.{RESET}")
            continue                                                                            #allow to continue

        print(f"{RED}Unknown action.{RESET}")
        print(f"{MAGENTA}MOVE{RESET}, {BLACK}LOCK{RESET}, {WHITE}SCANNER{RESET}, or L (map).{RESET}")

def typeLine(line):
    for letter in line:
        print(letter, end="", flush=True)
        time.sleep(0.0005)

def show_map(show_queen: bool = False):
    global module, queen, locked

    player_str = f"{module:02d}"
    queen_str = f"{queen:02d}"
    locked_str = f"{locked:02d}" if locked != 0 else None

    #winsound.PlaySound(TYPEsound, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
    try:                                                                                            #attempt to open the MAP.txt file and read its contents, 
                                                                                                    #replacing placeholders with colored symbols for player, queen, and locked module
        with open("MAP.txt", "r", encoding="utf-8") as mapfile:
            for line in mapfile:
                out_line = line

                out_line = out_line.replace(player_str, f"{RED}👨{RESET}")                          # Replace player 

                if locked_str:
                    out_line = out_line.replace(locked_str, f"{YELLOW}🔒{RESET}")                   #replace locked module

                if show_queen:
                    out_line = out_line.replace(queen_str, f"{YELLOW}👑{RESET}")                    ## Reveal queen only when requested (info panel)

                typeLine(out_line)
    except FileNotFoundError:
        print(f"{RED}MAP.txt not found in the current directory. Place a MAP.txt file next to TELIUM.py.{RESET}")
    #winsound.PlaySound(None, 0)

def Check_info_panels():
    global module, info_panels
    if module in info_panels:
        print(f"{CYAN}-{RESET}" * 80)
        print("You see a flickering light from an info panel.")
        print("You can use the info panel to get information about the station. and the queens location.")
        print(f"{CYAN}-{RESET}" * 80)
        user_input = input("Do you want to use the info panel? (yes/no): ").strip().lower()
        if user_input == "yes":
            print(f"{CYAN}-{RESET}" * 100)
            print("You access the info panel and find a map of the station.")
            print("The map shows the layout of the modules and the location of the queen.")
            show_map(show_queen=True)                                                          #reveal queen when using the info panel
            print(f"{CYAN}-{RESET}" * 100)
        
def intuition():
    global possible_moves, workers, vent_shafts, queen, info_panels
    worker_responses = ["worker alien moving around", "You hear a worker alien scuttling", "You see a worker alien moving"]
    vent_shafts_responses = ["You feel cold air coming from a vent", "You hear a vent shaft whirring", "You see a vent shaft nearby"]
    info_panels_responses = ["You see a flickering light from an info panel", "You hear a faint hum from an info panel", "You see a flickering light from an info panel"]
    queen_responses = ["You feel a strong presence of the queen", "You hear a faint scuttling sound", "You see a shadow moving in the distance"]

    for connected_module in possible_moves:
        if connected_module in workers:                                                        #print a message if a worker alien is in a connected module
            print(f"{ORANGE}{worker_responses[random.randint(0, len(worker_responses) - 1)]} in module {connected_module}.{RESET}")
        if connected_module in vent_shafts:                                                    #print a message if a vent shaft is in a connected module
            print(f"{BLUE}{vent_shafts_responses[random.randint(0, len(vent_shafts_responses) - 1)]} in module {connected_module}.{RESET}")
        if connected_module == queen:                                                          #print a message if the queen is in a connected module
            print(f"{YELLOW}{queen_responses[random.randint(0, len(queen_responses) - 1)]} in module {connected_module}.{RESET}")
        if connected_module in info_panels:                                                    #print a message if an info panel is in a connected module
            print(f"{CYAN}{info_panels_responses[random.randint(0, len(info_panels_responses) - 1)]} in module {connected_module}.{RESET}")

#MAIN PROGRAME
spawn_npcs()                                                                                   #call spawn_npcs() func to spawn the npcs in random modules
print(f"{YELLOW}-{YELLOW}" * 45)
print("Queen is located in module", queen)
print(f"{YELLOW}-{RESET}" * 45)

print(f"{BLUE}-{BLUE}" * 45)
print("Vent shafts are located in modules", vent_shafts)
print(f"{BLUE}-{RESET}" * 45)

print(f"{CYAN}-{CYAN}" * 45)
print("Info panels are located in modules", info_panels)
print(f"{CYAN}-{RESET}" * 45)

print(f"{ORANGE}-{ORANGE}" * 45)
print("Workers are located in modules", workers)
print(f"{ORANGE}-{RESET}" * 45)

while alive and not won:                                                                         #iteration to loop while playuer is not dead or won
    load_module()                                                                                #call load_module() func
    check_vent_shafts()
    move_queen()
    worker_aliens()
    if won == False and alive == True:                                                           #if player is alive feed the game loop
        intuition()
        Check_info_panels()

        output_moves()
        get_action()

if won == True:                                                                                  #checks if player wins or dies displaying win/death text
    print("The queen is traped and you burn it to death with your flamethrower. ")
    print("Game over, YOU WIN")

if alive == False:
    print("The station lost power unable to sustain life suport, you die. ")
    print("Game over, YOU LOST")

#updated version: idk