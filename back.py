import os
import pandas as pd
from datetime import datetime, timedelta

columns = ['iso_code', 'date', 'location',
           'new_cases', 'total_cases', 'new_cases_per_million', 'total_cases_per_million',
           'new_deaths', 'total_deaths', 'new_deaths_per_million', 'total_deaths_per_million']
last_data_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
_path = 'assets/data/'
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
            self.df.to_csv(_path + _filename, index=False)
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


if __name__ == '__main__':
    my_data = MyData()
    df = my_data.get_last().sort_values
    print(my_data.get_country_coords('Russia'))
