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
    print('Reading excel......')
    excel_file = 'precedence.xlsx'
    # load the sets
    #i = [0, 1, 2, 3, 4, 5, 6, 7]
    print('Initialising set......')
    i = _auxi.read_precedence(excel_file)[0]
    k = _auxi.get_resouce_set(excel_file)
    t = [time_int for time_int in range(250)]

    set_input = _auxi.SetInput(i, k, t)
    print('Initialising paramters......')
    # load the parameters for the production of olefins
    p = _auxi.read_process_time(excel_file)
    B = {'机械' : 38,  '结构' : 28, '特设' : 33}
    Bi = _auxi.get_resource_consumption(excel_file)

    precedence = _auxi.convert_precedence(excel_file)
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
    opt = SolverFactory('cplex')
    #opt.options['mipgap'] = 0.001
    #opt.options['threads'] = 0

    Shangfei_results = opt.solve(Shangfei_model, tee = True,
    symbolic_solver_labels = True)

    Shangfei_model.solutions.store_to(Shangfei_results)
    Shangfei_results.write(filename = 'Shangfei_solution.yml')


if __name__ == '__main__':
    main()
