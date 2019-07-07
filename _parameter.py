import pyomo.environ as pyo

def parameter_initialisation(model, par_input):
    """
    This function takes the model input (model) and the
    parameter input objects to initialise the model's parameters
    """
    model.p = pyo.Param(
                        model.i, initialize = par_input.p,
                        doc = 'process time of task i'
    )

    model.B = pyo.Param(
                        model.k, initialize = par_input.B,
                        doc = 'resouce availability of k'
    )

    model.Bi = pyo.Param(
                         model.i, model.k, initialize = par_input.Bi,
                         doc = 'resouce requirements of each task'
    )

    model.precedence = pyo.Param(
                                model.i, model.j,
                                initialize = par_input.precedence,
                                default = 0,
                                doc = 'precedence set of each task i'
    )
