import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# load data from csv file
def load_data(what, where):
    df = pd.read_csv(f'Data/Clean/time_series_covid19_{what}_{where}.csv')
    return df


# gets date data
def get_date_data(df):
    date_data = df.columns[3:]
    return date_data


# gets data for given country
def get_country_data(df, name):
    if name == 'USA' or name == 'America':
        name = 'US'
    if name == 'UK':
        name = 'United Kingdom'
    country_data = df.loc[df['Location'] == f'{name}'].T[3:]
    if country_data.empty:
        print(f'Could not find "{name}" in table.')
    return country_data


# gets daily cases from cumulative data
def get_daily_cases(df):
    daily = df - df.shift(periods=1, fill_value=0)
    daily.iloc[daily < 0] = 0
    return daily


# gets the moving average of cases
def get_moving_average(df, length=7):
    average = [df[i-length:i].mean() for i in range(length, len(df))]
    padding = [0] * (length // 2)
    return padding + average


# plots cumulative cases for a selection of european countries
def plot_european_data():
    df = load_data(what='confirmed', where='global')

    date_data = get_date_data(df)
    france_data = get_country_data(df, 'France')
    germany_data = get_country_data(df, 'Germany')
    italy_data = get_country_data(df, 'Italy')
    spain_data = get_country_data(df, 'Spain')
    uk_data = get_country_data(df, 'UK')
    
    plt.plot(date_data, france_data, label='France (confirmed)')
    plt.plot(date_data, germany_data, label='Germany')
    plt.plot(date_data, italy_data, label='Italy')
    plt.plot(date_data, spain_data, label='Spain')
    plt.plot(date_data, uk_data, label='UK')

    plt.legend(loc='best')
    plt.grid(True)
    plt.xlabel('Date')
    plt.xticks(date_data[0::50])
    plt.ylabel('Cumulative cases')
    plt.title('European Covid-19 Confirmed Cases')
    plt.tight_layout()
    plt.show()


# plot cases for the US from a selection of perspectives
def plot_us_data():
    df = load_data(what='confirmed', where='global')

    date_data = get_date_data(df)
    us_data = get_country_data(df, 'US')
    us_data_daily = get_daily_cases(us_data)
    us_data_mean = get_moving_average(us_data_daily)
    us_data_log = us_data_daily.replace(0, np.nan)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('US Covid-19 Confirmed Cases')

    ax1.plot(date_data, us_data)
    ax1.grid(True)
    ax1.set(xlabel='Date', ylabel='Cumulative cases')
    ax1.set_xticks(date_data[0::25])
    ax1.set_xticklabels(date_data[0::25], rotation=45)

    ax2.plot(date_data, us_data_daily, linewidth=1, color='tab:orange', label='Raw daily cases', zorder=1)
    ax2.plot(date_data[0:len(us_data_mean)], us_data_mean, '-o', linewidth=1, color='tab:green',
             alpha=0.5, label='Running weekly mean', zorder=2)
    ax2.legend(loc='best')
    ax2.grid(True)
    ax2.set(xlabel='Days (since 22/1/20)', ylabel='Daily cases (linear scale)')
    ax2.set_xticks(date_data[0::25])
    ax2.set_xticklabels(range(0, len(date_data), 25))

    ax3.plot(date_data, us_data_log, linewidth=1, color='tab:red', zorder=1)
    ax3.scatter(date_data, us_data_log, s=10, color='tab:purple', alpha=0.5, zorder=2)
    ax3.set_yscale('log')
    ax3.grid(True)
    ax3.set(xlabel='Date', ylabel='Daily cases (log scale)')
    ax3.set_xticks(date_data[0::25])
    ax3.set_xticklabels(date_data[0::25], rotation=45)

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    plot_european_data()
    plot_us_data()
