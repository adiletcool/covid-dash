import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from back import MyData
import plotly.graph_objects as go
import tools
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=tools.external_stylesheets)

server = app.server
my_data = MyData()

df = my_data.get_last()
counties = tools.get_counties()

colors = tools.get_colors()
params_origin = ['new_cases', 'new_deaths', 'total_cases', 'total_deaths',
                 'new_cases_per_million', 'new_deaths_per_million',
                 'total_cases_per_million', 'total_deaths_per_million']
params = [i.capitalize().replace('_', ' ') for i in params_origin]
my_countries = my_data.get_countries()
current_country = 'World'

country_ddItems = [a for i in my_countries for a in
                   [dbc.DropdownMenuItem(i, id=f'country_{i}'), dbc.DropdownMenuItem(divider=True)]]
param_ddItems = [a for i in params for a in
                 [dbc.DropdownMenuItem(i, id=f'param_{i}'),
                  dbc.DropdownMenuItem(divider=True)]]

fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=df['location'],
                                    z=df[params_origin[0]], colorscale=colors, marker_line_width=0,
                                    featureidkey="properties.admin", showscale=False))

fig.update_layout(
    autosize=True,
    clickmode='event+select',
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    mapbox_style='carto-positron',
    mapbox_center={"lat": 60, "lon": 0},
    mapbox_zoom=.8,
    updatemenus=[
        dict(xanchor='left', yanchor='top',
             pad={'l': 10, 't': 10},
             x=0, y=1, direction='down', font={'size': 17},
             buttons=[dict(args=[{"z": [df[i]]}],
                           label=i.replace('_', ' ').capitalize(),
                           method="restyle") for i in params_origin], ),

    ]
)

app.layout = html.Div(
    children=[
        dbc.Row(
            id='main-header',
            children=[html.H4('Covid-19 Forecasting'),
                      html.Div(
                          dbc.Col([
                              html.H2('Information Management'),
                              html.H1('Romanov A., Gerasimov. S. Reznichenko S., Abiraev A., Gulkin A.'),
                          ])
                      )],
            justify='between',
        ),
        html.Div(
            id='main-row',
            children=[
                dbc.Col(id='left-column',
                        children=[
                            dbc.Row([
                                dbc.DropdownMenu(label='New cases',
                                                 children=param_ddItems[:-1], direction='down',
                                                 id='param-dropdown'),
                                dbc.DropdownMenu(label='World',
                                                 children=country_ddItems[:-1], direction='down',
                                                 id='country-dropdown'),
                            ], id='dropdowns-row'),
                            dbc.Row((dcc.Graph(figure=fig, id='my_map'))),
                        ], width=6),
                dbc.Col(id='right-column',
                        children=[
                            html.H2('Selected:', id='demo_h2'),
                        ], width=6),
            ],
        ),
    ],
)


@app.callback(Output('demo_h2', 'children'),
              [Input('my_map', 'selectedData')])
def test1(value):
    if value is not None:
        return f'Selected: {value["points"][0]["location"]}'
    return 'Selected: World'


@app.callback(Output('country-dropdown', "label"),
              [Input(f'country_{i}', 'n_clicks') for i in my_countries])
def country_dropdown_clicked(*args):
    prop_id = dash.callback_context.triggered[0]['prop_id']
    return 'World' if prop_id == '.' else prop_id.split('.n_clicks')[0].split('_')[1]


@app.callback(Output('param-dropdown', "label"),
              [Input(f'param_{i}', 'n_clicks') for i in params])
def param_dropdown_clicked(*args):
    prop_id = dash.callback_context.triggered[0]['prop_id']
    return 'New cases' if prop_id == '.' else prop_id.split('.n_clicks')[0].split('_')[1]


app.scripts.config.serve_locally = True
if __name__ == '__main__':
    app.run_server(debug=True)
