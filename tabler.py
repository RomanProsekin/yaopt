import numpy as np
import pandas as pd

import formulas


def observ_tp_1(df):
    pvt_obs_1 = df.copy()
    # pvt_obs_1.loc['CNT_MONTH'] = observ['Date'].size / 4
    pvt_obs_1.loc['LAST_COST'] = df.iloc[-1, :]
    pvt_obs_1.loc['MAX'] = df.loc[:, ].max(axis=0)
    pvt_obs_1.loc['MIN'] = df.loc[:, ].min(axis=0)
    pvt_obs_1.loc['MEAN'] = df.loc[:, ].mean(axis=0)
    pvt_obs_1.loc['STD'] = df.loc[:, ].std(axis=0)
    pvt_obs_1.loc['CONFID_COEF'] = df.iloc[:, 1:].dropna().apply(formulas.confid_coef)

    return pvt_obs_1.iloc[-6:].drop('Date', axis=1)


def observ_tp_2(df):
    pvt_obs_2 = df.copy()
    pvt_obs_2.loc['PROFIT'] = df.iloc[:, 1:].apply(formulas.profit)
    pvt_obs_2.loc['STD'] = df.loc[:, ].std(axis=0)
    pvt_obs_2.loc['MAX'] = df.loc[:, ].max(axis=0)
    pvt_obs_2.loc['MIN'] = df.loc[:, ].min(axis=0)
    pvt_obs_2.loc['LAST_COST'] = df.iloc[-1, :]

    return pvt_obs_2.iloc[-5:, 1:]


def observ_tp_3(df):
    pvt_obs_3 = df.copy()
    pvt_obs_3['date_month'] = df.iloc[:, 0].values.astype('<M8[M]')
    pvt_obs_3.drop('Date', axis=1, inplace=True)
    pvt_obs_3 = pvt_obs_3.pivot_table(index=['date_month'],
                                      aggfunc={'mean', formulas.diff_percent},
                                      fill_value=0)

    pvt_obs_3.loc['INCOME'] = pvt_obs_3.iloc[:,
                              [x for x in range(pvt_obs_3.columns.labels[0].__len__()) if x % 2 == 1]].mean(axis=0)

    pvt_obs_3.loc['RISK'] = pvt_obs_3.iloc[:,
                            [x for x in range(pvt_obs_3.columns.labels[0].__len__()) if x % 2 == 1]].std(axis=0)

    return pvt_obs_3


def csv_reader(path, column = None, encoding = 'utf-8', sep=','):
    frame = pd.DataFrame(pd.read_csv(path, encoding=encoding, sep=sep))

    if column == None:
        return frame
    else:
        return frame.loc[:,column]



#CORR matrix
def plot_corr(df,size=10):
    '''Function plots a graphical correlation matrix for each pair of columns in the dataframe.

    Input:
        df: pandas DataFrame
        size: vertical and horizontal size of the plot'''

    corr = df.corr()
    #fig, ax = plt.subplots(figsize=(size, size))
    #plt.xticks(range(len(corr.columns)), corr.columns)
    #plt.yticks(range(len(corr.columns)), corr.columns)

    #ax.matshow(corr)
    return corr

