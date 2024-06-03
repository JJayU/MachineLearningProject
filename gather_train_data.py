from nba_api.stats.endpoints import playerawards
from nba_api.stats.endpoints import leaguedashplayerstats

import numpy as np
import time
import pandas

# This script is used to gather data for training the model. It downloads player stats for all seasons,
# then downloads player awards for each player and each season. It then merges all seasons into one file.
# Tip: run steps 1-3 separately, as the script may crash due to timeout.

# Copyright: Jakub Junkiert 2024


# --------------------------------------------------------------------------------------------
# Step 0 - Prepare list of seasons
seasons = []
for i in range(0, 23):
    seasons.append('20' + str(i).zfill(2) + '-' + str(i + 1).zfill(2))

# --------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------
# Step 1 - Download player stats for all seasons
for i in seasons:
    rookies = leaguedashplayerstats.LeagueDashPlayerStats(
        season=i,
        player_experience_nullable='Rookie').get_data_frames()[0]

    sophomores = leaguedashplayerstats.LeagueDashPlayerStats(
        season=i,
        player_experience_nullable='Sophomore').get_data_frames()[0]

    veterans = leaguedashplayerstats.LeagueDashPlayerStats(
        season=i,
        player_experience_nullable='Veteran').get_data_frames()[0]

    others = pandas.concat([sophomores, veterans])

    rookies.to_csv('rookies' + i + '.csv')
    others.to_csv('others' + i + '.csv')

# --------------------------------------------------------------------------------------------


# Lambda function to find All-NBA awards
def find_award_o(row):
    print('-----')
    print(row['PLAYER_ID'])
    print(row['PLAYER_NAME'])
    pl_awards = playerawards.PlayerAwards(player_id=row['PLAYER_ID'], timeout=120).get_dict()

    for award in pl_awards['resultSets'][0]['rowSet']:
        award_description = award[4]
        season = award[6]
        team_no = award[5]

        # print(award_description)

        if 'All-NBA' in award_description and season == i:
            print('All-NBA ' + str(team_no))
            row['AWARD'] = team_no

    # Random sleep time to prevent API blockage
    time.sleep(np.random.randint(1, 3))

    return row


# Lambda function to find All-Rookie awards
def find_award_r(row):
    print('-----')
    print(row['PLAYER_ID'])
    print(row['PLAYER_NAME'])
    pl_awards = playerawards.PlayerAwards(player_id=row['PLAYER_ID'], timeout=120).get_dict()

    for award in pl_awards['resultSets'][0]['rowSet']:
        award_description = award[4]
        season = award[6]
        team_no = award[5]

        if 'All-Rookie Team' in award_description and season == i:
            print('All-Rookie Team ' + str(team_no))
            row['AWARD'] = team_no

    # Random sleep time to prevent API blockage
    time.sleep(np.random.randint(1, 3))

    return row


# --------------------------------------------------------------------------------------------
# Step 2 - Open downloaded files and download each player awards
for i in seasons:
    print('Starting season ' + i)

    rookies = pandas.read_csv('rookies' + i + '.csv')
    others = pandas.read_csv('others' + i + '.csv')

    rookies['AWARD'] = 0
    rookies['SEASON'] = i

    others['AWARD'] = 0
    others['SEASON'] = i

    rookies = rookies.apply(find_award_r, axis=1)
    others = others.apply(find_award_o, axis=1)

    rookies.to_csv('rookies_w_awards' + i + '.csv')
    others.to_csv('others_w_awards' + i + '.csv')

# --------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------
# Step 3 - Merge all seasons into one file

rookies = pandas.DataFrame()
others = pandas.DataFrame()

for i in seasons:
    rookies = pandas.concat([rookies, pandas.read_csv('rookies_w_awards' + i + '.csv')])
    others = pandas.concat([others, pandas.read_csv('others_w_awards' + i + '.csv')])

rookies.to_csv('rookies_all.csv')
others.to_csv('others_all.csv')

# --------------------------------------------------------------------------------------------
