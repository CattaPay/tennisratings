
## joins recoded point data with match data
import pandas as pd

match_data = pd.read_csv("matchdata/charting-m-matches.csv", index_col = 0)[["Player 1", "Player 2", "Date", "Surface", "Best of"]]

point_data = pd.read_csv("createddata/2010s_points.csv", index_col = 0).drop(["TbSet", "1st", "2nd", "Notes"], axis = 1)

all_data = pd.merge(match_data, point_data, how = "right", left_index = True, right_index = True)

all_data["Year"] = all_data.apply(lambda row: row.Date[:4], axis = 1)

all_data = all_data.dropna(subset = ["First_Result"])

all_data.to_csv("createddata/2010s_all.csv")