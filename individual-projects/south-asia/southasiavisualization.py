
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
#alt.renderers.enable('notebook') # needs installation

# Reading a csv into a data frame

csvpath = "/Users/Aanandi/Desktop/projects/india-pakistan4.csv"
df = pd.read_csv(csvpath) # df variable represents a dataframe from the csv file
df.head(20) # preview the first 10 rows of your data frame

chart = alt.Chart(df, height=200, width=600
).mark_tick(thickness=2, height=40).encode(
    alt.X('date:T', title="Issue Date"),
    alt.Y('keyword:N', title=None),
    alt.Color('keyword:N', legend=None),
    tooltip = [alt.Tooltip('date:T', title="Issue date"), # add a tooltip to show
            alt.Tooltip('keyword'),
            alt.Tooltip('context', title="Context")
    ]
).properties(title="Keywords by Issue",)

chart.save('mychart.html')
