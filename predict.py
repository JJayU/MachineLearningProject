import json
from pathlib import Path
import joblib
import pandas
import sys

# This script is used to predict the All-NBA and All-Rookie teams for the 2023-24 season.
# It usus the models trained in train_model.py to predict the probabilities of players being in the teams.
# Copyright: Jakub Junkiert 2024

def main():
    # Read the argument containing the filename for the results
    results_file = Path(sys.argv[1])

    # Prepare the results dictionary
    results = {"first all-nba team": [], "second all-nba team": [], "third all-nba team": [],
               "first rookie all-nba team": [], "second rookie all-nba team": []}

    # Data processing here

    # Load the models
    rookies_model_filename = 'models/rookies_model.sav'
    rookies_model = joblib.load(rookies_model_filename)

    others_model_filename = 'models/others_model.sav'
    others_model = joblib.load(others_model_filename)

    # Load the data and drop the columns that are not needed
    rookies = pandas.read_csv('csv/rookies2023-24.csv')
    rookies_names = rookies['PLAYER_NAME']
    rookies = rookies.drop(columns=['Unnamed: 0', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ABBREVIATION'])

    others = pandas.read_csv('csv/others2023-24.csv')
    others_names = others['PLAYER_NAME']
    others = others.drop(columns=['Unnamed: 0', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ABBREVIATION'])

    # ---- Rookies ----

    print('\nAll-Rookie:')

    # Predict the probabilities of players being in the All-Rookie team
    prob_r = rookies_model.predict_proba(rookies)

    # Sort the probabilities and get the top 5
    top_five_r1 = sorted(prob_r[:, 1], reverse=True)[:5]
    top_five_r2 = sorted(prob_r[:, 2], reverse=True)[:5]

    # Iterate through the probabilities and print and append to results the players that are in the top 5
    print('\nAll-Rookie Team 1:')
    for i, val in enumerate(prob_r[:, 1]):
        if val in top_five_r1:
            results["first rookie all-nba team"].append(rookies_names[i])
            print(rookies_names[i])

    print('\nAll-Rookie Team 2:')
    for i, val in enumerate(prob_r[:, 2]):
        if val in top_five_r2:
            results["second rookie all-nba team"].append(rookies_names[i])
            print(rookies_names[i])

    # ---- Others ----

    print('\nAll-NBA:')

    # Predict the probabilities of players being in the All-NBA team
    prob_others = others_model.predict_proba(others)

    # Sort the probabilities and get the top 5
    top_five_nba1 = sorted(prob_others[:, 1], reverse=True)[:5]
    top_five_nba2 = sorted(prob_others[:, 2], reverse=True)[:5]
    top_five_nba3 = sorted(prob_others[:, 3], reverse=True)[:5]

    # Iterate through the probabilities and print and append to results the players that are in the top 5
    print('\nAll-NBA 1')
    for i, val in enumerate(prob_others[:, 1]):
        if val in top_five_nba1:
            results["first all-nba team"].append(others_names[i])
            print(others_names[i])

    print('\nAll-NBA 2')
    for i, val in enumerate(prob_others[:, 2]):
        if val in top_five_nba2:
            results["second all-nba team"].append(others_names[i])
            print(others_names[i])

    print('\nAll-NBA 3')
    for i, val in enumerate(prob_others[:, 3]):
        if val in top_five_nba3:
            results["third all-nba team"].append(others_names[i])
            print(others_names[i])

    # Uncomment the following lines to check the results
    # import check_results
    # check_results.check_results()

    # End of data processing

    # Save the results to a json file
    with results_file.open('w') as output_file:
        json.dump(results, output_file, indent=4)


if __name__ == '__main__':
    main()
