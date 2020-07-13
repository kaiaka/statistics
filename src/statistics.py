import pandas as pd
from scipy.stats import friedmanchisquare
from scipy.stats import f_oneway


def read_data(path):
    print('---------------------------------------------')
    print('Reading data from: ' + path)
    print('---------------------------------------------')
    df = pd.read_csv(path)
    print(df.head())
    return df


def analysis(df):
    print('---------------------------------------------')
    print('-- Analysis --')
    print('---------------------------------------------')

    # analyse rating for each scenario A B C
    independent_vars = ['A', 'B', 'C']

    for iv in independent_vars:
        print('Analyzing scenario {}:'.format(iv))

        # filter: get only data for selected scenario
        df_scenario = df.loc[df['scenario'] == iv]

        # basics
        mean = df_scenario['rating'].mean()
        std = df_scenario['rating'].std()
        print('- mean: {} '.format(mean))
        print('- standard deviation: {} '.format(std))

    # significance tests
    rating_A = df.loc[df['scenario'] == 'A']['rating']
    rating_B = df.loc[df['scenario'] == 'B']['rating']
    rating_C = df.loc[df['scenario'] == 'C']['rating']
    print('')

    print('Friedman')
    stat, p = friedmanchisquare(rating_A, rating_B, rating_C)
    significance = p < 0.05
    print('stat={:.3f} p={:.3f} significant={}'.format(stat, p, significance))

    print('ANOVA')
    significance = 'no'
    stat, p = f_oneway(rating_A, rating_B, rating_C)
    significance = p < 0.05
    print('stat={:.3f} p={:.3f} significant={}'.format(stat, p, significance))

    print('---------------------------------------------')

# - - - - - - - - - - - - - - - - - - - - - - - - - -
# https://cyfar.org/types-statistical-tests
# https://stats.idre.ucla.edu/other/mult-pkg/whatstat/
# https://machinelearningmastery.com/statistical-hypothesis-tests-in-python-cheat-sheet/
data = read_data('../data/example.csv')
analysis(data)


