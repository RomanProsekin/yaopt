#!/usr/bin/python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod

import numpy
import numpy.random

from Core.algs.swarm.particle import Particle


class Swarm (object):
    """
    Базовый класс для роя частиц. Его надо переопределять для конкретной целевой функции
    """
    __metaclass__ = ABCMeta

    def __init__ (self, 
            swarmsize, 
            minvalues, 
            maxvalues, 
            currentVelocityRatio,
            localVelocityRatio, 
            globalVelocityRatio,
            max_income,
            min_risk):
        """
        swarmsize - размер роя (количество частиц)
        minvalues - список, задающий минимальные значения для каждой координаты частицы
        maxvalues - список, задающий максимальные значения для каждой координаты частицы
        currentVelocityRatio - общий масштабирующий коэффициент для скорости
        localVelocityRatio - коэффициент, задающий влияние лучшей точки, найденной частицей на будущую скорость
        globalVelocityRatio - коэффициент, задающий влияние лучшей точки, найденной всеми частицами на будущую скорость
        """
        self.__swarmsize = swarmsize

        assert len (minvalues) == len (maxvalues)
        assert (localVelocityRatio + globalVelocityRatio) > 0.04   #0.04 is 4 (and everywhere)

        self.__minvalues = numpy.array(minvalues[:])
        self.__maxvalues = numpy.array(maxvalues[:])

        self.__currentVelocityRatio = currentVelocityRatio
        self.__localVelocityRatio = localVelocityRatio
        self.__globalVelocityRatio = globalVelocityRatio

        self.__globalBestFinalFunc = None
        self.__globalBestPosition = None

        self.__swarm = self.__createSwarm ()

        #добавленные
        self.max_income = max_income
        self.min_risk = min_risk


    def __getitem__ (self, index):
        """
        Возвращает частицу с заданным номером
        """
        return self.__swarm[index]


    def __createSwarm (self):
        """
        Создать рой из частиц со случайными координатами
        """
        return [Particle (self) for _ in range (self.__swarmsize) ]



    def nextIteration (self):
        """
        Выполнить следующую итерацию алгоритма
        """
        for particle in self.__swarm:
            particle.nextIteration (self)


    @property
    def minvalues (self):
        return self.__minvalues


    @property
    def maxvalues (self):
        return self.__maxvalues


    @property
    def currentVelocityRatio (self):
        return self.__currentVelocityRatio


    @property
    def localVelocityRatio (self):
        return self.__localVelocityRatio


    @property
    def globalVelocityRatio (self):
        return self.__globalVelocityRatio


    @property
    def globalBestPosition (self):
        return self.__globalBestPosition


    @property
    def globalBestFinalFunc (self):
        return self.__globalBestFinalFunc



    def getFinalFunc (self, position):
        assert len (position) == len (self.minvalues)

        finalFunc = self._finalFunc (position)

        if self.max_income == True and self.min_risk == False:
            # self.__globalBestFinalFunc returns [income, risk]
            if (self.__globalBestFinalFunc == None or
                    finalFunc[0] > self.__globalBestFinalFunc):
                self.__globalBestFinalFunc = finalFunc[0]
                self.__globalBestPosition = position[:]
        else:
            if (self.__globalBestFinalFunc == None or
                    finalFunc[1] < self.__globalBestFinalFunc):
                self.__globalBestFinalFunc = finalFunc[1]
                self.__globalBestPosition = position[:]

        return finalFunc


    @abstractmethod
    def _finalFunc (self, position):
        pass

    
    @property
    def dimension (self):
        """
        Возвращает текущую размерность задачи
        """
        return len (self.minvalues)


    def _getPenalty (self, position, possum):
        """
        Рассчитать штрафную функцию
        position - координаты, для которых рассчитывается штраф
        ratio - вес штрафа
        """

        if possum > 1.0:

            dif = (possum - 1.0) / numpy.where(self.minvalues > 0 )[0].shape[0]

            penalty = numpy.array([dif - coord if coord != 0 else 0.
                            for coord in position])

        else:

            dif = (0.95 - possum) / numpy.where(self.minvalues > 0)[0].shape[0]

            penalty = numpy.array([dif - coord if coord != 0 else 0.
                                   for coord in position])

        return penalty
