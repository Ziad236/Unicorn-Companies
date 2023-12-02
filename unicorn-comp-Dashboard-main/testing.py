# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly.express as px
# import pandas as pd
# from dash.dependencies import Input, Output
# ecom_sales = pd.read_csv('/usr/local/share/datasets/ecom_sales.csv')
# logo_link = 'https://assets.datacamp.com/production/repositories/5893/datasets/fdbe0accd2581a0c505dab4b29ebb66cf72a1803/e-comlogo.png'

# app = dash.Dash(__name__)

# app.layout = html.Div([
#   html.Img(src=logo_link,style={'margin':'30px 0px 0px 0px' }),
#   html.H1('Sales breakdowns'),
#   html.Div(
#     children=[
#     html.Div(
#         children=[
#         html.H2('Controls'),
#         html.Br(),
#         html.H3('Country Select'),
#         # Add a dropdown with identifier
#         dcc.Dropdown(component_id='country_dd',
#         # Set the available options with noted labels and values
#         options=[
#             {'label ':'United Kingdom', 'value ':'UK '},

#             {'label ':'Germany', 'value ':'GM'},

#             {'label': 'France', 'value':'FR'},
#             {'label':'Australia  ', 'value':'AUS'},
#             {'label':'Hong Kong ', 'value':'HK'}],
#             style={'width':'200px', 'margin':'0 auto'})
#         ],
#         style={'width':'350px', 'height':'350px', 'display':'inline-block', 'vertical-align':'top', 'border':'1px solid black', 'padding':'20px'}),
#     html.Div(children=[
#             # Add a graph component with identifier
#             dcc.Graph(id='major_cat'),
#             html.H2('Major Category', 
#             style={ 'border':'2px solid black', 'width':'200px', 'margin':'0 auto'})
#             ],
#              style={'width':'700px','display':'inline-block'}
#              ),
#     ])], 
#   style={'text-align':'center', 'display':'inline-block', 'width':'100%'}
#   )

# @app.callback(
#     # Set the input and output of the callback to link the dropdown to the graph
#     Output(component_id='major_cat', component_property='figure'),
#     Input(component_id='country_dd', component_property='options')
# )

# def update_plot(input_country):
#     country_filter = 'All Countries'
#     sales = ecom_sales.copy(deep=True)
#     if input_country:
#         country_filter = input_country
#         sales = sales[sales['Country'] == country_filter]
#     ecom_bar_major_cat = sales.groupby('Major Category')['OrderValue'].agg('sum').reset_index(name='Total Sales ($)')
#     bar_fig_major_cat = px.bar(
#         title=f'Sales in {country_filter}', data_frame=ecom_bar_major_cat, x='Total Sales ($)', y='Major Category', color='Major Category',
#                  color_discrete_map={'Clothes':'blue','Kitchen':'red','Garden':'green','Household':'yellow'})
#     return bar_fig_major_cat


# if __name__ == '__main__':
#     app.run_server(debug=True)
#*****************************************__________
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Card(
    dbc.CardBody(
        [
            dcc.Graph(
                figure={"data": [{"x": [1, 2, 3], "y": [4, 1, 2], "type": "bar"}]}
            ),
            dcc.Markdown(
                """
                This is some example text that could be displayed within a card.
                """
            ),
        ],
         className="custom-card-body"

        #style={"background-color": "custom-card-body"}

    )
)

if __name__ == "__main__":
    app.run_server()
