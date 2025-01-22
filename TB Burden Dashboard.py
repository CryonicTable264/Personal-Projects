import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Connect to the SQLite database
db_path = 'TB Project.db'
conn = sqlite3.connect(db_path)

# Helper function to run SQL queries
def run_query(query):
    return pd.read_sql_query(query, conn)

# Streamlit App
st.title("Global Tuberculosis (TB) Dashboard")

# 1. Global trends in TB prevalence, incidence, and mortality over time
st.header("1. Global Trends in TB Metrics Over Time")
query1 = """
SELECT 
    Year, 
    AVG(Estimated_prevalence_of_TB_all_forms_per_100000_population) AS Avg_Prevalence,
    AVG(Estimated_incidence_all_forms_per_100000_population) AS Avg_Incidence,
    AVG(Estimated_mortality_of_TB_cases_all_forms_excluding_HIV_per_100000_population) AS Avg_Mortality
FROM "TB Project"
GROUP BY Year
ORDER BY Year;
"""
data1 = run_query(query1)
fig1 = px.line(data1, x='Year', y=['Avg_Prevalence', 'Avg_Incidence', 'Avg_Mortality'],
               labels={'value': 'Rate per 100,000 Population', 'variable': 'Metric'},
               title="Global TB Trends")
st.plotly_chart(fig1)

# 2. Countries/Regions with the highest TB burden
st.header("High Burden Regions")
    
    # Query data
query2 = """
    SELECT 
        Country_or_territory_name, Region,
        AVG(Estimated_prevalence_of_TB_all_forms_per_100000_population) AS Avg_Prevalence,
        AVG(Estimated_incidence_all_forms_per_100000_population) AS Avg_Incidence,
        AVG(Estimated_mortality_of_TB_cases_all_forms_excluding_HIV_per_100000_population) AS Avg_Mortality
    FROM 
        "TB Project"
    GROUP BY 
        Country_or_territory_name, Region
    ORDER BY 
        Avg_Prevalence DESC
    LIMIT 10;
    """
data2 = run_query(query2)
st.dataframe(data2)
st.bar_chart(data2.set_index("Country_or_territory_name")[["Avg_Prevalence", "Avg_Incidence", "Avg_Mortality"]])
st.header("2. Countries/Regions with the Highest TB Burden")


# 3. Hotspots for TB-HIV co-infections
st.header("3. Hotspots for TB-HIV Co-Infections")
query3 = """
SELECT 
    Country_or_territory_name, 
    Region, 
    AVG("Estimated_mortality_of_TB_cases_who_are_HIV-positive_per_100000_population") AS HIV_Mortality
FROM "TB Project"
GROUP BY Country_or_territory_name, Region
ORDER BY HIV_Mortality DESC
LIMIT 10;
"""
data3 = run_query(query3)
fig3 = px.bar(data3, x='Country_or_territory_name', y='HIV_Mortality',
              color='Region', title="TB-HIV Co-Infection Hotspots")
st.plotly_chart(fig3)

# 4. Most vulnerable populations
st.header("4. Most Vulnerable Populations for TB Outbreaks")
query4 = """
SELECT 
    Region, 
    AVG(Estimated_HIV_in_incident_TB_percent) AS Avg_HIV_In_TB
FROM "TB Project"
GROUP BY Region
ORDER BY Avg_HIV_In_TB DESC;
"""
data4 = run_query(query4)
fig4 = px.bar(data4, x='Region', y='Avg_HIV_In_TB', title="Most Vulnerable Regions for TB Outbreaks")
st.plotly_chart(fig4)

# 5. Progress in response to interventions
st.header("5. Progress in TB Prevalence and Mortality Over Time")
query5 = """
SELECT 
    Year, 
    AVG(Estimated_prevalence_of_TB_all_forms_per_100000_population) AS Avg_Prevalence,
    AVG(Estimated_mortality_of_TB_cases_all_forms_excluding_HIV_per_100000_population) AS Avg_Mortality
FROM "TB Project"
GROUP BY Year
ORDER BY Year;
"""
data5 = run_query(query5)
fig5 = px.line(data5, x='Year', y=['Avg_Prevalence', 'Avg_Mortality'],
               labels={'value': 'Rate per 100,000 Population', 'variable': 'Metric'},
               title="Progress in TB Prevalence and Mortality Over Time")
st.plotly_chart(fig5)

# 6. Resource allocation needs
st.header("6. Regions with the Greatest Need for Improved Detection")
query6 = """
SELECT 
    Region, 
    Country_or_territory_name, 
    AVG(Case_detection_rate_all_forms_percent) AS Avg_Detection_Rate
FROM "TB Project"
GROUP BY Region, Country_or_territory_name
ORDER BY Avg_Detection_Rate ASC
LIMIT 10;
"""
data6 = run_query(query6)
st.dataframe(data6)

# 7. Population size and TB resource needs
st.header("7. Population Size and TB Resource Needs")
query7 = """
SELECT 
    Year, 
    Country_or_territory_name, 
    Estimated_total_population_number, 
    Estimated_number_of_incident_cases_all_forms
FROM "TB Project";
"""
data7 = run_query(query7)
fig7 = px.scatter(data7, x='Estimated_total_population_number', y='Estimated_number_of_incident_cases_all_forms',
                  title="Population Size vs. TB Incidence",
                  labels={'Estimated_total_population_number': 'Total Population',
                          'Estimated_number_of_incident_cases_all_forms': 'Incident Cases'})
st.plotly_chart(fig7)

# 8. Role of population size and growth in TB control resource needs
st.header("8. Role of Population Size and Growth in TB Control Resource Needs")
query8 = """
SELECT 
    Year, 
    Country_or_territory_name, 
    Estimated_total_population_number, 
    Estimated_number_of_incident_cases_all_forms
FROM "TB Project";
"""
data8 = run_query(query8)
fig8 = px.scatter(data8, x='Estimated_total_population_number', y='Estimated_number_of_incident_cases_all_forms',
                  color='Year',
                  title="Population Size vs. TB Incident Cases",
                  labels={'Estimated_total_population_number': 'Total Population',
                          'Estimated_number_of_incident_cases_all_forms': 'Incident Cases'})
st.plotly_chart(fig8)

# 9. Distribution of TB metrics by income level or healthcare infrastructure
st.header("9. Distribution of TB Metrics by Income Level or Healthcare Infrastructure")
query9 = """
SELECT 
    Region, 
    Country_or_territory_name, 
    AVG(Estimated_prevalence_of_TB_all_forms_per_100000_population) AS Avg_Prevalence
FROM "TB Project"
GROUP BY Region, Country_or_territory_name;
"""
data9 = run_query(query9)
fig9 = px.box(data9, x='Region', y='Avg_Prevalence', title="Distribution of TB Prevalence by Region",
              labels={'Avg_Prevalence': 'TB Prevalence per 100,000 Population', 'Region': 'Region'})
st.plotly_chart(fig9)

# 10. Trends to inform policy-making for high-burden regions
st.header("10. Trends to Inform Policy-Making for High-Burden Regions")
query10 = """
SELECT 
    Year, 
    Region, 
    AVG(Estimated_mortality_of_TB_cases_all_forms_excluding_HIV_per_100000_population) AS Avg_Mortality,
    AVG("Estimated_mortality_of_TB_cases_who_are_HIV-positive_per_100000_population") AS Avg_HIV_Mortality
FROM "TB Project"
GROUP BY Year, Region
ORDER BY Year;
"""
data10 = run_query(query10)
fig10 = px.line(data10, x='Year', y=['Avg_Mortality', 'Avg_HIV_Mortality'], color='Region',
                labels={'value': 'Mortality Rate per 100,000', 'variable': 'Metric'},
                title="TB and TB-HIV Mortality Trends by Region")
st.plotly_chart(fig10)

# Close the database connection
conn.close()