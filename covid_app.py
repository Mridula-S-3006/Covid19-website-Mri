import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.set_page_config(layout="wide", page_title="COVID-19 EDA")

@st.cache_data
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    data = pd.read_csv(url)
    data['date'] = pd.to_datetime(data['date'])
    data = data[~data['iso_code'].str.startswith("OWID_")]
    data = data[['continent', 'location', 'date', 'new_cases', 'new_deaths',
                 'total_cases', 'total_deaths', 'new_vaccinations', 'total_vaccinations']]
    data = data.rename(columns={'location': 'country'})
    data[['new_cases', 'new_deaths', 'new_vaccinations']] = data[
        ['new_cases', 'new_deaths', 'new_vaccinations']].fillna(0)
    return data

data = load_data()


dailydata = data.copy()
weeklydata = data.groupby(['country', pd.Grouper(key='date', freq='W')])[['new_cases', 'new_deaths', 'new_vaccinations']].sum().reset_index()
monthlydata = data.groupby(['country', pd.Grouper(key='date', freq='ME')])[['new_cases', 'new_deaths', 'new_vaccinations']].sum().reset_index()
continentdata = data.groupby(['continent', pd.Grouper(key='date', freq='ME')])['new_cases'].sum().reset_index()

st.sidebar.header("Filters")
view = st.sidebar.radio("Choose a View", ["Daily Cases", "Weekly Vaccinations", "Monthly Cases by Continent", "Top 10 Countries Snapshot"])
countries = st.sidebar.multiselect("Select countries", options=data['country'].unique(), default=['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czechia', 'Democratic Republic of Congo', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico', 'Micronesia (country)', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican', 'Venezuela', 'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe'])
continents = st.sidebar.multiselect("Select continents", options=data['continent'].dropna().unique(), default=["Asia", "Europe", "Africa","North America","South America","Australia"])

if view == "Daily Cases":
    st.title("Daily COVID-19 Cases")
    fig, ax = plt.subplots(figsize=(12, 6))
    for country in countries:
        subset = dailydata[dailydata['country'] == country]
        ax.plot(subset['date'], subset['new_cases'], label=country)
    ax.set_title("Daily COVID-19 Cases")
    ax.set_xlabel("Date")
    ax.set_ylabel("New Cases")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

elif view == "Weekly Vaccinations":
    st.title("Weekly COVID-19 Vaccinations")
    fig, ax = plt.subplots(figsize=(12, 6))
    for country in countries:
        subset = weeklydata[weeklydata['country'] == country]
        ax.plot(subset['date'], subset['new_vaccinations'], label=country)
    ax.set_title("Weekly Vaccinations")
    ax.set_xlabel("Date")
    ax.set_ylabel("New Vaccinations")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)


elif view == "Monthly Cases by Continent":
    st.title("Monthly COVID-19 Cases by Continent")
    fig, ax = plt.subplots(figsize=(12, 6))
    for continent in continents:
        subset = continentdata[continentdata['continent'] == continent]
        ax.plot(subset['date'], subset['new_cases'], label=continent)
    ax.set_title("Monthly COVID-19 Cases by Continent")
    ax.set_xlabel("Date")
    ax.set_ylabel("New Cases")
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
    
elif view == "Top 10 Countries Snapshot":
    st.title("Top 10 Countries by Total Cases (Latest Data)")
    latest_date = data['date'].max()
    latest_data = data[data['date'] == latest_date]
    country_stats = latest_data[['country', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_vaccinations']]
    top10 = country_stats.sort_values(by='total_cases', ascending=False).head(10)
    st.dataframe(top10.set_index('country'))