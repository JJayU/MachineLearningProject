import pandas
from ydata_profiling import ProfileReport

# Simply create a profile report

rookies = pandas.read_csv('csv/rookies_all.csv')

profile = ProfileReport(rookies, title="Profiling Report")
profile.to_file('raport.html')
