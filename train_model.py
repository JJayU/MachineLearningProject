import pandas
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

# This script is used to train the model. It loads the data, creates the model, fits it and saves it to a file.
# Copyright: Jakub Junkiert 2024

# Load the data
rookies = pandas.read_csv('csv/rookies_all.csv')
others = pandas.read_csv('csv/others_all.csv')

# Drop the columns that are not needed
rookies = rookies.drop(columns=['Unnamed: 0', 'Unnamed: 0.2', 'Unnamed: 0.1', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ABBREVIATION'])
others = others.drop(columns=['Unnamed: 0', 'Unnamed: 0.2', 'Unnamed: 0.1', 'PLAYER_NAME', 'NICKNAME', 'TEAM_ABBREVIATION'])

# Divide the data into X and Y
rookiesX = rookies.drop(columns=['AWARD', 'SEASON'])
rookiesY = rookies['AWARD']

othersX = others.drop(columns=['AWARD', 'SEASON'])
othersY = others['AWARD']


# Create the model
log_clf = LogisticRegression(max_iter=2000)
dt_clf = DecisionTreeClassifier(max_depth=1000)
svc_clf = SVC(probability=True)
rf_clf = RandomForestClassifier(max_depth=1000)

# Create the voting classifiers
model_r = VotingClassifier(
    estimators=[('lr', log_clf)],
    voting='soft'
)

model_o = VotingClassifier(
    estimators=[('lr', log_clf), ('dt', dt_clf), ('svc', svc_clf), ('rf', rf_clf)],
    voting='soft',
    weights=[2, 5, 5, 2]
)

# Fit the models
model_r.fit(rookiesX, rookiesY)
model_o.fit(othersX, othersY)

# Save models to files
rookies_model_filename = 'models/rookies_model.sav'
joblib.dump(model_r, rookies_model_filename)

others_model_filename = 'models/others_model.sav'
joblib.dump(model_o, others_model_filename)

# Uncomment the following lines to run the main script after training the models
# import predict
# predict.main()

