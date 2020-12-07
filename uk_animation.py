import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as patches
import matplotlib.cm as cm
import shapefile as shp


# loads covid and map data
def load_data():
    df = pd.read_csv('Data/UK/Clean/deaths_region.csv').set_index('Date')
    sf = shp.Reader('Data/UK/Map/uk.shp')
    return df, sf


# plots map from shapefile
def plot_map(sf):
    fig, ax = plt.subplots(figsize=(8, 9))
    lines = []
    fills = []
    regions = []
    for shape in sf.shapeRecords():
        i_start = shape.shape.parts[0]
        if 0 == len(shape.shape.parts) - 1:
            i_end = len(shape.shape.points)
        else:
            i_end = shape.shape.parts[0 + 1]
        x = [i[0] for i in shape.shape.points[i_start:i_end]]
        y = [i[1] for i in shape.shape.points[i_start:i_end]]
        l, = ax.plot(x, y, linewidth=0.5, c='black')
        lines.append(l)
        f, = ax.fill(x, y, 'white')
        fills.append(f)
        region = shape.record[2]
        if region.split()[-1] == '(England)':
            region = region.rsplit(' ', 1)[0]
        if region == 'East of England':
            region = 'East'
        regions.append(region)
    date_label = ax.text(0.02, 0.965, '', transform=ax.transAxes, bbox=dict(boxstyle='round', fill=False,
                                                                            linewidth=0.85))
    return fig, ax, lines, fills, date_label, regions


# processes covid data into desired format
def process_data(df, regions):
    new_header = df.iloc[2]
    df = df.iloc[6:-14]
    df.columns = new_header
    df.set_index('Date', inplace=True)
    df = df[regions].astype('int32')
    num_days = df.shape[0]
    return df, num_days


# animates covid data
def animate_uk_covid(cont_colour=True, interval=150, repeat=False):
    # load all data
    df, sf = load_data()

    # initialise plot objects
    fig, ax, lines, fills, date_label, regions = plot_map(sf)

    # process data
    num_days = df.shape[0]
    max_cases = df.max().max()
    if cont_colour:
        step_size = 50
        max_new = (max_cases // step_size) * step_size
        cmap = cm.get_cmap('YlGnBu')
        leg_ticks = list(range(0, max_new, step_size))
        leg_ticks.append(f'{max_new}+')
    else:
        step_size = 25
        max_new = (max_cases // step_size) * step_size
        colour_range = [(0.8, 1.0, 0.95), (0.7, 1.0, 0.93), (0.6, 1.0, 0.91), (0.5, 1.0, 0.88),
                        (0.4, 1.0, 0.86), (0.3, 1.0, 0.84), (0.2, 1.0, 0.81), (0.1, 1.0, 0.79),
                        (0.0, 1.0, 0.76), (0.0, 0.9, 0.69), (0.0, 0.8, 0.61), (0.0, 0.7, 0.54),
                        (0.0, 0.6, 0.46), (0.0, 0.5, 0.38), (0.0, 0.4, 0.31), (0.0, 0.3, 0.23),
                        (0.0, 0.2, 0.15)]
        ranges = [[0, 0, colour_range[0]]]
        num_steps = (max_new // step_size) + 1
        for step in range(1, num_steps):
            ranges.append([(step - 1) * step_size, (step * step_size) - 1,
                           colour_range[len(colour_range) * step // num_steps]])
        ranges[1][0] = 1
        ranges.append([max_new, 99999, colour_range[-1]])
        ranges_dict = {}
        for index, r in enumerate(ranges):
            if index == 0:
                range_str = f'{r[0]}'
            elif index < len(ranges) - 1:
                range_str = f'{r[0]}-{r[1]}'
            else:
                range_str = f'{r[0]}+'
            ranges_dict[range_str] = r[2]

    # blits clean plot
    def init():
        date_label.set_text('')
        for line in lines:
            line.set_color('black')
        for fill in fills:
            fill.set_color('white')
        return date_label, lines[0], lines[1], lines[2], lines[3], lines[4], lines[5], lines[6], \
            lines[7], lines[8], lines[9], lines[10], lines[11], fills[0], fills[1], fills[2], \
            fills[3], fills[4], fills[5], fills[6], fills[7], fills[8], fills[9], fills[10], fills[11],

    # updates plot every frame
    def animate(i):
        date_label.set_text(f'Date: {df.index[i]}')
        for i2, fill in enumerate(fills):
            value = df.iloc[i][i2]
            if cont_colour:
                colour = cmap(value / max_new)[:-1]
            else:
                for case_range in ranges:
                    if case_range[0] <= value <= case_range[1]:
                        colour = case_range[2]
            fill.set_color(colour)
        return date_label, lines[0], lines[1], lines[2], lines[3], lines[4], lines[5], lines[6], \
            lines[7], lines[8], lines[9], lines[10], lines[11], fills[0], fills[1], fills[2], \
            fills[3], fills[4], fills[5], fills[6], fills[7], fills[8], fills[9], fills[10], fills[11],

    # run animation
    FuncAnimation(fig, animate, frames=num_days, init_func=init, interval=interval,
                  blit=True, repeat=repeat, repeat_delay=5000)

    # plot control
    plt.title('Daily UK Covid-19 Related Deaths*')
    plt.xticks([])
    plt.yticks([])
    ax.text(0.325, 0.02, '*That is, daily provisional death occurrences in the UK where Covid-19 was mentioned \n '
                         'anywhere on the death certificate, including in combination with other health conditions.',
            transform=ax.transAxes, fontsize=6.5, bbox=dict(boxstyle='round', fill=False, linewidth=0.85))
    if cont_colour:
        leg_bar = np.linspace(0, 1, max_new + 1).reshape(max_new + 1, 1)
        cax = fig.add_axes([0.62, 0.46, 0.4, 0.4], frameon=False, xticks=[],
                           yticks=np.arange(max_new + 1, 0, -step_size), yticklabels=leg_ticks)
        cax.yaxis.tick_right()
        cax.tick_params(axis='y', length=0)
        cax.imshow(leg_bar, cmap=cmap, extent=[0, 25, 0, max_new + 1])
    else:
        legends = [patches.Rectangle((0, 0), 1, 1, facecolor=ranges_dict[i]) for i in ranges_dict]
        legend = plt.legend(legends, list(ranges_dict.keys()), handlelength=1, handleheight=1)
        legend.get_frame().set_facecolor('none')
        legend.get_frame().set_edgecolor('black')
    plt.show()


if __name__ == '__main__':
    animate_uk_covid(cont_colour=True, interval=250, repeat=False)
