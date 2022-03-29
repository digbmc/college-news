"""
College News Metadata Visualizations
- Reads metadata csv
- Creates html interactive visualization of issue length
- Includes a link to each issue on the Digital Collections site

"""

import pandas as pd
import matplotlib.pyplot as plt
import altair as alt 
# Altair is a new library -> see below for installation instructions
# For documentation, see: https://altair-viz.github.io/index.html


############### Reading a csv into a data frame ##############

csvpath = "data/cn-metadata-wordcounts.csv"
df = pd.read_csv(csvpath, # creates a dataframe from the csv file
                parse_dates=['date']) # parses 'date' column as datetime pandas object
#df.head(20) # preview the first 20 rows of your data frame
# create a new column with dates in EST timezone
df['date_est'] = df['date'].dt.tz_localize('EST')
#df.info() # make sure your columns are the data types you need

################# Configuring the chart #################

issue_length_chart = alt.Chart(df # creates 'chart' variable from data frame
).transform_calculate( # creates a new column by adding the base url to the id number
    url='https://digitalcollections.tricolib.brynmawr.edu/object/bmc'+ alt.datum.id 
).mark_point().encode( # scatterplot chart with points
    alt.Y( # Sets y axis of chart
        'words', # selects data frame column 'words'
        title="Word count"), # label text for axis
    alt.X( # sets x axis
        'yearmonthdate(date_est):T', # selects a temporal format (yearmonth), a column (date)
        title="Issue date"), # label text for x axis
    alt.Size('pages', title='Number of pages'), # sets mark size to depend on page count
    href='url:N', # makes each point link to the url created above
    tooltip = [ # add a tooltip to show for each point
        alt.Tooltip('yearmonthdate(date_est):T', title="Issue date"), # selects date column & specifies that it's temporal data (T)
        alt.Tooltip('vol', title="Vol."), # selects each data frame column to display and how it should be labeled
        alt.Tooltip('no', title="No."),
        alt.Tooltip('pages', title="Pages"),
        alt.Tooltip('words', title="Words"),
        alt.Tooltip('id', title="Object ID")
    ]
).configure_scale(
    maxSize = 300.0, # sets the maximum size of each mark
    pointPadding = 1.0
).properties(
    width=700, # sets chart width
    height=500, # sets chart height
    title = "Issue Length Over Time"
)


################# Saving the chart as html #################

issue_length_chart # displays chart in interactive viewer (doesn't work from command line)

issue_length_chart.save('issue-length-viz/issue_length.html')

# To save chart in other formats (png, pdf) install altair_saver package
# See https://altair-viz.github.io/user_guide/saving_charts.html

"""
To install the altair data visualization library:

$    conda install -c conda-forge altair vega_datasets

The csv I used is here:

I recommend using the VS Code Interactive Viewer or jupyter notebooks
so you can preview viz and test out changes

Open this file in VSCode and right click: 
-> select "Run Current File in Interactive Window"

If this doesn't work, try installing the ipykernel:
- Use your terminal or anaconda prompt (outside of VS code)
- Make sure you've activated the 'base' conda environment (or whichever you've been using)

$    conda activate base

Then install it:

$   conda install -c anaconda ipykernel

If this doesn't work, try quitting VSCode and reopening it.

"""




