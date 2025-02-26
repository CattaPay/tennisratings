

### General functions for recoding data

## takes a string s and a list of characters chars
## returns true if any of the characters in chars are in s 
def str_contains(s: str, chars: list[str]):
    for c in chars:
        if c in s:
            return True
    return False

## takes a string s and a list of characters chars
## returns the number of characters in s that and in chars
def count_contains(s: str, chars: list[str]):
    count = 0
    for c in s:
        if c in chars:
            count += 1
    return count

## takes in a coded rally (server, first/second serve, winner) as input
## returns result of first and second serve as a tuple (None if second serve didn't occur)
## also returns count of shots in rally (not including serve)
def recode(server, first, second, winner):
    SHOT_TYPES = ['f', 'b', 'r', 's', 'v', 'z', 'o', 'p', 'u', 'y', 'l', 'm', 'h', 'i', 'j', 'k', 't', 'q'] # list of all shot types
    WEIRD_CHARS = ['P', 'Q', 'S', 'R']
    # if first contains a character that indicates something weird, return (None, None)
    if str_contains(first, WEIRD_CHARS):
        return ("None", "None", 0)

    # if second serve is null, set result 2 to None, and determine result 1

    if isinstance(second, float): # checks if second serve is Nan
        # if first contains a valid shot, determine winner/loser
        if str_contains(first, SHOT_TYPES):
            # count shots
            n_shots = count_contains(first, SHOT_TYPES)
            if server == winner:
                return ("Win", "None", n_shots)
            else:
                return ("Loss", "None", n_shots)
        # if first doesn't contain a shot, check if ace (otherwise winner)
        else:
            if '*' in first:
                return ("Ace", "None", 0)
            else:
                return ("Win", "None", 0)
    # if second serve is not null, first serve is a fault
    else:
        # if second contains a valid shot, determine winner/loser
        # count shots
        n_shots = count_contains(second, SHOT_TYPES)
        if str_contains(second, SHOT_TYPES):
            if server == winner:
                return ("Fault", "Win", n_shots)
            else:
                return ("Fault", "Loss", n_shots)
        # if second doesn't contain a shot, check if ace
        else:
            if '*' in second:
                return ("Fault", "Ace", 0)
            # if not an ace, check if winner (if not it's a fault)
            if server == winner:
                return ("Fault", "Win", 0)
            else:
                return ("Fault", "Fault", 0)
    

import pandas as pd

## reads data from file pointed to by inpath and writes it back with simpler result columns (in terms of Ace, Fault, Win, Loss) to outpath
def process_file(inpath, outpath, verbose = True):
    dat = pd.read_csv(inpath)

    first_result = []
    second_result = []
    shot_count = []
    for ind, row in dat.iterrows():
        if verbose and ind % 1000 == 0:
            print(ind)
        new_values = recode(row["Svr"], row["1st"], row["2nd"], row["PtWinner"])
        first_result.append(new_values[0])
        second_result.append(new_values[1])
        shot_count.append(new_values[2])

    dat["First_Result"] = first_result
    dat["Second_Result"] = second_result
    dat["Shot_Count"] = shot_count

    dat.to_csv(outpath, index = False)

process_file("matchdata/charting-m-points-2010s.csv", "createddata/2010s_points.csv")
