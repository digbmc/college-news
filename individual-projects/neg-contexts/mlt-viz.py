#visualization for individual project (negro and related words in the college news)

import pandas as pd #for data analysis and manipulation
import altair as alt #for data visualization

#read csv into dataframe
csvpath = "mlt-viz-data.csv" #csv file with clean keyword context data
df = pd.read_csv(csvpath, #create dataframe from the csv file
                parse_dates=['date']) #parse date column as datetime pandas object
df['date_est'] = df['date'].dt.tz_localize('EST') #create new column with dates in EST timezone

#configure punchcard chart
selection = alt.selection_multi(fields=['keyword'], bind='legend') #allow viewers to select keyword from legend

chart = alt.Chart(df, width = 600, title = "Monthly Mentions of Words Over Time").mark_circle().encode( #set width #label chart #choose desired mark type
    alt.X('date:T', title="Year"), #set x-axis #select year from date column #label x-axis
    alt.Y('month(date):N', title = "Month"), #set y-axis #select month from date column #label y-axis
    alt.Size('count:Q', title = "Number of Mentions", scale=alt.Scale(domain=[1,36], range=[25,200])), #set mark size to depend on number of keyword instances #label
    alt.Color('keyword:N', title = "Words"), #set mark color to depend on keyword
    opacity=alt.condition(selection, alt.value(0.8), alt.value(0.1)), #fade out marks that are not selected keyword from legend
    #add tooltip to all marks
    tooltip = [alt.Tooltip('yearmonthdate(date_est):T', title="Issue Date"), #show issue date #label
            alt.Tooltip('keyword', title = "Word"), #show keyword #label
            alt.Tooltip('count', title = "Word Count"), #show number of keyword instances #label
            alt.Tooltip('context', title="Context") #show keyword context #label
            ]
).add_selection(selection
).interactive(
).transform_calculate(
    jitter='sqrt(-2*log(random()))*cos(2*PI*random())'
).configure_facet(spacing=0).configure_view(stroke=None
).configure_scale(pointPadding = 1.0
)

#save chart as html
type(chart)

chart

chart.save('mlt-viz-final.html')