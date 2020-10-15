import pandas as pd


# gets data from github repository (updated daily) and saves it in both raw and cleaned form
def update_data():
    names = ['confirmed_US', 'confirmed_global', 'deaths_US', 'deaths_global', 'recovered_global']
    dfs = {}
    for name in names:
        df = read_data(name)
        # save raw data
        save_data(df, f'Data/Raw/time_series_covid19_{name}')
        if name in ['confirmed_US', 'deaths_US']:
            df = process_us_data(df, name)
        elif name in ['confirmed_global', 'deaths_global', 'recovered_global']:
            df = process_global_data(df)
        dfs[name] = df
    # save clean uncombined data
    for key in dfs:
        save_data(dfs[key], f'Data/Clean/time_series_covid19_{key}')
    dfs = combine_global_us_data(dfs)
    # save clean combined data
    for key in dfs:
        save_data(dfs[key], f'Data/Clean/time_series_covid19_{key}')


# reads data from csv url
def read_data(name):
    base_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data' \
               '/csse_covid_19_time_series/time_series_covid19_'
    df = pd.read_csv(base_url + name + '.csv')
    return df


# saves data to csv file
def save_data(df, name):
    df.to_csv(name + '.csv', index=False)


# processes US data into desired format
def process_us_data(df, name):
    # drop unwanted columns
    df = df.drop(columns=['UID', 'iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Country_Region', 'Combined_Key'])
    if name == 'deaths_US':
        df = df.drop(columns='Population')
    # rename header names
    df.rename(columns={'Long_': 'Long', 'Province_State': 'Location'}, inplace=True)
    df = process_all_data(df)
    # group rows by province taking the mean of longitude/ latitude values while summing case numbers
    df = df.groupby('Location', as_index=False).agg({**{'Lat': 'mean', 'Long': 'mean'},
                                                     **{value: 'sum' for value in df.columns[3:].values}})
    return df


# processes global data into desired format
def process_global_data(df):
    # combine both location columns into one, giving priority to province/ state
    df['Province/State'] = df['Province/State'].fillna(df['Country/Region'])
    df.rename(columns={'Province/State': 'Location'}, inplace=True)
    df = df.drop(columns='Country/Region')
    df = process_all_data(df)
    return df


# processes all data into desired format
def process_all_data(df):
    # change date format in header names
    df.columns = [header.split('/')[1] + '/' + header.split('/')[0] + '/' + header.split('/')[2]
                  if header not in ['Location', 'Lat', 'Long'] else header for header in df.columns.values]
    # remove rows with no positional data
    df = df.loc[df['Lat'] != 0 & (df['Long'] != 0)]
    return df


# combines global and US data
def combine_global_us_data(dfs):
    # remove total US row from global data
    names = ['confirmed_global', 'deaths_global']
    for name in names:
        dfs[name] = dfs[name].loc[dfs[name]['Location'] != 'US']
    new_dfs = {'confirmed_global_US': pd.concat([dfs['confirmed_global'], dfs['confirmed_US']]),
               'deaths_global_US': pd.concat([dfs['deaths_global'], dfs['deaths_US']])}
    return new_dfs


if __name__ == '__main__':
    update_data()
