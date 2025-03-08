## creates summaries of each match... counting points and such

import pandas as pd

points = pd.read_csv("createddata/points.csv")
points["Server_Won"] = points.apply(lambda row: row.Svr == row.PtWinner, axis = 1)
summ = points.groupby(by = ["match_id", "Svr"]).agg({"Server_Won": ["sum", "count"]}).reset_index()
summ.columns = ["match_id", "Svr", "Won", "Count"]
summ = summ.pivot(columns = "Svr", index = "match_id").reset_index()
summ.columns = ["match_id", "P1_Won", "P2_Won", "P1_Serve_Count", "P2_Serve_Count"]
print(summ)
summ.to_csv("matchsummaries/bypoint.csv", index = False)

