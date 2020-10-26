import os
import pandas as pd
from datetime import datetime, timedelta
import pmdarima as pm
import numpy as np
import plotly.graph_objects as go

columns = ['iso_code', 'date', 'location',
           'new_cases', 'total_cases', 'new_cases_per_million', 'total_cases_per_million',
           'new_deaths', 'total_deaths', 'new_deaths_per_million', 'total_deaths_per_million']
last_data_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
_path = 'assets/data'
yesterday_str = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
_filename = f'covid-data-{yesterday_str}.csv'
_csv_files = os.listdir(_path)


class MyData:
    coordinates = pd.read_csv('assets/countries.csv')

    def __init__(self):
        if len(_csv_files) > 0 and _csv_files[0] == _filename:
            print('Data is up to date')
            self.df = pd.read_csv(f'{_path}/{_filename}')[columns].fillna(0)
        else:
            print('Downloading last data')
            if len(_csv_files) > 0:
                for i in _csv_files:
                    os.remove(f'{_path}/{i}')

            self.df = pd.read_csv(last_data_url)[columns].fillna(0)
            self.df.to_csv(_path + '/' + _filename, index=False)
            print('Downloaded last data')

    def get_countries(self, ) -> list:
        return self.df.groupby(by='location').max().sort_values('total_cases', ascending=False).index.to_list()

    def get_last(self):
        return pd.concat([self.df[self.df['location'] == i].tail(1) for i in self.get_countries()])

    def get_country_coords(self, location):
        if location in self.coordinates['name'].to_list():
            res = self.coordinates[self.coordinates['name'] == location][['latitude', 'longitude']].to_dict(
                orient='index')
            k = list(res)[0]
            return {'lat': res[k]['latitude'], 'lon': res[k]['longitude']}
        else:
            return {"lat": 100, "lon": 0}

    def predict(self, country, indicator, periods) -> dict:
        df_real = self.df[self.df['location'] == country][[indicator]].fillna(0).reset_index(drop=True)
        model = pm.auto_arima(df_real, start_p=0, start_q=0,
                              test='kpss',
                              max_p=3, max_q=3,
                              m=1,
                              d=None,
                              seasonal=False,
                              trace=True,
                              error_action='ignore',
                              suppress_warnings=True,
                              stepwise=False)
        forecast, confint = model.predict(periods, return_conf_int=True)
        index_of_fc = np.arange(len(df_real), len(df_real) + periods)
        forecast_series = pd.Series(forecast, index=index_of_fc)
        lower_series = pd.Series(confint[:, 0], index=index_of_fc)
        upper_series = pd.Series(confint[:, 1], index=index_of_fc)
        return {'real': df_real, 'fc_index': index_of_fc, 'forecast': forecast_series, 'lower': lower_series,
                'upper': upper_series}

    def get_prediction_plot(self, country, indicator, periods):
        res = self.predict(country=country, indicator=indicator, periods=periods)
        fig = go.Figure()
        # Real
        fig.add_trace(go.Scatter(x=res['real'].index.to_list(), y=res['real'][indicator].to_list(), name='Real'))
        # Lower confidence interval
        fig.add_trace(go.Scatter(x=res['fc_index'].tolist(), y=res['lower'].to_list(), showlegend=False, mode='lines',
                                 line=dict(width=.5, color='#9cc3c3')))
        # Upper confidence interval
        fig.add_trace(go.Scatter(x=res['fc_index'].tolist(), y=res['upper'].to_list(), mode='lines', showlegend=False,
                                 fill='tonexty', line=dict(width=.5, color='#9cc3c3')))
        # Prediction
        fig.add_trace(go.Scatter(x=res['fc_index'].tolist(), y=res['forecast'].to_list(), name='Prediction',
                                 line=dict(width=1.5, color='#2be4b1')))

        fig.update_layout(
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
        return fig


if __name__ == '__main__':
    my_data = MyData()
    figure = my_data.get_prediction_plot('World', 'new_cases', 100)
    figure.show()
