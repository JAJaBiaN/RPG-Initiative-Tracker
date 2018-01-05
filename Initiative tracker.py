import numpy as np


################
#### Set up ####
################

##Build a generic character class. Every combatant should be an instance of this class##
class Character:
    """Generic class for all creatures in a battle
    Variables:
        name: Character name (kept capitalized)
        initiative: the number they rolled for initiative
        conditions: a dictionary of all conditions that are effecting the character in this battle
            Form: {condition_name: [turns_remaining, condition_description], ...}"""
    def __init__(self, name, initiative):
        self.name = name.capitalize()
        self.initiative = initiative
        self.conditions = {}


##Set up functions that aren't commands##
def print_status(current_character, extra_lines=1):
    """Print information about a character at the beginning of their turn
    Input: current_character is the index of the character in the character list"""
    print(("\n"*extra_lines)+character_list[current_character].name.capitalize()+"'s turn!")
    elapse_conditions(character_list[current_character].name)
    conds = character_list[current_character].conditions
    if conds:
        print(conds)


##Set up the commands##
def end_battle():
    """End the battle (by setting the while boolean to false)"""
    global battle_happening
    battle_happening = False

def end_turn():
    """End the current character's turn and start the next character's turn"""
    global round_count, current_character
    
    char_num = ini_order.index(current_character)
    if char_num==len(ini_order)-1:
        current_character = ini_order[0]
        round_count+=1
        print("\nRound", str(round_count)+"!")
        print_status(current_character, 0)
    else:
        current_character = ini_order[char_num + 1]
        print_status(current_character)

def add_condition(name, condition, turns_remaining, condition_description=""):
    # Enforce some consistency
    name = name.capitalize()
    condition = condition.capitalize()
    turns_remaining = int(turns_remaining)
    condition_description = condition_description.capitalize()
    
    # Find the character being affected
    for c in character_list: #characters
        if c.name==name:
            affected_character = c
            break
    else:
        print("Name not recognised")
    
    # Add the new condition
    if condition in affected_character.conditions.keys():
        # If the condition already exists
        print("This character already has this condition, is that okay?")
        while True:
            # Keep taking in input until the user supplies a "Y" or an "N"
            text = input("Y/N: ").capitalize()
            if text=="N":
                break
            elif text=="Y":
                # Try "<condition>1", "<condition>2" etc. until an append_number is found that isn't in use
                append_number = 1
                while condition+str(append_number) in affected_character.conditions.keys():
                    append_number+=1
                new_condition = condition+str(append_number)

                affected_character.conditions[new_condition] = [turns_remaining, condition_description]
                print("    "+affected_character.name, "is even more", condition.lower())
                break
    else:
        affected_character.conditions[condition] = [turns_remaining, condition_description]
        print("    "+affected_character.name, "is now", condition.lower())

def drop_condition(name, condition):
    # Enforce some consistency
    name = name.capitalize()
    condition = condition.capitalize()
    
    # Find the character being affected
    for c in character_list: #characters
        if c.name==name:
            affected_character = c
            break
    else:
        print("Name not recognised")
    
    # Drop the condition
    if condition in affected_character.conditions.keys():
        # If the condition exists
        del affected_character.conditions[condition]
        print("    "+affected_character.name, "is no longer", condition.lower())
    else:
        print("    "+affected_character.name, "is not", condition.lower()+
              '. Please use "View conditions" to see what conditions they are affected by.')

def elapse_conditions(name):
    """Decrease the turns_remaining variable on all condtions for a character"""
    # Enforce some consistency
    name = name.capitalize()
    
    # Find the character being affected
    for c in character_list: #characters
        if c.name==name:
            affected_character = c
            break
    else:
        print("Name not recognised")
    
    # Loop through the conditions dictionary, updating turns_remaining
    for cond, cond_vals in affected_character.conditions.copy().items():
        affected_character.conditions[cond][0] -= 1
        if cond_vals[0] == 0:
            drop_condition(name, cond)

def view_status(name):
    """Print the conditions for a given character"""
    # Enforce some consistency
    name = name.capitalize()
    
    # Find the character being affected
    for c in character_list: #characters
        if c.name==name:
            conds = c.conditions
            if conds:
                print(conds)
            else:
                print(c.name, "currently has no conditions effecting them.")
            break
    else:
        print("Name not recognised")


def add_character(name, initiative):
    """Add a character to the battle
    This function will also place them into the correct position in the initiative order"""
    global character_list, ini_order, name_order, initiatives
    name = name.capitalize()
    initiative = int(initiative)
    
    # Add the character to the battle
    c = Character(name, initiative)
    character_number = max(character_list) + 1
    character_list.append(c)
    
    # Add the character to the initiative order
    for i in range(len(initiatives)):
        if initiative > initiatives[i]:
            ini_order.insert(i, character_number)
            name_order.insert(i, name)
            initiatives.insert(i, initiative)
            break
        elif i == len(initiatives)-1:
            ini_order.append(character_number)
            name_order.append(name)
            initiatives.append(initiative)
            break
    
    # Check that the lists are still the same length
    assert len(character_list)==len(ini_order)
    assert len(character_list)==len(name_order)
    assert len(character_list)==len(initiatives)
    
    print(name, "has joined the battle!")

def drop_character(name):
    """Remove a character from the initiative order"""
    global current_character, ini_order, name_order, character_list, initiatives
    name = name.capitalize()
    
    # Find the character being affected
    ini_num = name_order.index(name)
    char_num = ini_order[ini_num]
    
    # Move to the next character before deleting the current one to avoid errors
    if current_character==char_num:
        end_turn()
    
    
    # Remove the character from all relevant lists
    del ini_order[ini_num]
    del name_order[ini_num]
    del character_list[char_num]
    del initiatives[char_num]
    
    # The positions in character_list change when the element is deleted
    #     the following two sections deal with that
    if current_character > 0:
        current_character-=1
    
    # Make sure that the numbers in ini_order match the positions in character_list
    for c in range(len(ini_order)): # char_nums
        if ini_order[c] > char_num:
            ini_order[c]-=1
        elif ini_order[c]==char_num:
            raise(ValueError, "Something has gone wrong in drop_character")
    
    # Check that the lists are still the same length
    assert len(character_list)==len(ini_order)
    assert len(character_list)==len(name_order)
    assert len(character_list)==len(initiatives)

"""Set up command list.
Each element will be a tuple with three elements:
    0: Command name (The text to be input)
    1: The number of arguments to the function
    2: The function to be called
    3: The input parameters for the function as a tuple"""
command_list = []
command_list.append(("End battle", 0, end_battle, ()))
command_list.append(("End turn", 0, end_turn, ()))
command_list.append(("Add condition", 4, add_condition, ("name, condition, turns_remaining, condition_description=''")))
command_list.append(("Drop condition", 2, drop_condition, ("name, condition")))
command_list.append(("View conditions", 1, view_status, ("name")))
command_list.append(("View status", 1, view_status, ("name")))
command_list.append(("Add character", 2, add_character, ("name, initiative")))
command_list.append(("Add creature", 2, add_character, ("name, initiative")))
command_list.append(("Drop character", 1, drop_character, ("name")))
command_list.append(("Drop creature", 1, drop_character, ("name")))
command_list.append(("Kill creature", 1, drop_character, ("name")))


# Turn command_list into a numpy array for easier indexing later
command_list = np.array(command_list)


##Read in characters from .txt file##
with open('Initiative_setup_generic.txt', 'r') as f:
    line = f.readline()
    character_list = []
    while line:
        # Read details from the file and initialise the characters
        character_info = (line.strip('\n')).split(', ') # Allows for unexpected columns
        name, initiative = character_info[0], int(character_info[1])
        character_list.append(Character(name, initiative))
        line = f.readline()

for c in character_list:
    print('Name:', c.name, '| Initiative:', c.initiative)


##Organise other variables before runtime##
"""Organise initiative order"""
ini_order = []
name_order = []
initiatives = []
for c in range(len(character_list)):
    ini = character_list[c].initiative
    name = character_list[c].name
    if not ini_order:
        ini_order.append(c)
        name_order.append(name)
        initiatives.append(ini)
    else:
        for i in range(len(initiatives)):
            if ini > initiatives[i]:
                ini_order.insert(i, c)
                name_order.insert(i, name)
                initiatives.insert(i, ini)
                break
            elif i == len(initiatives)-1:
                ini_order.append(c)
                name_order.append(name)
                initiatives.append(ini)
                break


#############################
#### Visible at run time ####
#############################

##Make some initial prints##
# Print possible inputs
print('Available commands')
for c in command_list: #commands
    if c[3]:
        print('  Command:', '"'+str(c[0])+'"', '| Number of arguments:', (c[1]), '| Arguments:', c[3])
    else:
        print('  Command:', '"'+str(c[0])+'"', '| Number of arguments:', (c[1]))

print("\nRemember to separate the command and its arguments by ', '")
    
# Print initiative order
print('\nInitiative order:')
for n in range(len(name_order)):
    print(str(n+1)+':', name_order[n]) # Because dragons count like FORTRAN programmers

"""Begin actually moving through turns and rounds"""
battle_happening = True
print("\n##################")
print("## BATTLE BEGIN ##")
print("##################")

# Start off with the first character in the initiative order
round_count = 1 # Because the dark lord Orcus has forced me to start the count from 1
print("Round", str(round_count)+"!")
current_character = ini_order[0]
print_status(current_character, 0)

while battle_happening:
    # Take input from the command line
    text = input("Input: ").capitalize() # Deal with non-capitalised inputs
    
    # Check that there is actually a command
    if not text:
        continue
    inputs = text.strip().split(', ')
    
    command_index = np.nonzero(command_list[:, 0]==inputs[0])[0]
    if len(command_index)==0:
        # Note: This is NOT an error raise
        print("Command not recognised!")
        continue
    else:
        if len(inputs)==1:
            command_list[command_index, 2][0]()
        else:
            try: command_list[command_index, 2][0](*inputs[1:])
            except ValueError:
                print("There was a problem with the input arguments, please try again.")