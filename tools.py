import json
import plotly.graph_objects as go


access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"
authors = 'Romanov Alexander, Gerasimov Stanislav, Reznichenko Sergey, Abiraev Adilet, Gulkin Alexey'.split(', ')

colors = [[0, '#4DC9A8'],
          [0.00001, '#7DD8A8'],
          [0.00005, '#7DC4A8'],
          [0.0002, '#74AAAB'],
          [0.001, '#659394'],
          [0.003, '#658194'],
          [0.01, "#657dad"],
          [0.02, "#4f608e"],
          [0.04, "#48507e"],
          [0.1, "#384067"],
          [0.2, '#32355e'],
          [0.4, '#24274a'],
          [1, '#1f1b3c']]


def get_counties():
    with open('assets/world_map.json') as f:
        return json.load(f)


def get_mapbox(locations, z):
    return go.Choroplethmapbox(
        geojson=get_counties(), locations=locations,
        z=z, colorscale=colors,
        featureidkey="properties.admin", showscale=False,
        marker={'opacity': 0.7, 'line': {'width': .1, 'color': '#252e3f'}}
    )


''' 
updatemenus=[
        dict(xanchor='left', yanchor='top',
             pad={'l': 10, 't': 10},
             x=0, y=1, direction='down', font={'size': 17},
             buttons=[dict(args=[{"z": [df[i]]}],
                           label=i.replace('_', ' ').capitalize(),
                           method="restyle") for i in params_origin], ),
        dict(xanchor='left', yanchor='top',
             pad={'l': 10, 't': 53},
             x=0, y=1, direction='down', font={'size': 17},
             buttons=[dict(args=[{"locations": [df['location']]}],
                           label='World', method="update")] + [
                         dict(args=[{"locations": [df[df['location'] == i]['location']]}],
                              label=i,
                              method="update",
                              ) for i in my_countries], ),

    ]

'''
