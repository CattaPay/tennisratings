
## deals with converting from Tennis Abstract data to an easier to use format

# first, combine the points datasets into one
import pandas as pd

d1 = pd.read_csv("matchdata/charting-m-points-2020s.csv")
d2 = pd.read_csv("matchdata/charting-m-points-2010s.csv")
d3 = pd.read_csv("matchdata/charting-m-points-to-2009.csv")

all_points = pd.concat([d1, d2, d3])
all_points.to_csv("createddata/default_points.csv", index = False)
print("\nFiles combined\n")

# convert to simpler first and second serve results
import recoding
recoding.process_file("createddata/default_points.csv", "createddata/points.csv")
print("\nPoints processed\n")

# get match data
match_data = pd.read_csv("matchdata/charting-m-matches.csv", index_col = 0)[["Player 1", "Player 2", "Pl 1 hand", "Pl 2 hand", "Date", "Tournament", "Round", "Surface", "Best of"]]

# add year to match data
match_data["Year"] = match_data.apply(lambda row: str(row.Date)[:4], axis = 1)


# read in point data
point_data = pd.read_csv("createddata/points.csv")

# get row corresponding to last shot of each game
last_shot = point_data.loc[point_data.groupby('match_id')['Pt'].idxmax()][["match_id", "PtWinner"]]
last_shot.columns = ["match_id", "Match_Winner"]

# join with matches dataset (note that matches with no points recorded are excluded)
match_result_data = pd.merge(match_data, last_shot, left_index = True, right_on = "match_id").set_index("match_id", inplace = False)
match_result_data.to_csv("createddata/matches.csv")

print("\nMatches processed\n")