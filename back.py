import os
import tools
import pandas as pd
import pmdarima as pm
import plotly.graph_objects as go
from datetime import datetime, timedelta

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
        if _filename in _csv_files:
            self.df = pd.read_csv(f'{_path}/{_filename}')[columns].fillna(0)
        else:
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

    def predict(self, country, indicator, periods, start_p, start_q, max_p, max_q) -> dict:
        df_real = self.df[self.df['location'] == country][[indicator, 'date']].fillna(0).reset_index(drop=True)

        model = pm.auto_arima(df_real[[indicator]], start_p=start_p, start_q=start_q,
                              test='kpss',
                              max_p=max_p, max_q=max_q,
                              m=1,
                              d=None,
                              seasonal=False,
                              trace=True,
                              error_action='ignore',
                              suppress_warnings=True,
                              stepwise=False)
        forecast, confint = model.predict(periods, return_conf_int=True)

        fc_start = datetime.strptime(max(df_real['date']), '%Y-%m-%d') + timedelta(days=1)
        fc_dates = [fc_start + timedelta(days=i) for i in range(100)]

        index_of_fc = fc_dates  # np.arange(len(df_real), len(df_real) + periods)
        forecast_series = pd.Series(forecast, index=index_of_fc)
        lower_series = pd.Series(confint[:, 0], index=index_of_fc)
        upper_series = pd.Series(confint[:, 1], index=index_of_fc)
        return {'real': df_real, 'fc_index': index_of_fc, 'forecast': forecast_series, 'lower': lower_series,
                'upper': upper_series}

    def get_prediction_plot(self, country='World', indicator='new_cases', periods=100,
                            start_p=0, start_q=0, max_p=3, max_q=3):
        res = self.predict(country, indicator, periods, start_p, start_q, max_p, max_q)
        fig = go.Figure()
        # Real
        fig.add_trace(go.Scatter(x=res['real']['date'].to_list(), y=res['real'][indicator].to_list(), name='Real'))
        # Lower confidence interval
        fig.add_trace(go.Scatter(x=res['fc_index'], y=res['lower'].to_list(), showlegend=False, mode='lines',
                                 line=dict(width=.5, color='#9cc3c3'), hoverinfo='none'))
        # Upper confidence interval
        fig.add_trace(go.Scatter(x=res['fc_index'], y=res['upper'].to_list(), mode='lines', showlegend=False,
                                 fill='tonexty', line=dict(width=.5, color='#9cc3c3'), hoverinfo='none'))
        # Prediction
        fig.add_trace(go.Scatter(x=res['fc_index'], y=res['forecast'].to_list(), name='Prediction',
                                 line=dict(width=1.5, color='#2be4b1')))
        tools.update_pred_fig(fig)
        return fig


if __name__ == '__main__':
    my_data = MyData()
    figure = my_data.get_prediction_plot(country='United States')
    figure.show(config={'scrollZoom': True})
