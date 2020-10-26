import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from back import MyData
import plotly.graph_objects as go
import tools
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
    dbc.themes.BOOTSTRAP,
])

server = app.server
my_data = MyData()

df = my_data.get_last()

params_origin = ['new_cases', 'new_deaths', 'total_cases', 'total_deaths',
                 'new_cases_per_million', 'new_deaths_per_million',
                 'total_cases_per_million', 'total_deaths_per_million']
params = [i.capitalize().replace('_', ' ') for i in params_origin]
my_countries = my_data.get_countries()

country_ddItems = [dbc.DropdownMenuItem('Sorted by total cases', header=True)] + \
                  [a for i in my_countries for a in [dbc.DropdownMenuItem(i, id=f'country_{i}'),
                                                     dbc.DropdownMenuItem(divider=True)]]
param_ddItems = [a for i in params for a in
                 [dbc.DropdownMenuItem(i, id=f'param_{i}'),
                  dbc.DropdownMenuItem(divider=True)]]

fig = go.Figure(tools.get_mapbox(locations=df['location'], z=df[params_origin[0]]))

fig.update_layout(
    autosize=True,
    clickmode='event+select',
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    mapbox_style='carto-positron',  # "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz",
    mapbox_accesstoken=tools.access_token,
    mapbox_center={"lat": 90, "lon": 0},
    mapbox_zoom=1,
)

app.layout = html.Div(
    children=[
        dbc.Row(
            id='main-header',
            children=[html.H1('Covid-19 Forecasting'),
                      dbc.Col([
                          html.H3('Information Management, BMN 177'),
                          html.H4('Romanov A., Gerasimov. S. Reznichenko S., Abiraev A., Gulkin A.'),
                      ]), ],
            justify='between',
        ),
        html.Div(
            id='main-row',
            children=[
                dbc.Col(id='left-column',
                        children=[
                            dbc.Row(
                                children=[
                                    dbc.Col(dcc.Dropdown(
                                        id='param-dcc-dropdown',
                                        options=[{'label': i, 'value': i} for i in params],
                                        value='New cases',
                                        clearable=False,
                                        searchable=False,
                                        style={'background': 'transparent', 'color': '#7fafdf', 'font-size': 18},
                                    ), width=6),
                                    dbc.Col(dcc.Dropdown(
                                        id='country-dcc-dropdown',
                                        options=[{'label': i, 'value': i} for i in my_countries],
                                        value='World',
                                        clearable=False,
                                        style={'background': 'transparent', 'color': '#7fafdf', 'font-size': 18},
                                    ), width=6)
                                ],
                                id='topleft-row'
                            ),
                            dbc.Row((dcc.Graph(figure=fig, id='my_map')), id='graph-row'),
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


@app.callback(Output('my_map', 'figure'),
              [Input('param-dcc-dropdown', 'value'),
               Input('country-dcc-dropdown', 'value')])
def param_dropdown_clicked(param, country):
    prop_id = dash.callback_context.triggered[0]['prop_id']
    mapbox_center = my_data.get_country_coords(country)
    mapbox_zoom = 1 if country == 'World' else 2
    figure = go.Figure()

    if prop_id == '.':
        figure.add_trace(tools.get_mapbox(locations=df['location'], z=df[params_origin[0]]))

    elif prop_id == 'param-dcc-dropdown.value':
        if param in params and country in my_countries:
            param_column = param.lower().replace(' ', '_')
            locations = df['location'] if country == 'World' else df[df['location'] == country]['location']
            figure.add_trace(tools.get_mapbox(locations=locations, z=df[param_column]))
        else:
            return fig

    elif prop_id == 'country-dcc-dropdown.value':
        if param in params and country in my_countries:
            locations = df['location'] if country == 'World' else df[df['location'] == country]['location']
            figure.add_trace(tools.get_mapbox(locations=locations, z=df[param.lower().replace(' ', '_')]))
        else:
            return fig

    figure.update_layout(
        autosize=True,
        clickmode='event+select',
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_style='carto-positron',  # "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz",
        mapbox_accesstoken=tools.access_token,
        mapbox_center=mapbox_center,
        mapbox_zoom=mapbox_zoom,
    )
    return figure


app.scripts.config.serve_locally = True
if __name__ == '__main__':
    app.run_server(debug=False)
