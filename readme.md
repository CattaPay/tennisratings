Predicting the results of tennis matches

Rally results (POV of serve):
    - fault
    - ace
    - win
    - loss

# recoding.py
Contains useful tools for converting from the Tennis Abstract encoding format to useable data. 

# cam_strategy.py (WIP)
Uses a strategy developed by renowned engineer Cam. Considers all previous matches and predicts winner based on their average shots per match.

# naivebayes.py (WIP)
Uses a naive Bayes classifier to predict results of points.
- Considers matches from a time period prior to match to predict
- Fits seperate naive Bayes classifiers for first and second serve
    - based on variables tbd (surface, player, matchup?, player/surface interaction?)