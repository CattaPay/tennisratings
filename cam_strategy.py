
## implementing Cam's strategy

import pandas as pd

# # reading in data
# point_data = pd.read_csv("createddata/points.csv")

# # splitting shots between players
# point_data["P1_Shots"] = point_data.apply(lambda row: (row.Svr - 1 + row.Shot_Count) // 2, axis = 1)
# point_data["P2_Shots"] = point_data.apply(lambda row: row.Shot_Count - row.P1_Shots, axis = 1)

# # write to a file so it doesn't have to be calculated each time
# point_data.to_csv("createddata/campoints.csv", index = False)

# read Cam's point data from file
point_data = pd.read_csv("createddata/campoints.csv")

# reading in matches
match_data = pd.read_csv("createddata/matches.csv", index_col = 0)

# merge datasets for create full data
full_data = pd.merge(point_data, match_data, left_on = "match_id", right_index = True)

# loop over set of matches to predict
# for example, matches in 2023
predict_year = 2023
predict_matches = match_data[match_data["Year"] == predict_year]

# gets the number of hits and points played for a given player in a list of points
def getStats(all_points: pd.DataFrame, player: str):
    balls_hit = 0
    points_played = 0

    # matches where player is player 1
    subset = all_points[all_points["Player 1"] == player]
    points_played += subset.shape[0]
    balls_hit += sum(subset["P1_Shots"])

    # matches where player is player 2
    subset = all_points[all_points["Player 2"] == player]
    points_played += subset.shape[0]
    balls_hit += sum(subset["P1_Shots"])

    return balls_hit, points_played

# initialize list of predictions
predictions = []
# loop over each match to predict
for id, m in predict_matches.iterrows():
    print(id)
    game_date = m["Date"]
    first_date = game_date - 10000 # considers matches in the past year
    player_1 = m["Player 1"]
    player_2 = m["Player 2"]

    # set up subset of all points to be considered
    points_subset = full_data[(full_data["Date"] >= first_date) & (full_data["Date"] < game_date)]

    balls_1, points_1 = getStats(points_subset, player_1)
    balls_2, points_2 = getStats(points_subset, player_2)

    ratio_1 = balls_1 / points_1 if points_1 > 0 else 0
    ratio_2 = balls_2 / points_2 if points_2 > 0 else 0

    predictions.append(int(ratio_1 >= ratio_2))

predict_matches["Predictions"] = predictions

predict_matches.to_csv("createddata/cam_predictions.csv")