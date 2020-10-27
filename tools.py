import json
import plotly.graph_objects as go

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


def update_pred_fig(fig):
    return fig.update_layout(
        dragmode='pan',
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        legend={'x': 0, 'y': 1, 'bgcolor': 'rgba(0,0,0,0)',
                'font': {'size': 17, 'family': "Playfair Display", 'color': '#7fafdf'}},
        plot_bgcolor='#252e3f',
        paper_bgcolor='#252e3f',
        xaxis={'color': '#7fafdf', 'gridcolor': '#3b4e72', 'showline': False,
               'rangemode': "nonnegative", 'zeroline': False},
        yaxis={'color': '#7fafdf', 'gridcolor': '#3b4e72', 'showline': False,
               'rangemode': "nonnegative", 'zeroline': False},
    )


def update_map_fig(fig, center=None, zoom=1):
    if center is None:
        center = {"lat": 90, "lon": 0}

    return fig.update_layout(
        autosize=True,
        clickmode='event+select',
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_style='carto-positron',
        mapbox_center=center,
        mapbox_zoom=zoom,
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
