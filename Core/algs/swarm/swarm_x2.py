# -*- coding: UTF-8 -*-

from Core.algs.swarm.swarm import Swarm


class Swarm_X2(Swarm):
    def __init__ (self,
            swarmsize, 
            minvalues, 
            maxvalues, 
            currentVelocityRatio,
            localVelocityRatio, 
            globalVelocityRatio,
            cov_matrix,
            markovic_income,
            max_income,
            min_risk):

       # добавленные
       self.cov_matrix = cov_matrix
       self.income = markovic_income
       self.max_income = max_income
       self.min_risk = min_risk


       Swarm.__init__ (self, 
            swarmsize, 
            minvalues, 
            maxvalues, 
            currentVelocityRatio,
            localVelocityRatio, 
            globalVelocityRatio,
            self.cov_matrix,
            self.income,
            self.max_income,
            self.min_risk)






    def _finalFunc (self, position):

        if 1.0 > position.sum() > 0.95:

            #попали в нужный промежуток, штарф не начисляется
            #расчитываем
            # RISK
            risk = position * self.cov_matrix
            risk = risk * position

            #INCOME
            incm = risk * self.income

            return incm.sum(), risk.sum()

        else:

            #вышли за промежуток, получаем штраф
            penalty = self._getPenalty(position, position.sum())

            # расчитываем
            # RISK
            risk = penalty * self.cov_matrix
            risk = risk * penalty

            # INCOME
            incm = risk * self.income
            return incm.sum(), risk.sum()
