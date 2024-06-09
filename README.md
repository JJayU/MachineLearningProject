# Machine Learning Project

## Aim

This project aim is to predict which NBA players will be awarded with **All-NBA Team** and **All-Rookie Team** awards.

## How does it work?

### Gathering data
Firstly, players statistics are downloaded using *nba_api* library. It is done by running the *gather_train_data.py* script. It does the following things:

1. In first step, the script downloads all players stats from a given time period.
2. Second step iterates over previously created player list and check each player if he got qualified either in All-NBA Team or All-Rookie Team award. This data is saved to *'AWARD'* column and also contains information about to which team (1st,2nd or 3rd) the player was qualified.
3. Step three merges all gathered data into two csv files: *rookies_all.csv* and *others_all.csv*. These files would be used to train prediction model.

It is recommended to run each step separately as it takes a long time and there could be an API blockage which will abort the process.

### Training model
Second step is to train the model. It is done by running the *train_model.py* script.

The script opens the csv files created by *gather_train_data.py* and removes unnecessary columns. It then divides data into X and Y sets.
```python
# Load the data
rookies = pandas.read_csv('csv/rookies_all.csv')

# Drop the columns that are not needed
rookies = rookies.drop(columns=['Unnamed: 0', 'Unnamed: 0.2', 'Unnamed: 0.1', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ABBREVIATION'])

# Divide the data into X and Y
rookiesX = rookies.drop(columns=['AWARD', 'SEASON'])
rookiesY = rookies['AWARD']
```
The core of this model is the **Voting Classifier**. There are actually two models, the first is for predicting All-Rookie Team and the second one is predicting the All-NBA Team.

#### All-Rookie Team model:
After carrying out multiple test author decided to just use LogisticRegression model. It had the best results on predicting which rookies will be awarded. In this case the VotingClassifier isn't really needed as only one classifier is used. But it is used in order to have exact interface as the second model.
```python
model_r = VotingClassifier(
    estimators=[('lr', log_clf)],
    voting='soft'
)
```
#### All-NBA Team model:
This model is more complicated and it uses four classifiers inside the VotingClassifier. These are: LogisticRegression, DecisionTreeClassifier, SVC and RandomForestClassifier. There were more classifiers tested, but these ones turned out to have the best results.
```python
model_o = VotingClassifier(
    estimators=[('lr', log_clf), ('dt', dt_clf), ('svc', svc_clf), ('rf', rf_clf)],
    voting='soft',
    weights=[2, 5, 5, 2]
)
```
After fitting both models (it can take a while), they are saved to files using *joblib* library and they are ready to start predicting awards.

```python
# Fit the models
model_r.fit(rookiesX, rookiesY)
model_o.fit(othersX, othersY)

# Save models to files
rookies_model_filename = 'models/rookies_model.sav'
joblib.dump(model_r, rookies_model_filename)

others_model_filename = 'models/others_model.sav'
joblib.dump(model_o, others_model_filename)
```

### Predicting awards
It is the last step in this project and it is done by running the *predict.py* script.

The script loads the csv file of the players stats in selected season and loads the models created in previous step. Data is then cleared of unecessary columns, similiar to the previous script.

Next, the following method is used:
```python
# Predict the probabilities of players being in the All-Rookie team
prob_r = rookies_model.predict_proba(rookies)
```
It uses previously trained model to create a matrix with rows representing players and columns representing the classes onto which players can be assigned (in this situation those are All-Rookie Teams - 0 if None, 1st or 2nd). This matrix is then used to select five players with highest chance of being in this group.

```python
# Sort the probabilities and get the top 5
top_five_r1 = sorted(prob_r[:, 1], reverse=True)[:5]
top_five_r2 = sorted(prob_r[:, 2], reverse=True)[:5]
```

After this, selected players names are added to output *json* file.

## Project files

- *gather_train_data.py* - script used to download players stats and awards and to save it to csv files,
- *train_model.py* - script used to train prediction models,
- *predict.py* - script used to predict awards,
- *analyze_data.py* - script used to generate ProfileReport of gathered data, used for development only,
- *models/rookies_model.sav*, *models/others_model.sav* - Scikit-Learn models created and used for prediction,
- *junkiert_jakub.json* - results of running the prediction script,
- *requirements.txt* - file with list of libraries needed to run this project,
- *csv* - folder containing all generated csv files
- *README.md* - this file, containing desription of the project
