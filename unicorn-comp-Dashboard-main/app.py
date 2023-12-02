

# from dash import Dash, html, dcc, callback, Output, Input

# app = Dash()

# app.layout = html.Div([
#     html.Div([
#         dcc.Graph(id='graph1'),
#     ], className='six columns'),
#     html.Div([
#         dcc.Graph(id='graph2'),
#     ], className='six columns')
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)
# i will contiunou from there
#need to have a structure of the dash
# but before that you need to analysis the data 
#to fix it fast
import json
import dash
from dash import Dash, html, dcc                         # pip install dash
from dash.dependencies import Output, Input
import plotly.graph_objects as go
from dash_extensions import Lottie       # pip install dash-extensions
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px              # pip install plotly
import pandas as pd                      # pip install pandas
from datetime import date
import fig_layout
import numpy as np
import pandas as pd
import base64

#import calendar
import wrangle #to load the data and the figure need some change
#from wordcloud import WordCloud          # pip install wordcloud
#some bans assing it to constant variable then print it 

# Bootstrap themes by Ann: https://hellodash.pythonanywhere.com/theme_explorer
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA],title="UniConrn Dashboard")
badge = dbc.Button(
    [
        "Notifications",
        dbc.Badge("4", color="light", text_color="primary", className="ms-1"),
    ],  
    color="primary",
)
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                #html.H4("Unicorn Companies",className="custom-heading"),
                dbc.CardImg(src='/assets/unicorn.svg',style={'height':'40%', 'width':'40%'},className="d-flex align-items-center justify-content-center h-100")
            ],className="compound-card"),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                        html.H1("Unicorn Companies",className="custom-heading",style={'fontSize': '4.5rem','fontWeight':'bold'})
                ],className="d-flex align-items-center justify-content-center h-100")
             ],className="compound-card",style={"height": "100px"}),
        ], width=8),
    ],className='mb-2 mt-2'),

    #banners

    dbc.Row([
        dbc.Col([
            dbc.Card([html.Div('Total Funding',style={'fontSize': '1.5rem','fontWeight':'bold'}),
                dbc.CardBody([html.Div(f"{wrangle.toatl_funding} $M",style={'fontSize': '2.5rem','fontWeight':'bold'})
                ],className="compound-card")
            ],className="compound-card", id="banner_funding"),
        ], width=4),
        dbc.Col([
            dbc.Card([html.Div('Total Number Unicorn',style={'fontSize': '1.5rem','fontWeight':'bold'}),
                dbc.CardBody([ html.Div(f"#{wrangle.toatl_number_unicorn}",style={'fontSize': '2.5rem','fontWeight':'bold'} )
                ],className="compound-card")
            ],className="compound-card", id="banner_unicorn"),
        ], width=4),
        dbc.Col([
            dbc.Card([html.Div('Total Valuation',style={'fontSize': '1.5rem','fontWeight':'bold'}),
                dbc.CardBody(
                    [ html.Div(f"~ {wrangle.total_valuation } $B",style={'fontSize': '2.5rem','fontWeight':'bold'})
                ],className="compound-card")
            ],className="compound-card", id="banner_valuation"),
        ], width=4),
    ],className='mb-1'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([ dcc.Graph(id="figurefour",figure=wrangle.fig4) 
                ],className="compound-card")
            ],className="compound-card"),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([ dcc.Graph(id="next-graph",figure=wrangle.fig2) 
                ])
            ],className="compound-card"),
        ], width=6),
    ],className="compound-card"),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([dcc.Dropdown(wrangle.df.Industry.unique().tolist() , value="Finetech", id='demo-dropdown')
                              ,dcc.Graph(id="figurethree",figure={},)
                ],className="compound-card")
            ],className="compound-card"),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody(dcc.Graph(id="figureone",figure=wrangle.fig5)
                ,className="compound-card")
            ],className="compound-card"),
        ], width=6),    
        dbc.Col([
            dbc.Card([
                dbc.CardBody([dcc.Graph(id="figureFive",figure=wrangle.fig3)
                ],className="compound-card")
            ],className="compound-card"),
        ], {"size": 6, "offset": 3}),
    ]),
], fluid=True)

# df=wrangle.df.copy(deep=True)
#here we get call back
# @app.callback(
#     [Output(component_id="output_container",component_property='children')],
#     [Input(component_id='figureFive', component_property='hoverData')]
# )

# def update_secondgraph(option_slctd):  
#     if option_slctd is None:
#         x= f'Updated Heading (none clicks)'
#     else:
#         #clicked_industry = option_slctd['points'][0]['x']
#         x='Initial Heading'
#     return json.dumps(option_slctd, indent=2)    

 
@app.callback(
    Output("figurethree","figure"),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    df=wrangle.df.copy(deep=True)
    #container = "The year chosen by user was: {}".format(value)
    if value:
        df=df[df['Industry']==value]
        df_with_fyear = df[~df['Founded Year'].isna()]
        #df_with_fyear=df_with_fyear[df_with_fyear['Industry']=="Other"]
        num_by_founded_year = df_with_fyear["Founded Year"].value_counts().reset_index()
        num_by_founded_year.columns=["index", "Founded Year"]
        num_by_founded_year["index"] = num_by_founded_year["index"].astype(np.int64)
        num_by_founded_year = num_by_founded_year[num_by_founded_year["index"] >= 1990]
        num_by_founded_year.sort_values(by=["index"], inplace=True)
        years = pd.DataFrame({"years" : num_by_founded_year["index"]})

        fig1 = go.Figure(layout=fig_layout.my_figlayout)
        fig1.add_trace(go.Scatter(x=num_by_founded_year["index"],
                                fillcolor='rgba(178, 211, 194,0.11)', 
                                fill='tonexty',
                                mode='lines',
                                line_color='#3DED97', 
                                y=num_by_founded_year["Founded Year"],
                                name='lines')
                    )
    if value is not None:
        fig1.update_layout(title=f'You have selected {value}')

    
    return fig1

 
    
@app.callback(
    # [Output(component_id="output_container",component_property='children')
    Output(component_id='next-graph', component_property='figure'),
    [Input(component_id='figurefour', component_property='hoverData')]
)
def update_graph(option_slctd):
    
   # container = "The year chosen by user was: {}".format(option_slctd)
    
    df=wrangle.df.copy(deep=True)
    if option_slctd :
        selected_country = option_slctd['points'][0]['hovertext']
            
        filtered_df = df[df['Country'] == selected_country]
    else:
        filtered_df = df
                   
    investors = []
    for i, row in filtered_df.iterrows():
        if row["Select Investors"] is not np.nan:
            investors += row["Select Investors"].split(', ')
    investors = pd.Series(investors).value_counts()[:10]
    investors.sort_values(ascending=True, inplace=True)

    fig2 = go.Figure([go.Bar(x=investors.values, y=investors.index, orientation='h',marker=dict(color='#3DED97'))])
    fig2.update_layout( # we can see top investor in all counteie or china and set it as variable
        title = "Top 10 investors",

        xaxis_title='Unicorns count',
        yaxis_title='Investors')
    fig2.update_layout(fig_layout.my_figlayout)
    if option_slctd is not None:
        fig2.update_layout(title=f" Top investors in  {selected_country} ")
    
    return fig2


if __name__=='__main__':
    app.run_server(debug=True, port=8001)
    
    