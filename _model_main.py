## Import built packages ##
import pandas as pd
from pyomo.environ import *
from pyomo.opt import SolverStatus, TerminationCondition

## Import model components ##
import _set
import _parameter
import _variable
import _constraint
import _auxi


def data_construction():
    """
    This function constructs the input data object
    """
    # load the sets
    i = [0, 1, 2, 3, 4, 5, 6, 7]
    k = [1]
    t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    set_input = _auxi.SetInput(i, k, t)

    # load the parameters for the production of olefins
    p = {0 : 0, 1 : 3, 2 : 4, 3 : 2, 4 : 2, 5 : 1, 6 : 4, 7 : 0}
    B = {1 : 4}
    Bi = {(0, 1) : 0, (1, 1) : 2, (2, 1) : 3, (3, 1) : 4,
    (4, 1) : 4, (5, 1) : 3, (6, 1) : 2, (7, 1) : 0}

    precedence = {(1, 0) : 1, (2, 0) : 1, (3, 1) : 1, (4, 2) : 1,
    (5, 3) : 1, (6, 4) : 1, (7, 5) : 1, (7, 6) : 1}

    par_input = _auxi.ParaInput(p, B, Bi, precedence)

    return set_input, par_input


def main():
    """
    This is the main function which calls all other functions to solve the
    optimisation model
    """
    # initialise the concreteModel
    Shangfei_model = ConcreteModel()

    # get the data input as objects
    # Excel_file = 'Borouge_Data_Final_PYTHON.xlsx'
    set_input, par_input = data_construction()

    # set initialisation
    _set.set_initialisation(Shangfei_model, set_input)

    # parameter initialisation
    _parameter.parameter_initialisation(Shangfei_model, par_input)

    # variable initialisation
    _variable.variable_initialisation(Shangfei_model)

    # constraint initialisation
    _constraint.constraint_definition(Shangfei_model)

    # set up the model
    opt = SolverFactory('CBC.exe')
    #opt.options['mipgap'] = 0.001
    #opt.options['threads'] = 0

    results = opt.solve(Shangfei_model, tee = True,
    symbolic_solver_labels = True)

    Shangfei_model.solutions.store_to(Shangfei_results)
    Shangfei_results.write(filename = 'Shangfei_solution.yml')


if __name__ == '__main__':
    main()
