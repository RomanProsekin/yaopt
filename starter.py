#optimize
from Core.algs.swarm import Swarm_X2
from Core.algs.swarm import printResult


#####
#There is a start function, it's legasy and it will be changed
#####



if __name__ == "__main__":
    ##############
    col_covm = cov_mtx[:,0]


    #INCOME
    incm = markovice_result.loc['INCOME'].values

    income_all = np.array([incm[n] * per_stock[n] for n in range(observ.columns.__len__() - 1)])
    dimension = observ.columns.__len__() - 1
    swarmsize = 200

    minvalues = #np.array([0 if stp not in list(reject_incomes[0]) else identical for stp in range(dimension)])  # min value (start from)
    maxvalues = #np.array([0 if stp not in list(reject_incomes[0]) else formulas.choiser(stp, best_incomes_indexes) for stp in range(dimension)])  # max value (stop)
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













