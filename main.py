import json
from pathlib import Path
import joblib
import pandas
import sklearn.svm as svm

filename = "junkiert_jakub.json"
results_file = Path(filename)


def main():

    results = {"first all-nba team": [], "second all-nba team": [], "third all-nba team": [],
               "first rookie all-nba team": [], "second rookie all-nba team": []}

    # Data processing here
    # Note: at least 65 games have to be played in 23-24 in order to get All_NBA (at least 20 min played)

    # Load the model
    rookies_model_filename = 'rookies_model.sav'
    rookies_model = joblib.load(rookies_model_filename)

    others_model_filename = 'others_model.sav'
    others_model = joblib.load(others_model_filename)

    # Load the data
    rookies = pandas.read_csv('rookies2023-24.csv')
    rookies = rookies.drop(columns=['Unnamed: 0', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ABBREVIATION'])

    others = pandas.read_csv('others2023-24.csv')
    others = others.drop(columns=['Unnamed: 0', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ABBREVIATION'])

    result_r = rookies_model.predict(rookies)
    result_o = others_model.predict(others)

    true_r = pandas.read_csv('rookies_w_awards2023-24.csv')
    true_o = pandas.read_csv('others_w_awards2023-24.csv')

    dobrze_r = 0
    dobrze_o = 0

    punkty = 0
    dobre_piatki = [0, 0, 0, 0, 0]

    print('Rookies:')
    for i in range(len(result_r)):

        if result_r[i] > 0:
            if result_r[i] == 1:
                if len(results["first rookie all-nba team"]) < 5:
                    results["first rookie all-nba team"].append(true_r['PLAYER_NAME'][i])
            elif result_r[i] == 2:
                if len(results["second rookie all-nba team"]) < 5:
                    results["second rookie all-nba team"].append(true_r['PLAYER_NAME'][i])

        if result_r[i] == true_r['AWARD'][i] and result_r[i] > 0:
            dobrze_r += 1
            punkty += 10
            dobre_piatki[result_r[i] - 1] += 1
        elif result_r[i] > 0 and true_r['AWARD'][i] > 0:
            punkty += 8

    print('Dobrze: ' + str(dobrze_r) + '/10 - ' + str(dobrze_r/10 * 100) + '%')

    print('Others:')
    for i in range(len(result_o)):

        if result_o[i] > 0:
            if result_o[i] == 1:
                if len(results["first all-nba team"]) < 5:
                    results["first all-nba team"].append(true_o['PLAYER_NAME'][i])
            elif result_o[i] == 2:
                if len(results["second all-nba team"]) < 5:
                    results["second all-nba team"].append(true_o['PLAYER_NAME'][i])
            elif result_o[i] == 3:
                if len(results["third all-nba team"]) < 5:
                    results["third all-nba team"].append(true_o['PLAYER_NAME'][i])

        if result_o[i] == true_o['AWARD'][i] and result_o[i] > 0:
            dobrze_o += 1
            punkty += 10
            dobre_piatki[result_o[i] + 1] += 1
        elif result_o[i] > 0 and true_o['AWARD'][i] > 0:
            if abs(result_o[i] - true_o['AWARD'][i]) == 1:
                punkty += 8
            elif abs(result_o[i] - true_o['AWARD'][i]) == 2:
                punkty += 6

    print('Dobrze: ' + str(dobrze_o) + '/15 - ' + str(dobrze_o/15 * 100) + '%')

    for i in dobre_piatki:
        if i == 5:
            punkty += 40

    print('Punkty: ' + str(punkty))

    # End of data processing

    with results_file.open('w') as output_file:
        json.dump(results, output_file, indent=4)


if __name__ == '__main__':
    main()
