#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy

from Core.algs.swarm import Swarm_X2
from Core.algs.swarm import printResult



if __name__ == "__main__":

    iterCount = 300

    dimension = 11
    swarmsize = 200

    minvalues = numpy.array ([0.0] * dimension) #min value (start from)
    maxvalues = numpy.array ([3.0] * dimension) #max value (stop)

    currentVelocityRatio = 0.1
    localVelocityRatio = 1.0
    globalVelocityRatio = 5.0

    swarm = Swarm_X2 (swarmsize, 
            minvalues, 
            maxvalues,
            currentVelocityRatio,
            localVelocityRatio, 
            globalVelocityRatio
            )

    for n in range (iterCount):
        print("Position", swarm[0].position)
        print("Velocity", swarm[0].velocity)

        print(printResult(swarm, n))

        swarm.nextIteration()
