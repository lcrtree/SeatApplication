import random
from typing import *
from utils import constants, io

def put_musnt(seating:io.SeatingTable) -> io.SeatingTable:
    """Put all the blacklisted in the table
    """
    for i, k in seating.rules[io.BLACKLIST].items():
        for j in k:
            if i in seating.rules[io.WHITELIST]:
                continue
            if j in seating.rules[io.WHITELIST]:
                continue
            if seating.status[i] == False:
                column = -1
                row = -1
                pos = random.randint(0, 1)
                while (column == -1 and row == -1) or (seating.table[column][row][0] != ""):
                    column = random.randint(0, len(seating.table) - 1) # choose a random group
                    row = random.randint(0, len(seating.table[column]) - 1) # choose a random row
                seating.table[column][row][0] = i
            if seating.status[j] == False:
                column = -1
                row = -1
                pos = random.randint(0, 1)
                while (column == -1 and row == -1) or (seating.table[column][row][0] != "") \
                                                or seating.table[column][row][pos^1] == i: # bumped into the blacklist
                    column = random.randint(0, len(seating.table) - 1) # choose a random group
                    row = random.randint(0, len(seating.table[column]) - 1) # choose a random row
                seating.table[column][row][1] = j
                seating.status[i] = seating.status[j] = True
    return seating

def put_must(seating:io.SeatingTable)-> io.SeatingTable:
    """Put all the whitelisted in the table
    """
    for i, k in seating.rules[io.WHITELIST].items():
        for j in k:
            if seating.status[i] == True:
                if seating.status[j] == True:
                    continue
            column = -1
            row = -1
            desk = [i, j]
            seating.status[i] = seating.status[j] = True
            random.shuffle(desk) # randomize the deskmates
            while (column == -1 and row == -1) or (seating.table[column][row][0] != ""):
                column = random.randint(0, len(seating.table) - 1) # choose a random group
                row = random.randint(0, len(seating.table[column]) - 1) # choose a random row
            seating.table[column][row] = desk
    return seating

def rand_others(seating:io.SeatingTable) -> io.SeatingTable:
    """Put all the others in the given table
    """ 
    names = seating.names
    random.shuffle(names)
    start_column = 0
    current_name = 0
    for column in range(start_column, len(seating.table)):
        for row in range(len(seating.table[column])):
            for pos in (0, 1):
                while current_name < len(names) and seating.status[names[current_name]] == True:
                    current_name += 1
                if current_name >= len(names):
                    return seating
                if seating.table[column][row][pos] == '':
                    seating.table[column][row][pos] = names[current_name]
                    seating.status[names[current_name]] = True
                    current_name += 1
    return seating

def check(seating:io.SeatingTable) -> io.SeatingTable:
    
    return seating

def rdesk():
    seating = io.SeatingTable()
    if constants.DEBUG:
        print("Start: ", seating.table)
    seating = put_musnt(seating)
    if constants.DEBUG:
        print("Put Musnt: ", seating.table)
    seating = put_must(seating)
    if constants.DEBUG:
        print("Put Must: ", seating.table)
    seating = rand_others(seating)
    if constants.DEBUG:
        print("Rand Others: ", seating.table)
    seating = check(seating)
    print(seating)
    seating.save()