# -*- coding: UTF-8 -*-

def printResult (swarm, iteration):
    template = u"""Count of Iterations: {iter}
                   Best Position: {bestpos}
                   Best Final Func: {finalfunc}
                   ----------------------------
                   """

    result = template.format(iter = iteration,
                             bestpos = swarm.globalBestPosition,
                             finalfunc = swarm.globalBestFinalFunc)

    #return result
    return swarm.globalBestPosition, swarm.globalBestFinalFunc
