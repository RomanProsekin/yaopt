import sys
from os import listdir, walk
from itertools import product, filterfalse, starmap, permutations
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import tabler
import formulas

#optimize
from swarm_optimization.swarm_x2 import Swarm_X2
from swarm_optimization.utils import printResult

#constants
hub = 'csv_hub'


#funcs
def get_direcotries(hub):
    '''
    :param hub: 
    :return: list of forlders
     
     0 - main folder
     1 - folders in
     2 - other files
    '''
    return next(walk(hub))[1]

def get_names(path):
    return listdir(path), [one.split('.')[0] for one in listdir(path)]










if __name__ == "__main__":
    print('Choice one:')
    [print(num, dr) for num, dr in enumerate(get_direcotries(hub))]
    directory = int(input('->'))
    directory = get_direcotries(hub)[directory]

    names = get_names('{}/{}'.format(hub, directory))

    #create observe

    for n in range(names[0].__len__()):

        print(names[0][n])

        path_csv = '{}/{}/{}'.format(hub, directory, names[0][n])

        if n == 0:
            #, 'latin-1',';'
            observ = tabler.csv_reader(path_csv, ['Date', 'Open']).rename(columns = {'Open':names[1][n]})
            #observ[names[1][n]] = pd.Series([float(i.replace(',', '.')) for i in observ[names[1][n]].values if type(i) == str])  # apply(lambda x: x.replace(',','.')).convert_objects(convert_numeric=True)

        #elif names[1][n] == 'BOND' or names[1][n] == 'LYG' or names[1][n] == 'FWHEAT':
        #    observ = pd.concat([observ, tabler.csv_reader(path_csv, ['Date', 'Open']).drop('Date', axis=1).rename(columns={'Open': names[1][n]})], axis=1, join_axes=[observ.index])

        else:
            observ = pd.concat([observ, tabler.csv_reader(path_csv, ['Date', 'Open']).drop('Date', axis = 1).rename(columns = {'Open':names[1][n]})], axis=1, join_axes=[observ.index])

            #observ[names[1][n]] = pd.Series([float(i.replace(',', '.')) for i in observ[names[1][n]].values if type(i) == str])  # apply(lambda x: x.replace(',','.')).convert_objects(convert_numeric=True)

        #changer currency
        if names[1][n] == 'COSCO':
            observ[names[1][n]] = observ[names[1][n]].values * 0.13
        elif names[1][n] == 'DANO':
            observ[names[1][n]] = observ[names[1][n]].values * 1.13
        elif names[1][n] == 'MAERSK-A':
            observ[names[1][n]] = observ[names[1][n]].values * 0.15
        elif names[1][n] == 'THAI':
            observ[names[1][n]] = observ[names[1][n]].values * 0.031
        else: pass

    #pivot of observed
    pvt_obs_1 = tabler.observ_tp_1(observ)



    #observe with income

    pvt_obs_2 = tabler.observ_tp_2(observ)
    #step 2 done


    #step 3

    observ.iloc[:, 0] = pd.to_datetime(observ.iloc[:, 0])
    pvt_obs_3 = tabler.observ_tp_3(observ)

    income = pvt_obs_3.iloc[-2,[x for x in range(pvt_obs_3.columns.labels[0].__len__()) if x%2 == 1 ]]
    rick =  pvt_obs_3.iloc[-1,[x for x in range(pvt_obs_3.columns.labels[0].__len__()) if x%2 == 1 ]]


    #print(pvt_obs_1)
    #step 3 done

    #corrilation matrix
    corr = tabler.plot_corr(observ[observ.columns[1:]])
    #print(corr)

    #step 4 cov_matrix and Markovice portfolio
    observ.iloc[:, 0] = pd.to_datetime(observ.iloc[:, 0])
    markovice_result = observ.copy()
    markovice_result['date_month'] = observ.iloc[:, 0].values.astype('<M8[M]')


    income_matrix = markovice_result.pivot_table(index = ['date_month'],
                                      aggfunc = {formulas.diff_percent},
                                      fill_value = 0).reset_index().drop('date_month', axis = 1, level = 0)#.values

    markovice_result = markovice_result.drop(['Date','date_month'], axis = 1).fillna(0)

    cov_mtx = formulas.cov_matrix(income_matrix)


    #Base data
    print('Base Data')
    col_covm = cov_mtx[:,0]
    per_stock = np.array([((observ.columns.__len__() - 1) / (observ.columns.__len__() - 1)) / (observ.columns.__len__() - 1) for _ in range(observ.columns.__len__() - 1)])

    #print(markovice_result.iloc[:,])

    markovice_result.loc['INCOME'] = markovice_result.iloc[:,].apply(formulas.expincome)

    markovice_result.loc['RISK'] = markovice_result.iloc[:-1,].apply(formulas.exprisk)

    markovice_result.loc['STOK_PRC'] = per_stock

    print(markovice_result.iloc[-3:-1])


    #RISK
    res1 = per_stock * col_covm
    res2 = res1 * per_stock

    #INCOME
    incm = markovice_result.loc['INCOME'].values

    income_all = np.array([incm[n] * per_stock[n] for n in range(observ.columns.__len__() - 1)])

    print('\nRisk is ', res2.sum())

    print('\nIncome is ', income_all.sum())


    print('Rolling is comming...')
    #Search all variance
    #min stockes in a portpholio
    min_cnt_stock = 3

    #min, max variables and whether 0 or not
    per_max = (min_cnt_stock / (observ.columns.__len__() - 1))
    per_min = 0.0
    step = 0.015

    vars = np.arange(per_min, per_max, step)
    #####

    print(vars)

    iterCount = 300

    dimension = observ.columns.__len__() - 1
    swarmsize = 200

    #get list of max values
    best_incomes_indexes = np.where(np.isin(income_all, sorted(income_all, reverse=True)[:min_cnt_stock]))[0]
    reject_incomes = np.where(np.array(income_all) > 0) # cause they are 0 or -

    #because there couldn't 0/- values
    try:
        identical = 1.0 / reject_incomes[0].shape[0]
    except ZeroDivisionError:
        identical = 1.0 / dimension

    minvalues = np.array([0 if stp not in list(reject_incomes[0]) else identical for stp in range(dimension)])  # min value (start from)
    maxvalues = np.array([0 if stp not in list(reject_incomes[0]) else formulas.choiser(stp, best_incomes_indexes) for stp in range(dimension)])  # max value (stop)
    #print(minvalues, maxvalues)


    currentVelocityRatio = 0.0015
    localVelocityRatio = 0.001
    globalVelocityRatio = 0.05

    max_income, min_risk = [True, False] #взаимосвязные параметры, в зависимости от того, что ищем

    swarm = Swarm_X2(swarmsize,
                     minvalues,
                     maxvalues,
                     currentVelocityRatio,
                     localVelocityRatio,
                     globalVelocityRatio,
                     col_covm,
                     incm,
                     max_income,
                     min_risk)


    #отлично! осталось выбрать параметр, больше риск или больше доход
    #меняем знак в getFinalFunc (self, position) и везде, где она появляется)


    for n in range(iterCount):
        #print("Position", swarm[0].position)
        #print("Velocity", swarm[0].velocity)

        #print(printResult(swarm, n))

        swarm.nextIteration()

    result_table = markovice_result.iloc[-3:-1]

    if min_risk == True:
        # расчитываем
        # RISK
        position, _ = printResult(swarm, n)
        risk = position * col_covm
        risk = risk * position

        # INCOME
        incm = risk * incm

        #print(position, incm.sum())

        result_table.loc['% in P'] = position * 100

        result_table.loc['EX_RISK'] = np.array([risk.sum() if n == 0 else 0 for n in range(dimension)])
        result_table.loc['EX_INCOME'] = np.array([incm.sum() if n == 0 else 0 for n in range(dimension)])


    else:
        position, incm = printResult(swarm, n)

        risk = position * col_covm
        risk = risk * position

        #print(printResult(swarm, n))

        result_table.loc['% in P'] = position * 100

        result_table.loc['EX_RISK'] = np.array([risk.sum() if n == 0 else 0 for n in range(dimension)])
        result_table.loc['EX_INCOME'] = np.array([incm if n == 0 else 0 for n in range(dimension)])

    #print(result_table)

    #when I want to print int
    #pvt_obs_1.loc['INCOME'] = income.values
    #pvt_obs_1.loc['RISK'] = rick.values

    result_table = result_table.style.format("{:.2f}").render()
    with open('result_table_main.html', 'w+') as f:
        f.write(result_table)













