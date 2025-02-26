

### Reads data from points files and returns a simplified 

## takes a string s and a list of characters chars
## returns true if any of the characters in chars are in s 
def str_contains(s: str, chars: list[str]):
    for c in chars:
        if c in s:
            return True
    return False

## takes in a coded rally (server, first/second serve, winner) as input
## returns result of first and second serve as a tuple (None if second serve didn't occur)
def recode(server, first, second, winner):
    SHOT_TYPES = ['f', 'b', 'r', 's', 'v', 'z', 'o', 'p', 'u', 'y', 'l', 'm', 'h', 'i', 'j', 'k', 't', 'q'] # list of all shot types
    WEIRD_CHARS = ['P', 'Q', 'S', 'R']
    # if first contains a character that indicates something weird, return (None, None)
    if str_contains(first, WEIRD_CHARS):
        return ("None", "None")

    # if second serve is null, set result 2 to None, and determine result 1
    if isinstance(second, float):
        # if first contains a valid shot, determine winner/loser
        if str_contains(first, SHOT_TYPES):
            if server == winner:
                return ("Win", "None")
            else:
                return ("Loss", "None")
        # if first doesn't contain a shot, check if ace (otherwise winner)
        else:
            if '*' in first:
                return ("Ace", "None")
            else:
                return ("Win", "None")
    # if second serve is not null, first serve is a fault
    else:
        # if second contains a valid shot, determine winner/loser
        if str_contains(second, SHOT_TYPES):
            if server == winner:
                return ("Fault", "Win")
            else:
                return ("Fault", "Loss")
        # if second doesn't contain a shot, check if ace
        else:
            if '*' in second:
                return ("Fault", "Ace")
            # if not an ace, check if winner (if not it's a fault)
            if server == winner:
                return ("Fault", "Win")
            else:
                return ("Fault", "Fault")
    


import pandas as pd

## reads data from file pointed to by inpath and writes it back with simpler result columns to outpathj
def process_file(inpath, outpath):
    dat = pd.read_csv(inpath)

    first_result = []
    second_result = []
    for ind, row in dat.iterrows():
        if ind % 1000 == 0:
            print(ind)
        new_values = recode(row["Svr"], row["1st"], row["2nd"], row["PtWinner"])
        first_result.append(new_values[0])
        second_result.append(new_values[1])


    dat["First_Result"] = first_result
    dat["Second_Result"] = second_result

    dat.to_csv(outpath, index = False)

process_file("createddata/2020s_points.csv", "matchdata/charting-m-points-2020s.csv")
