import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
import shapefile


# load data from csv file
def load_data(what, where):
    df = pd.read_csv(f'Data/Clean/time_series_covid19_{what}_{where}.csv')
    return df


# plots each country according to its longitude and latitude
def plot_country_points(df, label):
    for index, row in df.iterrows():
        name = row['Location']
        lat = row['Lat']
        long = row['Long']
        plt.scatter(long, lat, c='none', edgecolors='tab:blue', s=10, alpha=0.75)
        if label:
            plt.annotate(name, (long + 0.5, lat + 0.5), size=7, c='tab:purple')


# plots world map from a shapefile and countries from data
def plot_world_map(show=False, countries=False, label=True):
    sf = shapefile.Reader('Data/World Map/world_map.shp')
    for shape in sf.shapeRecords():
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            if i == len(shape.shape.parts) - 1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i + 1]
            x = [i[0] for i in shape.shape.points[i_start:i_end]]
            y = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(x, y, linewidth=0.5, c='tab:gray')
    # plot country points
    if countries:
        df = load_data('confirmed', 'global_US')
        plot_country_points(df, label)
    if show:
        plt.title('World Map')
        plt.xlabel('Longitude ($\degree$)')
        plt.ylabel('Latitude ($\degree$)')
        # maximise window
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')
        plt.show()


# processes data ready for plotting
def process_data(df, plot_daily, plot_log):
    long = df['Long'].values
    lat = df['Lat'].values
    dates = df.columns[3:].values
    num_days = len(dates)
    plot_data = df.T[3:]
    # daily or cumulative cases
    if plot_daily:
        plot_data = plot_data - plot_data.shift(periods=1, fill_value=0)
    plot_data.iloc[plot_data <= 0] = np.nan
    # logarithmic or linear size scale
    if plot_log:
        plot_sizes = 50 * np.log(plot_data.astype('float64'))
    else:
        plot_sizes = plot_data.astype('float64') / 50
    return plot_sizes, long, lat, dates, num_days


# animates data time series
def animate_time_series(what='confirmed', where='global_US', plot_daily=True, plot_log=True,
                        interval=150, repeat=False):
    # ensure proper options are chosen
    if what not in ['confirmed', 'deaths', 'recovered', 'all']:
        print('"what" options: confirmed, deaths, recovered', 'all')
        return
    if where not in ['global', 'global_US', 'US']:
        print('"where" options: global, global_US, US')
        return
    if what == 'recovered':
        where = 'global'

    # blits clean plot
    def init():
        date_label.set_text('')
        if what == 'all':
            scat1.set_sizes([0] * num_days)
            scat2.set_sizes([0] * num_days)
            scat3.set_sizes([0] * num_days)
            return scat1, scat2, scat3, date_label,
        else:
            scat.set_sizes([0] * num_days)
            return scat, date_label,

    # updates plot every frame
    def animate(i):
        date_label.set_text(f'Date: {dates[i]}')
        if what == 'all':
            scat1.set_sizes(plot_sizes1.iloc[i])
            scat2.set_sizes(plot_sizes2.iloc[i])
            scat3.set_sizes(plot_sizes3.iloc[i])
            return scat1, scat2, scat3, date_label,
        else:
            scat.set_sizes(plot_sizes.iloc[i])
            return scat, date_label,

    # get all necessary data
    if what == 'all':
        df1 = load_data('confirmed', 'global_US')
        df2 = load_data('deaths', 'global_US')
        df3 = load_data('recovered', 'global')
        plot_sizes1, long1, lat1, dates, num_days = process_data(df1, True, False)
        plot_sizes2, long2, lat2, dates, num_days = process_data(df2, False, True)
        plot_sizes3, long3, lat3, dates, num_days = process_data(df3, False, True)
    else:
        df = load_data(what, where)
        plot_sizes, long, lat, dates, num_days = process_data(df, plot_daily, plot_log)

    # initialise figure, scatter and label objects
    fig, ax = plt.subplots()
    if what == 'all':
        scat1 = ax.scatter(long1, lat1, s=0, c='tab:orange', edgecolors='tab:red', alpha=0.5, zorder=3)
        scat2 = ax.scatter(long2, lat2, s=0, c='tab:grey', edgecolors='tab:purple', alpha=0.25, zorder=2)
        scat3 = ax.scatter(long3, lat3, s=0, c='tab:green', edgecolors='tab:blue', alpha=0.25, zorder=1)
    else:
        if what == 'confirmed':
            main_colour = 'tab:orange'
            edge_colour = 'tab:red'
        elif what == 'deaths':
            main_colour = 'tab:grey'
            edge_colour = 'tab:purple'
        elif what == 'recovered':
            main_colour = 'tab:green'
            edge_colour = 'tab:blue'
        scat = ax.scatter(long, lat, s=0, c=main_colour, edgecolors=edge_colour, alpha=0.5, zorder=3, label='Confirmed')
    date_label = ax.text(-195, 87, '', fontsize=10)

    # run animation
    FuncAnimation(fig, animate, frames=num_days, init_func=init, interval=interval,
                  blit=True, repeat=repeat, repeat_delay=5000)

    # overlay world map
    plot_world_map()
    plt.title('Global Covid-19 Time Series')
    # add legend for all cases
    if what == 'all':
        legend1 = Line2D(range(1), range(1), color='white', marker='o', markersize=10,
                         markerfacecolor='tab:orange', alpha=0.75)
        legend2 = Line2D(range(1), range(1), color='white', marker='o', markersize=10,
                         markerfacecolor='tab:grey', alpha=0.75)
        legend3 = Line2D(range(1), range(1), color='white', marker='o', markersize=10,
                         markerfacecolor='tab:green', alpha=0.75)
        plt.legend((legend1, legend2, legend3), ('Confirmed', 'Deaths', 'Recovered'), loc=1)
    plt.xlabel('Longitude ($\degree$)')
    plt.ylabel('Latitude ($\degree$)')
    # maximise window
    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()


if __name__ == '__main__':
    plot_world_map(show=True, countries=True, label=True)
    animate_time_series(what='confirmed', where='global_US', plot_daily=True, plot_log=True,
                        interval=150, repeat=False)
