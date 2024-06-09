import pandas
from ydata_profiling import ProfileReport

# This script is used to analyze the data. It generates a profiling report for the data.
# Copyright: Jakub Junkiert 2024

rookies = pandas.read_csv('csv/rookies_all.csv')

profile = ProfileReport(rookies, title="Profiling Report")
profile.to_file('raport.html')
