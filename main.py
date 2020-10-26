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
current_param = 'New cases'
current_country = 'World'

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
            children=[html.H4('Covid-19 Forecasting'),
                      html.Div(
                          dbc.Col([
                              html.H2('Information Management, BMN 177'),
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
                                dbc.DropdownMenu(label=current_param,
                                                 children=param_ddItems[:-1], direction='down',
                                                 id='param-dropdown'),
                                dbc.DropdownMenu(label=current_country,
                                                 children=country_ddItems[:-1], direction='down',
                                                 id='country-dropdown'),
                            ], id='dropdowns-row'),
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


@app.callback([Output('param-dropdown', "label"),
               Output('country-dropdown', "label"),
               Output('my_map', 'figure')],
              [Input(f'param_{i}', 'n_clicks') for i in params] +
              [Input(f'country_{i}', 'n_clicks') for i in my_countries])
def param_dropdown_clicked(*args):
    global current_country
    global current_param
    prop_id = dash.callback_context.triggered[0]['prop_id']
    param = current_param
    country = current_country
    mapbox_center = {"lat": 90, "lon": 0}
    mapbox_zoom = 1
    figure = go.Figure()

    if prop_id == '.':
        figure.add_trace(tools.get_mapbox(locations=df['location'], z=df[params_origin[0]]))

    elif 'param' in prop_id:
        param = prop_id.split('.n_clicks')[0].split('_')[1]
        current_param = param
        param_column = param.lower().replace(' ', '_')
        locations = df['location'] if current_country == 'World' else df[df['location'] == current_country]['location']
        figure.add_trace(tools.get_mapbox(locations=locations, z=df[param_column]))

    elif 'country' in prop_id:
        country = prop_id.split('.n_clicks')[0].split('_')[1]
        current_country = country
        locations = df['location'] if current_country == 'World' else df[df['location'] == current_country]['location']
        mapbox_center = my_data.get_country_coords(current_country)
        mapbox_zoom = 2
        figure.add_trace(tools.get_mapbox(locations=locations, z=df[param.lower().replace(' ', '_')]))

    figure.update_layout(
        autosize=True,
        clickmode='event+select',
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_style='carto-positron',  # "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz",
        mapbox_accesstoken=tools.access_token,
        mapbox_center=mapbox_center,
        mapbox_zoom=mapbox_zoom,
    )
    return [param, country, figure]


app.scripts.config.serve_locally = True
if __name__ == '__main__':
    app.run_server(debug=True)
