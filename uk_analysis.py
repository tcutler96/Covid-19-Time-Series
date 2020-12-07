import pandas as pd
import matplotlib.pyplot as plt


# loads covid data
def load_data():
    df = pd.read_csv('Data/UK/Clean/confirmed_deaths_age.csv').set_index('Week Ended')
    return df


# processes covid data into desired age groupds
def process_data(df, age_groups):
    age_ranges = [f'0-{age_group.split("-")[-1]}' for age_group in age_groups[:-1]] + ['0+']
    for index, age_range in enumerate(age_ranges):
        if index < len(age_ranges) - 1:
            end_age = age_range.split('-')[-1]
        else:
            end_age = '90+'
        for i, header in enumerate(df.columns):
            if end_age in header:
                stop_i = i + 1
        df[age_range] = df.iloc[:, :stop_i].sum(axis=1)
    return df, age_ranges


# plots covid data
def plot_uk_data():
    # age groups to separate data into
    age_groups = ['0-49', '50-59', '60-69', '70-79', '80-84', '85-89', '90+']

    # load and process data
    df = load_data()
    df, age_ranges = process_data(df, age_groups)

    # main control
    plt.figure(figsize=(10, 5))
    for index, age_range in enumerate(reversed(age_ranges)):
        plt.bar(df.index, df[age_range], label=' ')

    # process data
    xticks = df.index[::2]
    xlabels = pd.to_datetime(xticks, dayfirst=True).strftime('%d %b %y')
    deaths = [0] + list(df[age_ranges].sum())
    death_percents = [round((death - deaths[index]) / deaths[-1] * 100, 2) for index, death in enumerate(deaths[1:])]
    legend_label = [f'{age_group} ({percent}%)' for percent, age_group in zip(reversed(death_percents), reversed(age_groups))]

    # plot control
    ax = plt.gca()
    ax.set_xlabel('Week Ending')
    ax.set_xticks(ticks=xticks)
    ax.set_xticklabels(labels=xlabels, rotation=50, fontsize=9)
    ax.set_ylabel('Number of Cases')
    ax.set_title('Weekly UK Deaths Involving Covid-19 by Age Groups')
    handles, _ = ax.get_legend_handles_labels()
    ax.legend(handles, legend_label, title='Age (% of total deaths)', edgecolor='k', fancybox=True)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    plot_uk_data()
