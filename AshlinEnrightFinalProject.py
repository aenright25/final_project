"""
Ashlin Enright
CS230-5
Final Project
"""
import matplotlib.pyplot as plt
import streamlit as st
import csv
import pandas as pd
import pydeck as pdk

st.title("Skyscrapers Around the World")


st.header("What are the tallest skyscrapers in each city?")
st.sidebar.header("What are the tallest skyscrapers in each city?")

df_skyscrapers = pd.read_csv("Skyscrapers2021.csv")
df_skyscrapers.set_index("RANK", inplace=True)
df_skyscrapers.sort_values(["CITY"], ascending=[True], inplace=True)

skyscraper_cities = df_skyscrapers.groupby(by=["CITY"]).count()
skyscraper_cities.sort_values(["NAME"], ascending=False, inplace=True)

q1_cities = []
q1_cities.extend(df_skyscrapers["CITY"].unique().tolist())
q1_cities.append(" ")
q1_cities.sort()

select_q1_city = st.sidebar.selectbox("Please select a city:", q1_cities)
st.success(f'The city/cities you have selected is/are {select_q1_city}.')
st.sidebar.success(f'The city/cities you have selected is/are {select_q1_city}.')

df_skyscrapers = pd.read_csv("Skyscrapers2021.csv")
df_skyscrapers.rename(columns={"Latitude": "lat", "Longitude": "lon"}, inplace=True)

selected_columns = ["NAME", "CITY", "lat", "lon", "Feet", "Meters"]
sdf_skyscrapers = df_skyscrapers[selected_columns].sort_values(["Feet"], ascending=False)

for i in sdf_skyscrapers.index:
    if select_q1_city not in sdf_skyscrapers.loc[i, "CITY"]:
        sdf_skyscrapers.drop([i], axis=0, inplace=True)

num_skyscrapers = st.sidebar.slider("How many skyscrapers would you like to see per city?", min_value=1, max_value=len(sdf_skyscrapers.index))
st.success(f'You have selected to see {num_skyscrapers} skyscraper(s).')
st.sidebar.success(f'You have selected to see {num_skyscrapers} skyscraper(s).')


while num_skyscrapers < len(sdf_skyscrapers.index):
    sdf_skyscrapers.drop(index=sdf_skyscrapers.index[-1], axis=0, inplace=True)

# getting the view on this map to focus on just one of the cities took me a really long time to figure out so I'm really happy with this code
view_state = pdk.ViewState(latitude=sdf_skyscrapers["lat"].mean(), longitude=sdf_skyscrapers["lon"].mean(), zoom=12, pitch=0)
layer1 = pdk.Layer(type='ScatterplotLayer', data=sdf_skyscrapers, get_position= '[lon, lat]', get_radius=250, get_color=[190, 85, 85], pickable=True)
map = pdk.Deck(map_style='mapbox://styles/mapbox/navigation-day-v1', initial_view_state=view_state, layers=[layer1])
st.pydeck_chart(map)

st.header("How many skyscrapers were completed each year?")
st.sidebar.header("How many skyscrapers were completed each year?")

df_skyscrapers = pd.read_csv("Skyscrapers2021.csv")
df_skyscrapers.set_index("RANK", inplace=True)
df_skyscrapers.sort_values(["COMPLETION"], ascending=[True], inplace=True)

skyscraper_q2_years = st.sidebar.slider("What year(s) would you like to focus on?", min_value=int(df_skyscrapers.iloc[0, 5]), max_value=int(df_skyscrapers.iloc[-1, 5]), value=(int(1973), int(1990)), step=int(1))
st.success(f'The range of the years picked is {skyscraper_q2_years}.')
st.sidebar.success(f'The range of the years picked is {skyscraper_q2_years}.')

sdf_skyscrapers_years = df_skyscrapers[(df_skyscrapers["COMPLETION"] >= int(min(skyscraper_q2_years))) & (df_skyscrapers["COMPLETION"] <= int(max(skyscraper_q2_years)))].groupby(by=["COMPLETION"]).count()[["NAME"]]

# a lot like the map, trying to get this bar chart to only show years within the provided range was difficult and I am happy it was successful
y = sdf_skyscrapers_years.loc[0:, "NAME"]
x = sdf_skyscrapers_years.index[0:]
fig, ax = plt.subplots()
ax.bar(x, y, width=0.5)
st.pyplot(fig)

st.header("What percent of materials were used in each continent?")
st.sidebar.header("What percent of materials were used in each continent?")

df_skyscrapers = pd.read_csv("Skyscrapers2021.csv")
df_skyscrapers.set_index("RANK", inplace=True)


continents = ["Asia", "Asia", "Asia", "Asia", "Asia", "North America", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "North America", "Europe", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "North America", "Asia", "Asia", "North America", "North America", "Asia", "North America", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "North America", "Asia", "Asia", "Asia", "Asia", "North America", "Asia", "Asia", "Europe", "Asia", "Asia", "Asia", "Asia", "North America", "North America", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "Europe", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "North America", "Asia", "Europe", "North America", "Asia", "Asia", "Asia", "Asia", "North America", "Asia", "Asia", "Asia", "Europe", "Asia", "Asia", "Asia", "Asia", "Asia", "North America", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia", "Asia"]
selected_columns = ["NAME", "CITY", "MATERIAL"]
sdf_skyscrapers_continents = df_skyscrapers[selected_columns]
sdf_skyscrapers_continents["CONTINENT"] = continents

q3_continents = ["Asia", "North America", "South America", "Africa", "Antarctica", "Australia", "Europe"]
q3_continents.sort()

q3_continents_skyscrapers = st.sidebar.radio(f'Which continent(s) would you like to focus on?', q3_continents)

sdf_g2 = sdf_skyscrapers_continents.groupby(by=["CONTINENT", "MATERIAL"]).count()[["NAME"]]

if q3_continents_skyscrapers == "Africa" or q3_continents_skyscrapers == "South America" or q3_continents_skyscrapers == "Antarctica" or q3_continents_skyscrapers == "Australia":
    st.success("There are no skyscrapers in this continent. Please choose another an option.")
    st.sidebar.success("There are no skyscrapers in this continent. Please choose another an option.")

elif q3_continents_skyscrapers == "Asia":
    st.success(f'You have chosen {q3_continents_skyscrapers}.')
    st.sidebar.success(f'You have chosen {q3_continents_skyscrapers}.')
    st.title("Materials Used on Skyscrapers in Asia")
    materials = ["composite", "concrete", "steel", "steel/concrete"]
    material_count = [sdf_g2.iloc[0, 0], sdf_g2.iloc[1, 0], sdf_g2.iloc[2, 0], sdf_g2.iloc[3, 0]]
    fig, ax = plt.subplots()
    ax.pie(material_count, labels=materials, autopct='%.1f%%')
    st.pyplot(fig)

elif q3_continents_skyscrapers == "Europe":
    st.success(f'You have chosen {q3_continents_skyscrapers}.')
    st.sidebar.success(f'You have chosen {q3_continents_skyscrapers}.')
    st.title("Materials Used on Skyscrapers in Europe")
    materials = ["composite", "concrete"]
    material_count = [sdf_g2.iloc[4, 0], sdf_g2.iloc[5, 0]]
    fig, ax = plt.subplots()
    ax.pie(material_count, labels=materials, autopct='%.1f%%')
    st.pyplot(fig)

elif q3_continents_skyscrapers == "North America":
    st.success(f'You have chosen {q3_continents_skyscrapers}.')
    st.sidebar.success(f'You have chosen {q3_continents_skyscrapers}.')
    st.title("Materials Used on Skyscrapers in North America")
    materials = ["composite", "concrete", "steel"]
    material_count = [sdf_g2.iloc[6, 0], sdf_g2.iloc[7, 0], sdf_g2.iloc[8, 0]]
    fig, ax = plt.subplots()
    ax.pie(material_count, labels=materials, autopct='%.1f%%')
    st.pyplot(fig)
