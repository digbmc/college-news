"""
Altair Visualization of Religion Data
- read data from a csv
- create a dataframe
- use the dataframe to make a visualization
- save the chart as a json file

"""

import pandas as pd # tool for data analysis and manipulation
import altair as alt # tool for data visualization

csvpath = "/Users/alyssanash/Desktop/DSSF/collegenews/religions-output-topics.csv" # input csv
df = pd.read_csv(csvpath) # creates a dataframe from the csv file
# create the chart
chart = alt.Chart(df).mark_circle( # each point on the chart should be marked as a circle
    opacity=0.8,
    stroke='black',
    strokeWidth=1
).encode(
    alt.X('year:O', axis=alt.Axis(labelAngle=0)), # the x-axis is the year, encoded as ordinal data
    alt.Y('religion:N'), # the y-axis is the religion, encoded as nominal data
    alt.Size('count:Q', # the size of each circle corresponds to the count, encoded as quantitative data
        scale=alt.Scale(range=[0, 1000]), 
        legend=alt.Legend(title='Number of Mentions') # add a legend to explain the scale
    ),
    alt.Color('religion:N', legend=None), # the color should be different for each religion
    tooltip = [ # add tooltips for each circle to display:
        alt.Tooltip('year',title='Year'), # the year
        alt.Tooltip('count', title='Count'), # the number of mentions
        alt.Tooltip('topic', title='Top Topic') # the most frequent topic for the point
    ]
).properties( 
    width=700, # set width 
    height=500, # set height 
    title = "Mentions of Religions Over Time" # set title
)
chart.save("religion-chart.json") # save the chart to a json file