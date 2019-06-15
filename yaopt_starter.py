# -*- coding: UTF-8 -*-
import numpy.random as random
import os
from Core.op_types import Optset


#constants
CPUS = os.cpu_count()


def optdriver(alg, params, set_x, set_y, threades = CPUS):
    """
    Main function starts the optimization process

    :param alg:
    :param params:
    :param set_x:
    :param set_y:
    :return:
    """

    def shuffle_dict(params):

        params_set = dict()

        for key in params.keys():
            print(params[key].values)
            values = params[key].values

            #shuffle only marked sets
            if params[key].is_shuffle == True:
                random.shuffle(values)

            #create new shuffled / unshuffled
            params_set[key] = values

        return params_set

    params_set = shuffle_dict(params)

    #################################
    class OPTDriver(alg):

        def __init__(self):
            assert 'fit' in dir(alg), 'Class {} does not have necessary attributes '.format(self.__class__.__bases__[0].__name__)
            assert 'get_params' in dir(alg), 'Class {} does not have necessary attributes '.format(self.__class__.__bases__[0].__name__)
            assert 'predict' in dir(alg), 'Class {} does not have necessary attributes '.format(self.__class__.__bases__[0].__name__)

            alg.__init__(self)


        def printer(self):
            print('Vouola!')


    return OPTDriver()




if __name__ == "__main__":


    import sklearn
    from sklearn.ensemble import RandomForestClassifier


    alg = RandomForestClassifier
    params = {'n_estimators' : Optset([100,1,3,4])}


    #print(alg.__class__)
    #ins = inspect.getmembers(alg)
    set_x, set_y = 0, 0
    #послывать без скобочек, не запущенный в init
    opt = optdriver(alg, params, set_x, set_y)
    #print(opt.__class__.__bases__[0].__name__)
    #print(opt.__class__)

    #opt.printer()

