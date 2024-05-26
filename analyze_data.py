import pandas
from ydata_profiling import ProfileReport

rookies = pandas.read_csv('rookies_all.csv')

profile = ProfileReport(rookies, title="Profiling Report")
profile.to_file('raport.html')
