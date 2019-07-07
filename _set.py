# from pyomo.environ import *
import pyomo.environ as pyo


def set_initialisation(model, set_class):
    """
    This function takes in the model object and the set input (set_class)
    and initialise the set for the model
    """
    # set of monomer production plants
    model.i = pyo.Set(initialize = set_class.i,
                         doc = 'tasks', ordered = True)

    model.j = pyo.Set(initialize = model.i)

    model.t = pyo.Set(initialize = set_class.t,
                         doc = 'time intervals', ordered = True)

    model.k = pyo.Set(initialize = set_class.k,
                         doc = 'resource types', ordered = True)
