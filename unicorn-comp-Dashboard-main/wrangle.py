import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import pycountry
import fig_layout
import math
#read data 
df = pd.read_csv("C:/Users/LapStore/Downloads/ITI_Data_Visualization-main/ITI_Data_Visualization-main/viualization_unicorn/Unicorn_Companies.csv")
#clean the data 
ind_shifted = df[df["Select Inverstors"].isnull()].index.to_list()
ind_shifted.remove(789) #because its right  you dont have to switch
for i, row in df.iterrows():
    if i in ind_shifted:
        city, industry, invest = df.at[i, "City"], df.at[i, "Industry"], df.at[i, "Select Inverstors"]
        df.at[i, "City"] = invest
        df.at[i, "Industry"] = city
        df.at[i, "Select Inverstors"] = industry

##date and valuation 
df["Valuation ($B)"] = df["Valuation ($B)"].apply(lambda x: x[1:]).astype(float)
df["Date Joined"] = pd.to_datetime(df["Date Joined"])
##
# fill "None" values with np.nan
def replace_none_with_npnan(x):
    return np.nan if x == "None" else x

df = df.applymap(replace_none_with_npnan)
df["Investors Count"] = df["Investors Count"].fillna(0)
#df.info()
######
# Get the actual values of "Total Raised" and replace the wrong values in data
def get_actual_total_raised(value: str) -> float:
    to_replace = "$BMK"
    unity = value[-1]
    value = float(''.join(v for v in value if v not in to_replace))
    if unity == "B":
        result = value * 1000000000
    elif unity == "M":
        result = value * 1000000
    elif unity == "K":
        result = value * 1000
    else:
        result = value
    return result
   
df["Total Raised"] = df["Total Raised"].apply(lambda x: get_actual_total_raised(x) if x is not np.nan else x)
df["Total Raised"] = df["Total Raised"] / 1e6
df = df.rename(columns={"Total Raised" : "Total Raised(M)", 
                        "Select Inverstors" : "Select Investors"})

df['Financial Stage'] = df['Financial Stage'].replace({"Acq" : "Acquired"})
df["Industry"] = df["Industry"].replace({"Finttech" : "Fintech", 
                                         "Artificial intelligence" : "Artificial Intelligence"})
#########
# change column types
df["Country"] = df["Country"].astype('category')
df["City"] = df["City"].astype('category')
df["Industry"] = df["Industry"].astype('category')
df["Investors Count"] = df["Investors Count"].astype(int)


# trend company by each year 
#count of each industry in every year 
#todo : should filter by industry
# df_with_fyear = df[~df['Founded Year'].isna()]
# #df_with_fyear=df_with_fyear[df_with_fyear['Industry']=="Other"]
# num_by_founded_year = df_with_fyear["Founded Year"].value_counts().reset_index()
# num_by_founded_year.columns=["index", "Founded Year"]
# num_by_founded_year["index"] = num_by_founded_year["index"].astype(np.int64)
# num_by_founded_year = num_by_founded_year[num_by_founded_year["index"] >= 1990]
# num_by_founded_year.sort_values(by=["index"], inplace=True)
# years = pd.DataFrame({"years" : num_by_founded_year["index"]})

# fig1 = go.Figure(layout=fig_layout.my_figlayout)
# fig1.add_trace(go.Scatter(x=num_by_founded_year["index"],
#                           fillcolor='rgba(178, 211, 194,0.11)', 
#                           fill='tonexty',
#                           mode='lines',
#                           line_color='#7a1c3f', 
#                           y=num_by_founded_year["Founded Year"],
#                           name='lines')
#                )
#fig1.show()
# second graph 
#top 10 investor 
#todo : should filter by country in the map
investors = []
for i, row in df.iterrows():
    if row["Select Investors"] is not np.nan:
        investors += row["Select Investors"].split(', ')
investors = pd.Series(investors).value_counts()[:10]
investors.sort_values(ascending=True, inplace=True)

fig2 = go.Figure([go.Bar(x=investors.values, y=investors.index, orientation='h',marker=dict(color='#3DED97'))])
fig2.update_layout( # we can see top investor in all counteie or china and set it as variable

    title='Top 10 Investors',
    xaxis_title='Unicorns count',
    yaxis_title='Investors')
fig2.update_layout(fig_layout.my_figlayout
                   )
#fig2.show()

#figure 3
top_20_companies = df.sort_values("Valuation ($B)", ascending=False)[:20]

fig3 = px.scatter(top_20_companies, x="Valuation ($B)", y="Total Raised(M)",
                 size="Investors Count", 
                 color=top_20_companies["Industry"].to_numpy(),
                 hover_name="Company", size_max=60,
                 title ='Top 20 companies',



    )
fig3.update_layout(
    title={
            'text': 'Top 20 companies',
        'font': {
            'family': 'Roboto_font',
            'size': 22,
            'color': 'White'
        },},
    legend=dict(
        title={
            'text': 'Industries',
            'font': {
                'family': 'Roboto_font',
                'size': 18,
                'color': 'White'
            },},
    )

)

fig3.update_layout(fig_layout.my_figlayout)
#fig3.show()

##figure 7

top_10_countries = df[["Country", "Valuation ($B)"]].groupby(by="Country").sum()
top_10_countries = top_10_countries.sort_values(by="Valuation ($B)", ascending=False)[:10].reset_index()
top_10_countries_total_valuation = top_10_countries["Valuation ($B)"].sum()
top_10_countries_total_valuation_perc = top_10_countries_total_valuation * 100 / df["Valuation ($B)"].sum()
top_10_countries["iso_code"] = top_10_countries["Country"].apply(lambda x: pycountry.countries.lookup(x).alpha_3)
color_scale = ["#9BECB2", "#55E77C", "#26E1B2", "#25C488", "#06BE84", "#097759", "#003141", "#002837"]

fig4 = px.choropleth(top_10_countries, locations="iso_code", color="Valuation ($B)",
                    hover_name="Country", 
                    title=f"Valuation for top 10 countries is {top_10_countries_total_valuation:.1f} B$ ({top_10_countries_total_valuation_perc:.1f}% of total)"
                   ,color_continuous_scale=color_scale


                   )
fig4.update_layout(fig_layout.my_figlayout)
#fig7.show()


industry_total_val = df[["Industry", "Valuation ($B)"]].groupby(by="Industry").sum().sort_values(by="Valuation ($B)",ascending=True)

fig5 = go.Figure()
fig5.add_trace(go.Bar(
    y=industry_total_val.index,
    x=industry_total_val["Valuation ($B)"],
    hovertext=industry_total_val.index,
    marker=dict(color='#3DED97'),
    orientation='h'
))

fig5.update_layout(title={'text': 'Industries distribution by total valuation',
        'font': {'family': 'Roboto_font', 'color': 'white', 'size': 26}})
fig5.update_layout(fig_layout.my_figlayout)

#constant
#Todo 1- investor 2- country  3-company  4- industry 5- total funding total evaluation
total_valuation=math.ceil(df['Valuation ($B)'].sum()*10**-3)
toatl_number_unicorn=df.Company.count()
toatl_funding=round(df["Total Raised(M)"].sum()*10**-3,2)