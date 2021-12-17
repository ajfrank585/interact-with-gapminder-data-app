import streamlit as st
import pandas as pd
import plotly.express as px

# format app
st.set_page_config(layout = "wide")
st.title("Interact with Gapminder Data")

# read in the tidy gapminder data
df = pd.read_csv('Data/gapminder_tidy.csv')

# refractor data
continent = "Europe"
metric = "pop"

query = f"continent=='{continent}' & metric=='{metric}'"
df_filtered = df.query(query)

# format plot
metric_labels = {"gdpPercap": "GDP Per Capita", "lifeExp": "Average Life Expectancy", "pop": "Population"}
title_f = f"{metric_labels[metric]} for countries in {continent}"
label_f = {"value": f"{metric_labels[metric]}", 'year': 'Year'}

# create static plot
# fig = px.line(df_filtered, x = 'year', y = 'value', color = 'country', title = title_f, labels = label_f)
# st.plotly_chart(fig, use_container_width=True)

# Challenge - display text below the chart
# st.markdown(f"This plot shows the {metric_labels[metric]} for countries in {continent}")

# Challenge - display dataframe below the plot if a variable is true
# show_data = True
# if show_data: st.dataframe(df_filtered)

# create lists for widgets
continent_list = list(df['continent'].unique())
metric_list = list(df['metric'].unique())

# function to be used in widget argument format_func that maps metric values to readable labels, using dict above
def format_metric(metric_raw):
    return metric_labels[metric_raw]

# create widgets
with st.sidebar:
    st.subheader("Configure the interactive plot")
    continent_w = st.selectbox(label = "Choose a Country", options = continent_list)
    metric_w = st.selectbox(label = "Choose a Metric", options = metric_list, format_func=format_metric)
    # Challenge - show the data frame (if the user wants)
    show_data_w = st.checkbox(label = "Show data")  

# get a list of all possible continents / metrics for the widgets
query_w = f"continent=='{continent_w}' & metric=='{metric_w}'"
df_filtered_w = df.query(query_w)

# Challenge - limit the dates displayed
year_min = int(df_filtered_w['year'].min())
year_max = int(df_filtered_w['year'].max())
with st.sidebar:
    years = st.slider(label = "What years should be plotted?", min_value = year_min, max_value = year_max, value = (year_min, year_max))
df_filtered_w = df_filtered_w[(df_filtered_w.year >= years[0]) & (df_filtered_w.year <= years[1])]

# Challenge - limit the country is displayed
countries_list = list(df_filtered_w['country'].unique())
with st.sidebar:
    countries = st.multiselect(label = "Which countries should be plotted?", options = countries_list, default = countries_list)
df_filtered_w = df_filtered_w[df_filtered_w.country.isin(countries)]

# create interative plot
title_w = f"Interactive plot of {metric_labels[metric_w]} for countries in {continent_w}"
label_w = {"value": f"{metric_labels[metric_w]}", 'year': 'Year'}
fig = px.line(df_filtered_w, x = 'year', y = 'value', color = 'country', title = title_w, labels = label_w)
st.plotly_chart(fig, use_container_width=True)
# Challenge - show the data frame (if the user wants)
if show_data_w: st.dataframe(df_filtered_w)
# Challenge - describe the plot
st.markdown(f"This plot shows the {metric_labels[metric]} for {', '.join(countries)} (in {continent_w}) from {years[0]} to {years[1]}")


