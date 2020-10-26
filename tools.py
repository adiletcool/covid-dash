import json
import dash_bootstrap_components as dbc

external_stylesheets = [  # 'https://codepen.io/chriddyp/pen/bWLwgP.css',
    dbc.themes.BOOTSTRAP]


def get_colors():
    return [[0, '#4DC9A8'],
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


''' 
# dict(xanchor='left', yanchor='top',
#      pad={'l': 10, 't': 53},
#      x=0, y=1, direction='down', font={'size': 17},
#      buttons=[dict(args=[{"locations": [df['location']]}],
#                    label='World', method="update")] + [
#                  dict(args=[{"locations": [df[df['location'] == i]['location']]}],
#                       label=i,
#                       method="update",
#                       ) for i in my_countries], ),
'''
