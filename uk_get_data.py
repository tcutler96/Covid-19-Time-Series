import pandas as pd


# reads, processes and then saves data in cleaned form
def update_data():
    file_name = 'publishedweek472020'
    sheet_names = ['Covid-19 - Daily occurrences', 'Covid-19 - Weekly occurrences']
    dfs = read_data(file_name, sheet_names)
    for index, df in enumerate(dfs):
        if index == 0:
            name = 'deaths_region'
            df = process_daily_date(df)
        else:
            name = 'confirmed_deaths_age'
            week_number = int(file_name[-6:-4])
            df = process_weekly_data(df, week_number)
        save_data(df, f'Data/UK/Clean/{name}', True)


# reads data from excel file
def read_data(name, sheets):
    xls = pd.ExcelFile(f'Data/UK/Raw/{name}.xlsx')
    dfs = []
    for sheet in sheets:
        dfs.append(pd.read_excel(xls, sheet_name=sheet))
    return dfs


# saves data to csv file
def save_data(df, name, index):
    df.to_csv(name + '.csv', index=index)


# processes daily data into desired format
def process_daily_date(df):
    regions = ['North East', 'North West', 'Yorkshire and The Humber', 'East Midlands', 'West Midlands',
               'East', 'London', 'South East', 'South West', 'Wales', 'Scotland', 'Northern Ireland']
    new_header = df.iloc[2]
    df.dropna(axis=0, how='all', inplace=True)
    df = df.iloc[6:-14]
    df.columns = new_header
    df.set_index('Date', inplace=True)
    df = df[regions].astype('int32')
    return df


# processes weekly data into desired format
def process_weekly_data(df, week_number):
    new_index = pd.to_datetime(df.iloc[4, 2:week_number + 2]).dt.strftime('%d/%m/%Y')
    new_header = df['Unnamed: 1'].iloc[10:30]
    df = df.iloc[10:30, 2:week_number + 2].fillna(0).T.set_index(new_index)
    df.columns = new_header
    df.index.name = 'Week Ended'
    return df


if __name__ == '__main__':
    update_data()

