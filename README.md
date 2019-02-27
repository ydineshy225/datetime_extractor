# datetime_extractor
The main intent of this project is to extract mostly all possible timestamps from a given string where date and time written together. It extracts timestaamps in a string format. Later one can convert extracted timestamp to python timestamp using pandas datetime package.

# How to install the package
pip install datetime-extractor

# Example1
  from datetime-extractor import DateTimeExtractor
  import pandas as pd

  samplestring = 'scala> val xorder= new order(1,"2016-02-22 00:00:00.00",100,"COMPLETED")'

  DateTimeExtractor(samplestring)

  Out: ['2016-02-22 00:00:00.00']

# Example2
Suppose if one has a dataframe with text column where timestamps written, the above function can be used to create a new column with extracted timestamp strings. One can use below command in this case

  data = pd.read_csv('sampledata.csv')
  data['ExtractedTimestamp'] = data['textcolumn'].apply(lambda x: DateTimeExtractor(x))
